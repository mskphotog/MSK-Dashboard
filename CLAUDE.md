# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

This is a zero-build project — open `index.html` directly in a browser or serve it locally:

```bash
npx serve .
# or
python3 -m http.server 8080
```

No build step, no dependencies, no package.json.

## Architecture

The entire application lives in `index.html` as a single file: CSS in `<style>`, markup in `<body>`, and all logic in a `<script>` block.

**State model** — two arrays/objects in memory, each persisted to `localStorage`:
- `apps` (key: `dashboardAppsGrid`) — array of `{ id, name, url, category, type }` objects. `id` is a `Date.now()` string. `type` is `"popup"` or `"tab"`.
- `categoryLabels` (key: `dashboardCategories`) — plain object mapping internal slug keys (e.g. `"local"`) to display names (e.g. `"Local PWAs"`). **This object is the single source of truth for which categories exist.** Adding or deleting a key is all it takes to create or remove a category.

**Rendering** — `renderDashboard()` is a full re-render; it clears `#dashboardContainer` and rebuilds all DOM from the two state objects. It's called after every state mutation. There is no virtual DOM or diff — just wipe and rebuild.

**Category slugs** — `slugifyCategoryName()` converts a user-typed label to a URL-safe key. `getUniqueCategoryKey()` handles collisions. The slug is stored on each app as `app.category`; the human label lives only in `categoryLabels`.

**Drag-and-drop** — two independent systems share the same render cycle:
- *Card reordering* within a category: `getDragAfterElement()` uses 2D distance to the center of each card to handle multi-column grid layout. On drop, `syncCategoryOrderFromDOM()` reads DOM order and rewrites the `apps` array in-place.
- *Category reordering*: `getCategoryDragAfterElement()` compares only vertical position (categories are single-column). On drop, `syncCategoryListOrderFromDOM()` rebuilds `categoryLabels` with keys in the new DOM order. The two drag systems are kept separate via `draggedFromCategory` and `draggedCategoryKey` flags.

**Import/Export** — Export serializes `{ apps, categoryLabels }` as a JSON download. Import accepts either that combined format or a legacy plain `apps` array.

**PWA setup** — `sw.js` is intentionally self-destructing (it unregisters itself on activate) to prevent stale service worker caching during development. The cache-buster block at the top of `<head>` also aggressively clears caches and unregisters service workers on every page load. Do not replace this with a real caching service worker without understanding the implications.
