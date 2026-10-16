# Deploying to the Omarchy box

The server is `server.py` (Python standard library + SQLite, nothing to install). It binds only to the Tailscale address, `100.73.36.36:20006`, and refuses a wildcard bind.

## First time

```bash
git clone <repo-url> ~/msk-dashboard
mkdir -p ~/.config/systemd/user
cp ~/msk-dashboard/deploy/msk-dashboard.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now msk-dashboard
loginctl enable-linger "$USER"        # start at boot, before you log in
```

Check it: `curl http://100.73.36.36:20006/api/dashboard` from any machine on the tailnet.

## Updating

```bash
cd ~/msk-dashboard && git pull && systemctl --user restart msk-dashboard
```

The database lives outside the repo (`~/.local/share/msk-dashboard/dashboard.db`), so a pull never touches your data.

## Moving your existing data in

Each browser's data lives at its own origin, so the new address starts empty. On the old dashboard, press **Export**; on the new one, press **Import**. Do the same in the passkey tracker with **Export backup** / **Import backup**. Once, from one machine. Every other machine then sees it.

## Backups

The first change each day writes a snapshot to `~/.local/share/msk-dashboard/backups/` (14 days kept). To roll back, stop the service and copy a snapshot over `dashboard.db`.

## Logs

`journalctl --user -u msk-dashboard -f`
