# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read first

**[HANDOFF.md](HANDOFF.md)** — running state, decisions already made, and what is deliberately unfinished. Read it before proposing changes; it holds the reasoning the code can't show you, including several choices that should not be quietly reversed. Update it when a session changes direction or settles something.

Also: [PRODUCT.md](PRODUCT.md) for who uses this and what must never break, and [DESIGN.md](DESIGN.md) for the visual system and its named rules. DESIGN.md is normative for anything visual.

## Running the App

The product is served by `server.py` — Python standard library plus SQLite, no build step, no dependencies, no package.json. It serves the pages and stores their data. By default it binds the Tailscale address `100.73.36.36:20006` only; to run it on your own machine, override the bind:

```bash
MSK_HOST=127.0.0.1 MSK_PORT=8080 MSK_DB=/tmp/dev.db python3 server.py
```

The pages no longer work from `file://` or a plain static server, because their data comes from `/api/*`. Deployment to the Omarchy box is in [deploy/README.md](deploy/README.md).

## Architecture

Three pages, each with CSS in `<style>`, markup in `<body>`, and its logic in a `<script>` block, plus `store.js` (the shared client for saving to the server) and `server.py`:

- `index.html` — the dashboard (the launcher and hub)
- `ollama-chat.html` — chat against a local Ollama at `localhost:11434`; model chosen via `?model=`
- `passkey-tracker.html` — tracks which accounts have passkeys and strong passwords

**Design tokens are duplicated in all three files** as `:root` custom properties, with light, dark, and explicit `[data-theme]` overrides. This is deliberate: a shared stylesheet would break the "every page opens directly" constraint. DESIGN.md holds the canonical values — change them there and in all three files together.

**Theme** — all three read and write the same `dashboardTheme` key, applied before paint by a small script in `<head>` to avoid a flash. Same origin, so one choice carries across the whole product.

**State model** — two arrays/objects in memory, persisted to SQLite on the server as one document (`GET`/`PUT /api/dashboard`). `store.js` turns `saveApps()` / `saveCategories()` calls into whole-document PUTs, one at a time, carrying a `baseRev`; a stale write gets a 409 with the current document and the page adopts it. Tables keep a `position` column, so hand-set order is stored, never derived. Only the theme (`dashboardTheme`) and the Restore snapshot stay in `localStorage`. The passkey tracker's accounts work the same way (`/api/passkeys`).
- `apps` — array of `{ id, name, url, category, type }` objects. `id` is a `Date.now()` string (the server always returns ids as strings). `type` is `"popup"` or `"tab"`.
- `categoryLabels` — plain object mapping internal slug keys (e.g. `"local"`) to display names (e.g. `"Local PWAs"`). **This object is the single source of truth for which categories exist.** Adding or deleting a key is all it takes to create or remove a category.

**Rendering** — `renderDashboard()` is a full re-render; it clears `#dashboardContainer` and rebuilds all DOM from the two state objects. It's called after every state mutation. There is no virtual DOM or diff — just wipe and rebuild.

**Category slugs** — `slugifyCategoryName()` converts a user-typed label to a URL-safe key. `getUniqueCategoryKey()` handles collisions. The slug is stored on each app as `app.category`; the human label lives only in `categoryLabels`.

**Cards are `<a href>` elements**, not divs. The click handler intercepts only popup-mode launches and bails on modified clicks (`metaKey`, `ctrlKey`, `shiftKey`, `altKey`) so ⌘-click, middle-click and the context menu behave natively. Popup windows are held in a `Map` keyed by app id so a re-click focuses the existing window. **Do not put `noopener` in the `window.open` features string** — it forces `_blank`, discards the window name, and reintroduces duplicate windows on every click.

**Arrange mode** (`editMode`) — a whole-page state. At rest the page is destinations only. Toggling Arrange reveals per-card edit/delete and per-category rename/delete/move controls, and enables dragging. Editing affordances exist *only* in this mode, which is what keeps the resting page scannable and gives every control a keyboard path.

**Drag-and-drop** — two independent systems share the same render cycle, both confined to Arrange mode (at rest, cards are links and drag natively):
- *Card reordering* within a category: `getDragAfterElement()` uses 2D distance to the center of each card to handle multi-column grid layout. On drop, `syncCategoryOrderFromDOM()` reads DOM order and rewrites the `apps` array in-place.
- *Category reordering*: `getCategoryDragAfterElement()` compares only vertical position (categories are single-column). On drop, `syncCategoryListOrderFromDOM()` rebuilds `categoryLabels` with keys in the new DOM order. The two drag systems are kept separate via `draggedFromCategory` and `draggedCategoryKey` flags.
- A cancelled drag re-renders from state, so the DOM and the saved state can't silently diverge. Alt+arrow reorders by keyboard.

**Dialogs** — native `<dialog>` throughout, via the `askConfirm()` / `askText()` helpers. No `prompt()`, `confirm()` or `alert()` anywhere in the project; the native `<dialog>` brings a focus trap, Esc, backdrop dismissal and an inert background, and stays out of the tab order when closed.

**Import/Export** — Export serializes `{ apps, categoryLabels }` as a dated JSON download. Import accepts either that combined format or a legacy plain `apps` array, **and this backward compatibility must be preserved** — export files are now the backup and migration path, and the owner's older exports must keep importing. Before overwriting, the current state is snapshotted to `dashboardBackupPrev` and a Restore control appears.

**Building card DOM** — use `textContent`, never `innerHTML` with interpolated app data. Import is the sync path, so a tampered file would otherwise execute script on load.

**PWA setup** — `sw.js` is intentionally self-destructing (it unregisters itself on activate) to prevent stale service worker caching during development. The cache-buster block at the top of `<head>` also aggressively clears caches and unregisters service workers on every page load. Do not replace this with a real caching service worker without understanding the implications.
