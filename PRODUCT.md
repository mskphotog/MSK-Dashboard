# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

A single user — Mark, the owner and sole maintainer. No second audience: nothing needs to be self-explanatory to a stranger, and nothing needs to be presentable to a client or teammate.

The situation is the start of a work session, or a mid-session jump between tools. He opens the dashboard in a **desktop browser on a Mac** and uses it as the place he goes to get somewhere else. He also uses it on at least one other device, which is why config transfer exists (see Operating Context).

## Product Purpose

MSK-Dashboard is a personal home base for the tools Mark uses and the small utilities he builds himself. It does two jobs:

1. **Launch** — a categorized grid of links to everything he works in: hosting and repo dashboards (Netlify, GitHub, Cloudflare), mail and Google accounts across multiple identities, hosted LLM chats, and his own deployed apps.
2. **Host** — increasingly, the tools themselves live here as sibling pages, not just links to elsewhere. `ollama-chat.html` and `passkey-tracker.html` are already part of the product, launched from the same grid as everything external.

Success is that the dashboard is the fastest path to any tool he owns, and that the utilities it hosts are worth opening on their own.

## Positioning

It is built for exactly one person's actual stack, so it can do things a general bookmark manager or start page cannot: encode Mark's own conventions (per-account Gmail identities, model knowledge-cutoff labels), open a link in the window shape that suits it, and host first-party tools alongside third-party links with no distinction in the interface.

## Operating Context

- **Categories are user-defined and evolve.** Live categories are `Stack / Tools / Assets`, `Google Stuff / Email`, `LLMs`, `Local LLMs` — not the code's shipped defaults. Category names, order, and card order within a category are all arranged by hand via drag-and-drop; that arrangement carries meaning and must survive any redesign.
- **Multi-device by manual transfer.** Export and Import exist specifically so Mark can move his configuration between devices. There is no account, sync service, or server — a JSON file is the transport. Both directions must keep working, and the export format is effectively a save file.
- **Two window modes.** Each app is launched either as a compact popup utility window or a standard browser tab, chosen per app. Local LLM chats and small tools suit the popup; full dashboards suit a tab.
- **Multiple identities in one place.** Several entries are the same service under different accounts (e.g. Gmail as `mskphotog` vs. a work address). Distinguishing near-identical entries at a glance is a real part of the job.
- **Local services are first-class.** Entries point at `localhost:8080` and `localhost/…` alongside public URLs. Links that only resolve on this machine are expected, not broken.
- **Manual annotations in names.** LLM entries carry hand-written knowledge-cutoff tags like `(C/O - Jan25)`. This is Mark's convention, maintained by hand in the app name field.
- **Runs from a local server.** Pages are served at `localhost:8080` (`npx serve .` / `python3 -m http.server 8080`), which is also how the hosted tool pages address each other.

## Capabilities and Constraints

**Confirmed today:**
- Add, edit, delete apps; each has a name, URL, category, and window mode.
- Create, rename, delete, and reorder categories. Deleting a non-empty category reassigns its apps rather than dropping them.
- Drag-and-drop reordering of cards within a category and of whole categories.
- Export/Import of the full configuration as JSON, accepting both the current `{ apps, categoryLabels }` shape and a legacy plain `apps` array.
- Hosted sibling tools: `ollama-chat.html` (streams from a local Ollama at `localhost:11434`, model chosen by `?model=` query param) and `passkey-tracker.html` (tracks which accounts have passkeys vs. passwords).
- Installable as a PWA (`manifest.json`, standalone display).

**Technical constraints (incumbent, observed):**
- Zero build. No package.json, no dependencies, no bundler. Every page is a single self-contained HTML file with inline CSS and JS, openable directly.
- All state is `localStorage` on the device. No backend, no accounts, no network persistence.
- `sw.js` is deliberately self-destructing and `index.html` clears caches on load, to prevent stale service-worker caching during development.

**Explicitly undecided — do not assume either way:**
- Whether the zero-build / single-file / local-only architecture is a permanent rule or the current convenient state. Treat it as binding until Mark says otherwise, and ask before introducing a build step, dependency, or backend.
- Whether true offline operation is a goal. It is not currently supported (the cache-buster and self-destructing service worker actively prevent it), and no one has asked for it.
- Whether mobile/tablet use matters. Desktop Mac browser is confirmed; other devices exist but their role is unstated.

## Brand Commitments

- The name is **MSK-Dashboard**. The PWA manifest separately carries "App Control Center" / "Control Center" — an inconsistency, not a second brand.
- `favicons/` holds eight unused candidate marks (grid, monogram, teal circle, dashboard bars, 3×3 grid, teal M, compass, stacked cards) with a `preview.html` to compare them. **No mark has been chosen.** The live favicon is an inline SVG wordmark ("MSK" with a blue rule).
- No voice, tone, or copy commitments have been established. There is no marketing surface and no external reader.

## Evidence on Hand

- Real configuration content, visible in Mark's live dashboard: four hand-made categories and ~20 real entries spanning hosting, repos, mail, hosted LLMs, and local LLMs.
- Two working first-party tool pages (`ollama-chat.html`, `passkey-tracker.html`).
- Eight candidate favicon SVGs in `favicons/`, undecided.
- **Absent — do not fabricate:** users other than Mark, usage metrics, testimonials, a public deployment, a roadmap, or any product claim. The dashboard's default seed data (`Dew Counter`, `your-counter-app.netlify.app`) is placeholder, not real content.

## Product Principles

1. **Speed to destination beats everything.** This is a surface people leave. Anything that slows the path from open to launch is a cost, not a feature.
2. **Manual arrangement is data.** Category order, card order, and hand-written name annotations are Mark's judgment made durable. Never re-sort, normalize, or "clean up" what he arranged.
3. **First-party tools sit as equals beside third-party links.** The hub does not distinguish between "my app" and "someone else's site" — both are just places to get to.
4. **One user means no defensive design.** No onboarding, no empty-state hand-holding, no explanatory copy for a newcomer who does not exist. Optimize for the hundredth visit, not the first.
5. **The config is portable and owned.** Export/Import is the sync story and the backup story. Any change to the data model must keep old exports importable.
