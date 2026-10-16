#!/usr/bin/env python3
"""MSK-Dashboard server.

Serves the three pages and keeps their data in SQLite. Standard library only:
no pip, no npm, nothing to install.

It listens on the Tailscale address and nowhere else. A wildcard bind is
refused on purpose, so a config slip can't put the dashboard on the LAN.

    MSK_HOST   bind address            (default 100.73.36.36)
    MSK_PORT   port                    (default 20006)
    MSK_DB     database file           (default ~/.local/share/msk-dashboard/dashboard.db)

API (JSON). Each document is replaced whole, inside one transaction, so hand-set
order is written exactly as the client sent it and never re-sorted.

    GET /api/dashboard   -> { initialized, rev, apps, categoryLabels }
    PUT /api/dashboard   <- { baseRev, apps, categoryLabels }
    GET /api/passkeys    -> { initialized, rev, accounts }
    PUT /api/passkeys    <- { baseRev, accounts }

`rev` is bumped on every write. A PUT whose baseRev is stale gets 409 with the
current document, so a tab left open on one machine can't silently overwrite
changes made on another.
"""

import json
import mimetypes
import os
import sqlite3
import sys
import threading
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = os.environ.get("MSK_HOST", "100.73.36.36")
PORT = int(os.environ.get("MSK_PORT", "20006"))
ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get(
    "MSK_DB", Path.home() / ".local" / "share" / "msk-dashboard" / "dashboard.db"))

# Only these files are ever served, so .git, the database and the tooling
# folders can't be fetched by path.
STATIC_FILES = {
    "/": "index.html",
    "/index.html": "index.html",
    "/ollama-chat.html": "ollama-chat.html",
    "/passkey-tracker.html": "passkey-tracker.html",
    "/store.js": "store.js",
    "/manifest.json": "manifest.json",
    "/sw.js": "sw.js",
}

