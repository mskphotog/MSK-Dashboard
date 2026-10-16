# Handoff

Running state of the project: what was decided, what is deliberately unfinished, and where to pick up. Read this before proposing changes — it holds the *why* behind choices that the code alone doesn't explain.

**Keep it current.** When a session ends having changed direction, resolved an open item, or made a decision worth honouring later, update this file. Stale continuity notes are worse than none.

**Related docs:** [PRODUCT.md](PRODUCT.md) (who uses this and what must never break) · [DESIGN.md](DESIGN.md) (the visual system and its named rules) · [CLAUDE.md](CLAUDE.md) (architecture and how to run it).

---

## State as of 14 Aug 2026

`main` at `ba196d8`, pushed, working tree clean. All three pages share one visual system.

The rebuild was two commits:

- **`3f5cb1a`** — rebuilt the dashboard's interaction layer and added PRODUCT.md / DESIGN.md.
- **`63d37e6`** — brought `ollama-chat.html` and `passkey-tracker.html` onto that system.

Since then: **`aa14f11`** settled the favicon (see below), and **`ba196d8`** fixed editing.

The visual layer had always been sound; the interaction layer had never been built. Two genuine bugs were found and fixed: every launch target was a `<div>` (nothing reachable by keyboard, no browser affordances), and `noopener` inside the `window.open` features string was discarding the window name, so popup mode spawned a duplicate window on every click.

### Editing an app silently did nothing (`ba196d8`)

Reported as "somewhere along the line I lost the ability to modify the existing Apps." Two things were behind it, and only one was a bug.

The bug: the submit handler looked up the app with `apps.find(a => a.id === id)`, where `id` comes from the dialog's hidden field and is therefore **always a string**. Cards saved by earlier versions carry a **number** in `id`, so the strict comparison never matched them — the dialog closed and announced "updated" while the app was left untouched. Delete and drag were never affected, because they compare the app object's id to itself. The fix coerces with `String(a.id) === id`. Verified in Chrome on a throwaway port with one string-id and one number-id card.

The other half was not a bug: **the edit affordance moved in the rebuild.** It used to appear on card hover (`.card:hover .card-actions`); it now lives only in Arrange mode, which is the "at rest the page is destinations only" decision below. Worth knowing that the change reads as a loss to someone who learned the hover gesture — but the affordance was deliberately relocated, not removed, so it stays where it is unless the owner asks otherwise.

A UX critique of `index.html` scored **14/36 (Poor)** before the rebuild — every visual heuristic at 2, every interaction heuristic at 1. The snapshot is in `.impeccable/critique/`, so a re-run shows movement rather than a fresh baseline. **It has not been re-run since the rebuild.**

---

## Moved to the Omarchy box (16 Oct 2026, uncommitted)

The dashboard now runs from `server.py` on the Omarchy box, bound to the Tailscale IP `100.73.36.36:20006` only, with its data in SQLite instead of per-browser `localStorage` and hand-carried JSON. The owner chose, in order: Python stdlib + SQLite, move the passkey tracker's data too, deploy by `git pull` + a systemd user service, retire Netlify and keep Export/Import as backup. Steps are in [deploy/README.md](deploy/README.md).

- **`server.py`** serves an allowlist of files and `GET`/`PUT /api/dashboard` and `/api/passkeys`. Writes replace the whole document in one transaction, storing a `position` per row, so the hand-set order is kept exactly. A daily snapshot goes to `backups/` before the first write of the day. It refuses a wildcard bind, rejects non-JSON and cross-origin writes, and sends `no-store`.
- **`store.js`** is the one shared script. It queues saves so only one is in flight, and sends `baseRev` with each. A stale write gets a 409 and the page adopts the server's copy with a dialog saying so; nothing is merged. A tab refetches when it becomes visible again (not mid-Arrange or with a dialog open). A failed save shows a notice and retries with backoff. The notice shows only on failure.
- **Ids are now always strings**, because SQLite stores them as text. This closes off the id-coercion trap in "Where to pick up" #3, and the latent bug where drag-reorder dropped number-id cards.
- **`sw.js` and the cache-buster are untouched.** Pages are served over plain HTTP on a non-localhost address, which is not a secure context, so Chrome will not offer to install the PWA from there. Tailscale's own HTTPS (`tailscale serve`) would change that, but it changes the address, so it is the owner's call.
- **Tested** on a throwaway port in Chrome: load, add and round trip (order and string ids preserved), conflict dialog, passkey debounce, outage and recovery. **Not tested on the box itself**, and not run on `100.73.36.36`.

