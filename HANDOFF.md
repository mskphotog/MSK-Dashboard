# Handoff

Running state of the project: what was decided, what is deliberately unfinished, and where to pick up. Read this before proposing changes — it holds the *why* behind choices that the code alone doesn't explain.

**Keep it current.** When a session ends having changed direction, resolved an open item, or made a decision worth honouring later, update this file. Stale continuity notes are worse than none.

**Related docs:** [PRODUCT.md](PRODUCT.md) (who uses this and what must never break) · [DESIGN.md](DESIGN.md) (the visual system and its named rules) · [CLAUDE.md](CLAUDE.md) (architecture and how to run it).

---

## State as of 5 Aug 2026

`main` at `63d37e6`, pushed, working tree clean. All three pages share one visual system.

Two commits did the work:

- **`3f5cb1a`** — rebuilt the dashboard's interaction layer and added PRODUCT.md / DESIGN.md.
- **`63d37e6`** — brought `ollama-chat.html` and `passkey-tracker.html` onto that system.

The visual layer had always been sound; the interaction layer had never been built. Two genuine bugs were found and fixed: every launch target was a `<div>` (nothing reachable by keyboard, no browser affordances), and `noopener` inside the `window.open` features string was discarding the window name, so popup mode spawned a duplicate window on every click.

A UX critique of `index.html` scored **14/36 (Poor)** before the rebuild — every visual heuristic at 2, every interaction heuristic at 1. The snapshot is in `.impeccable/critique/`, so a re-run shows movement rather than a fresh baseline. **It has not been re-run since the rebuild.**

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

**Design tokens are duplicated across all three HTML files.** The cost of the zero-build, self-contained-page constraint. A shared `tokens.css` would fix it but breaks "every page opens directly." Each file carries a comment saying so. If that constraint is ever relaxed, this is the first thing to collapse.

**Three product questions remain unanswered** and are recorded as undecided in PRODUCT.md rather than guessed at: whether the zero-build architecture is a permanent rule, whether true offline support is a goal (it is not supported today — the cache-buster and self-destructing service worker actively prevent it), and whether mobile/tablet matters beyond the confirmed Mac desktop.

**The favicon is undecided.** Eight candidate marks sit in `favicons/` with a `preview.html` to compare them; none has been chosen. The live icon is an inline SVG data URI.

---

## Where to pick up

1. **Re-run the critique** (`/impeccable critique index.html`) to score the rebuild against the 14/36 baseline.
2. **Run an audit** (`/impeccable audit`) — the critique covered UX heuristics; the technical a11y / performance / responsive pass hasn't been done.
3. **Pick a favicon** from `favicons/preview.html`.

Before any of that, the owner should open the dashboard, toggle the theme, and launch a Local LLM chat from a card — that exercises both P0 fixes at once.

---

## Testing note

When verifying in a browser, serve on a **throwaway port** and seed `localStorage` there. The owner's real data lives at `localhost:8080`; a different port is a different origin, so their configuration stays untouched. Clear the seeded keys and stop the server when finished.

There is also a published read-only summary of this state at
`https://claude.ai/code/artifact/08e3ff18-7a58-4403-b9e1-ab5f8ec25c79` — a static snapshot of `63d37e6`, not a live view. This file is the source of truth.