MAX_BODY = 5 * 1024 * 1024
BACKUPS_KEPT = 14

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    name       TEXT PRIMARY KEY,
    rev        INTEGER NOT NULL,
    updated_at TEXT NOT NULL
);
-- `position` is the whole point of these tables: order is the owner's
-- judgment, so it is stored, never derived.
CREATE TABLE IF NOT EXISTS categories (
    position INTEGER PRIMARY KEY,
    key      TEXT NOT NULL,
    label    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS apps (
    position INTEGER PRIMARY KEY,
    id       TEXT NOT NULL,
    name     TEXT NOT NULL,
    url      TEXT NOT NULL,
    category TEXT NOT NULL,
    type     TEXT NOT NULL CHECK (type IN ('popup', 'tab'))
);
CREATE TABLE IF NOT EXISTS accounts (
    position        INTEGER PRIMARY KEY,
    id              TEXT NOT NULL,
    site            TEXT NOT NULL,
    url             TEXT NOT NULL,
    username        TEXT NOT NULL,
    passkey         INTEGER NOT NULL,
    strong_password INTEGER NOT NULL,
    notes           TEXT NOT NULL
);
"""


class BadRequest(Exception):
    pass


class Conflict(Exception):
    pass


def connect():
    conn = sqlite3.connect(DB_PATH, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = connect()
    try:
        conn.executescript(SCHEMA)
    finally:
        conn.close()


# ----------------------------------------------------------------- backups

_backup_lock = threading.Lock()


def backup_if_due():
    """One snapshot per day, written before the first change of that day.

    The database is now the only copy of the owner's arrangement, so a bad
    import or a bad edit needs somewhere to roll back to."""
    stamp = datetime.now().strftime("%Y-%m-%d")
    folder = DB_PATH.parent / "backups"
    target = folder / f"dashboard-{stamp}.db"
    with _backup_lock:
        if target.exists():
            return
        folder.mkdir(exist_ok=True)
        src, dst = connect(), sqlite3.connect(target)
        try:
            src.backup(dst)
        finally:
            dst.close()
            src.close()
        for old in sorted(folder.glob("dashboard-*.db"))[:-BACKUPS_KEPT]:
            old.unlink()


# -------------------------------------------------------------- validation

def text(value, field):
    if value is None:
        return ""
    if isinstance(value, (str, int, float)) and not isinstance(value, bool):
        # ids from older versions of the app were numbers; they become
        # strings here, which is also what the DOM hands back on edit.
        return str(value)
    raise BadRequest(f"{field} must be text")


def clean_apps(raw):
    if not isinstance(raw, list):
        raise BadRequest("apps must be a list")
    out = []
    for item in raw:
        if not isinstance(item, dict):
            raise BadRequest("each app must be an object")
        kind = text(item.get("type"), "type") or "tab"
        if kind not in ("popup", "tab"):
            raise BadRequest("type must be 'popup' or 'tab'")
        out.append((text(item.get("id"), "id"), text(item.get("name"), "name"),
                    text(item.get("url"), "url"), text(item.get("category"), "category"), kind))
    return out


def clean_categories(raw):
    if not isinstance(raw, dict):
        raise BadRequest("categoryLabels must be an object")
    # dict preserves insertion order, which is the owner's order.
    return [(text(k, "category key"), text(v, "category label")) for k, v in raw.items()]


def clean_accounts(raw):
    if not isinstance(raw, list):
        raise BadRequest("accounts must be a list")
    out = []
    for item in raw:
        if not isinstance(item, dict):
            raise BadRequest("each account must be an object")
        out.append((text(item.get("id"), "id"), text(item.get("site"), "site"),
                    text(item.get("url"), "url"), text(item.get("username"), "username"),
                    1 if item.get("passkey") else 0, 1 if item.get("strongPassword") else 0,
                    text(item.get("notes"), "notes")))
    return out


# ------------------------------------------------------------------ access

def read_meta(conn, name):
    row = conn.execute("SELECT rev FROM meta WHERE name = ?", (name,)).fetchone()
    return (row["rev"], True) if row else (0, False)


def read_dashboard(conn):
    rev, initialized = read_meta(conn, "dashboard")
    if not initialized:
        return {"initialized": False, "rev": 0, "apps": None, "categoryLabels": None}
    apps = [dict(r) for r in conn.execute(
        "SELECT id, name, url, category, type FROM apps ORDER BY position")]
    cats = {r["key"]: r["label"] for r in conn.execute(
        "SELECT key, label FROM categories ORDER BY position")}
    return {"initialized": True, "rev": rev, "apps": apps, "categoryLabels": cats}


def read_passkeys(conn):
    rev, initialized = read_meta(conn, "passkeys")
    if not initialized:
        return {"initialized": False, "rev": 0, "accounts": None}
    accounts = [{"id": r["id"], "site": r["site"], "url": r["url"], "username": r["username"],
                 "passkey": bool(r["passkey"]), "strongPassword": bool(r["strong_password"]),
                 "notes": r["notes"]}
                for r in conn.execute("SELECT * FROM accounts ORDER BY position")]
    return {"initialized": True, "rev": rev, "accounts": accounts}


def write_document(name, reader, base_rev, replace):
    """Replace one document if base_rev still matches. Returns the new rev."""
    if not isinstance(base_rev, int) or isinstance(base_rev, bool):
        raise BadRequest("baseRev must be an integer")
    backup_if_due()
    conn = connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        current, _ = read_meta(conn, name)
        if current != base_rev:
            latest = reader(conn)
            conn.execute("ROLLBACK")
            raise Conflict(latest)
        replace(conn)
        rev = current + 1
        conn.execute(
            "INSERT INTO meta (name, rev, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(name) DO UPDATE SET rev = excluded.rev, updated_at = excluded.updated_at",
            (name, rev, datetime.now(timezone.utc).isoformat(timespec="seconds")))
        conn.execute("COMMIT")
        return rev
    except Conflict:
        raise
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()


def put_dashboard(body):
    apps = clean_apps(body.get("apps"))
    cats = clean_categories(body.get("categoryLabels"))

    def replace(conn):
        conn.execute("DELETE FROM apps")
        conn.execute("DELETE FROM categories")
        conn.executemany("INSERT INTO apps VALUES (?, ?, ?, ?, ?, ?)",
                         [(i, *a) for i, a in enumerate(apps)])
        conn.executemany("INSERT INTO categories VALUES (?, ?, ?)",
                         [(i, *c) for i, c in enumerate(cats)])

    return write_document("dashboard", read_dashboard, body.get("baseRev"), replace)


def put_passkeys(body):
    accounts = clean_accounts(body.get("accounts"))

    def replace(conn):
        conn.execute("DELETE FROM accounts")
        conn.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         [(i, *a) for i, a in enumerate(accounts)])

    return write_document("passkeys", read_passkeys, body.get("baseRev"), replace)


ROUTES = {
    "/api/dashboard": (read_dashboard, put_dashboard),
    "/api/passkeys": (read_passkeys, put_passkeys),
}


# ------------------------------------------------------------------ server

class Handler(BaseHTTPRequestHandler):
    server_version = "MSKDashboard"
    protocol_version = "HTTP/1.1"

    def send_json(self, status, payload):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def fail(self, status, message):
        self.send_json(status, {"error": message})

    def path_only(self):
        return self.path.split("?", 1)[0]

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        path = self.path_only()
        if path in ROUTES:
            conn = connect()
            try:
                self.send_json(HTTPStatus.OK, ROUTES[path][0](conn))
            finally:
                conn.close()
            return
        name = STATIC_FILES.get(path)
        if not name:
            return self.fail(HTTPStatus.NOT_FOUND, "not found")
        data = (ROOT / name).read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type",
                         (mimetypes.guess_type(name)[0] or "application/octet-stream")
                         + ("; charset=utf-8" if name.endswith((".html", ".js", ".json")) else ""))
        self.send_header("Content-Length", str(len(data)))
        # The project's standing posture: never serve a stale page.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def do_PUT(self):
        route = ROUTES.get(self.path_only())
        if not route:
            return self.fail(HTTPStatus.NOT_FOUND, "not found")

        # Guard against another site in the browser writing to this server:
        # a cross-origin page can't send application/json without a preflight
        # (which we never answer), and a mismatched Origin is refused outright.
        origin = self.headers.get("Origin")
        if origin and origin != f"http://{self.headers.get('Host', '')}":
            return self.fail(HTTPStatus.FORBIDDEN, "cross-origin write refused")
        if not (self.headers.get("Content-Type") or "").startswith("application/json"):
            return self.fail(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "send application/json")

        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            return self.fail(HTTPStatus.LENGTH_REQUIRED, "Content-Length required")
        if length > MAX_BODY:
            self.close_connection = True
            return self.fail(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "body too large")

        raw = self.rfile.read(length)
        try:
            body = json.loads(raw)
            if not isinstance(body, dict):
                raise BadRequest("body must be an object")
            rev = route[1](body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self.fail(HTTPStatus.BAD_REQUEST, "invalid JSON")
        except BadRequest as err:
            return self.fail(HTTPStatus.BAD_REQUEST, str(err))
        except Conflict as err:
            return self.send_json(HTTPStatus.CONFLICT, err.args[0])
        self.send_json(HTTPStatus.OK, {"rev": rev})

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


def main():
    if HOST in ("", "0.0.0.0", "::", "*"):
        sys.exit("Refusing to bind a wildcard address. Set MSK_HOST to the Tailscale IP.")
    init_db()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"MSK-Dashboard on http://{HOST}:{PORT}  (db: {DB_PATH})", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