### Things the move changes that the code doesn't fix

- **`ollama-chat.html` still calls `http://localhost:11434`.** From the new address that is the *viewing* machine's Ollama, and Ollama only accepts its default localhost origins, so it will refuse requests from `http://100.73.36.36:20006` unless `OLLAMA_ORIGINS` allows it on each machine. Not changed; pick between allowing that origin or pointing the page at the box's Ollama.
- **Cards that point at `localhost:8080`** (the sibling pages) need repointing.
- **Data does not carry over by itself.** The new origin starts empty; Export on the old dashboard, Import on the new one, once (same for the tracker).

---

## Decisions that constrain future work

These came from the owner directly. Don't quietly reverse them.

| Decision | Why it matters |
|---|---|
| **North star: "The Control Room"** | An instrument panel for one operator. The warmth is load-bearing — cool greys make it read as borrowed enterprise software. |
| **`index.html`'s palette is canonical** | Warm paper + indigo won over the tracker's cool greys. The other two pages were drift and have been reconciled. |
| **One signal colour** | Instrument Blue means *this responds to you*. Patina is the only ornamental colour. A second saturated accent is not available. |
| **Flat at rest** | Shadow and lift are responses to hover, drag, focus and open — never a way to rank importance. |
| **Dark mode is system-wide** | Every surface owes both themes. Dark is the same warm room with the lights down, never a cool-grey inversion. |
| **No command palette** | A ⌘K filter was explicitly declined: *"the grid is the point."* Keyboard access came from making cards real links, not from a search box. Don't re-propose it. |
| **The blue category flag stays** | The 3px rule is sanctioned by The Section Flag Exception in DESIGN.md, with a detector waiver scoped to `index.html` in `.impeccable/config.json`. |
| **Hand-set order is data** | Card and category order are the owner's judgment made durable. Nothing sorts, tidies, or inserts — new items append. |

---

## Deliberately open

**Card border contrast (~1.5:1 light, 1.8:1 dark).** Up from 1.16:1 but short of the 3:1 WCAG 1.4.11 asks of component boundaries. Reaching 3:1 needs roughly `#8d8676`, which turns the paper room into a wireframe and destroys the tone-step depth model the system rests on. The card is identified by its label at 14:1 and its state changes are high-contrast. This was a conscious trade, not an oversight — reopen it only with a plan that doesn't wreck the depth model.

**Design tokens are duplicated across all three HTML files.** The cost of keeping each page self-contained. Pages can no longer open from `file://` now that they need the API, so a shared `tokens.css` served by `server.py` is possible; it was not done in the move. Each file carries a comment saying so. If that constraint is ever relaxed, this is the first thing to collapse.

**Three product questions remain unanswered** and are recorded as undecided in PRODUCT.md rather than guessed at: whether zero-build is a permanent rule, whether true offline support is a goal (it is not supported today — the cache-buster and self-destructing service worker actively prevent it), and whether mobile/tablet matters beyond the confirmed Mac desktop.

**~~The favicon is undecided.~~ Settled in `aa14f11`** — the M monogram (`favicons/favicon-2-monogram.svg`), a bold M in Instrument Blue on paper, now applies to all three pages and the PWA manifest icons. The eight candidates and their `preview.html` remain in `favicons/` as a record of what was considered.

---

## Where to pick up

1. **Re-run the critique** (`/impeccable critique index.html`) to score the rebuild against the 14/36 baseline.
2. **Run an audit** (`/impeccable audit`) — the critique covered UX heuristics; the technical a11y / performance / responsive pass hasn't been done.
3. **Check whether other id comparisons need the same coercion `ba196d8` applied.** That fix was scoped to the edit-save path, which is where the failure showed up; nothing else compares an id round-tripped through the DOM today, but a future control that does will hit the same trap. Normalising ids to strings on load would close it off for good, at the cost of rewriting stored data.

Before any of that, the owner should open the dashboard, toggle the theme, and launch a Local LLM chat from a card — that exercises both P0 fixes at once.

---

## Testing note

When verifying in a browser, serve on a **throwaway port** and seed `localStorage` there. The owner's real data lives at `localhost:8080`; a different port is a different origin, so their configuration stays untouched. Clear the seeded keys and stop the server when finished.

There is also a published read-only summary of this state at
`https://claude.ai/code/artifact/08e3ff18-7a58-4403-b9e1-ab5f8ec25c79` — a static snapshot of `63d37e6`, not a live view. This file is the source of truth.
