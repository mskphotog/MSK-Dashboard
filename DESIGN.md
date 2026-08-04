---
name: MSK-Dashboard
description: A warm-paper control room for one person's tools — flat panels, instrument-blue signal, and arrangement that stays exactly where it was put.
colors:
  instrument-blue: "#3654d1"
  instrument-blue-deep: "#2a41a8"
  instrument-blue-wash: "#eef0fb"
  patina: "#9c5e26"
  paper: "#f2f0ec"
  surface: "#ffffff"
  ink: "#24211d"
  rule: "#e4e0d6"
  muted: "#79746a"
  faint: "#c7c2b4"
  alert: "#b3261e"
  paper-dark: "#1a1815"
  surface-dark: "#24211d"
  ink-dark: "#f2f0ec"
  rule-dark: "#3a352d"
  muted-dark: "#a39d90"
  faint-dark: "#6b6558"
  instrument-blue-dark: "#7b93e8"
  instrument-blue-deep-dark: "#9aabee"
  instrument-blue-wash-dark: "#262b45"
  patina-dark: "#c98c46"
  alert-dark: "#f2b8b5"
typography:
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.4rem"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "normal"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "normal"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1rem"
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "1px"
  caption:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  chip:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.7rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0.5px"
rounded:
  sm: "4px"
  md: "6px"
  lg: "8px"
spacing:
  xs: "5px"
  sm: "10px"
  md: "15px"
  lg: "20px"
  xl: "25px"
  xxl: "30px"
components:
  button-primary:
    backgroundColor: "{colors.instrument-blue}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "8px 14px"
  button-primary-hover:
    backgroundColor: "{colors.instrument-blue-deep}"
    textColor: "{colors.surface}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "8px 14px"
  button-secondary-hover:
    backgroundColor: "{colors.instrument-blue-wash}"
    textColor: "{colors.instrument-blue}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
    height: "120px"
  card-hover:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
  chip-mode:
    backgroundColor: "{colors.instrument-blue-wash}"
    textColor: "{colors.instrument-blue}"
    rounded: "{rounded.sm}"
    padding: "2px 6px"
  input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "8px"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    width: "320px"
---

# Design System: MSK-Dashboard

## Overview

**Creative North Star: "The Control Room"**

This is an instrument panel for one operator. Every surface exists to answer *where do I go next* in under a second, and the entire visual system is organized around making destinations legible at a glance rather than making the interface itself interesting. The room is calm: warm off-white paper, hairline rules, white panels laid out in a grid. Nothing glows, nothing pulses, nothing competes. The only saturated color in the room is **Instrument Blue**, and it means one thing — *this responds to you*.

The warmth is deliberate and load-bearing. A control room rendered in cool greys reads as somebody else's software, borrowed and generic. The paper tone (`#f2f0ec`) and the brass-warm ink (`#24211d`) make it read as a workshop that belongs to a person — a bench that has been arranged, not a dashboard that was configured. **Patina** carries that further: the category labels are engraved in warm bronze, the one place the system permits an ornamental color, because those labels are the operator's own filing scheme made visible.

Density is moderate and deliberately un-clever. Cards are generous enough to hit without aiming, the grid reflows on its own, and arrangement is never automated — order in this system is a record of human judgment and the interface treats it as data, not decoration. The system rejects the two obvious neighbors: it is not a *start page* (no wallpaper, no clock, no weather, no search box pretending to be a browser), and it is not a *cool-grey SaaS admin panel* (no sidebar, no avatar menu, no chrome that implies an organization). There is one user. The design owes them speed and owes a stranger nothing.

**Key Characteristics:**
- Warm paper ground with pure-white panels — depth by tone, not by shadow
- Exactly one saturated accent, reserved for interactivity
- Bronze-engraved section labels as the only ornamental color
- Flat at rest; motion and shadow appear strictly as a response to the hand
- Hairline rules (1px) doing the work borders usually ask shadows to do
- System font stack throughout — zero webfont cost, native feel
- Grid that reflows itself, order that never does

## Colors

A warm, low-chroma room with a single cold signal color and one bronze ornament.

### Primary
- **Instrument Blue** (`#3654d1`): The signal color, and the system's only saturated voice. It marks anything that responds to input — primary buttons, focus rings, the active drop target, the window-mode chip, the hover border on a card, links. It is also the page title's color, which is the one exception: there it identifies the room rather than invites a click. Against paper it holds 5.5:1; white text on it holds 6.3:1.
- **Instrument Blue Deep** (`#2a41a8`): The pressed and hovered state of anything already blue. Never used at rest.
- **Instrument Blue Wash** (`#eef0fb`): The 10%-tint ground behind mode chips and secondary-button hover. Carries the signal's meaning at a whisper.

### Secondary
- **Patina** (`#9c5e26`): Warm bronze, used in exactly one place: the uppercase category labels that name each section of the grid. It is the operator's filing scheme rendered as engraving. It reaches 4.6:1 on paper and is always set bold and uppercase, never as running text.

### Neutral
- **Paper** (`#f2f0ec`): The room's ground. Warm off-white, never pure white, never grey.
- **Surface** (`#ffffff`): Panels — cards, modals, the chip backdrop. Pure white against warm paper is the primary depth cue in the entire system; it does more work than any shadow.
- **Ink** (`#24211d`): All primary text. A warm near-black, not `#000`, sharing the paper's hue family. 14:1 on paper.
- **Rule** (`#e4e0d6`): Every hairline — card borders, the header divider, input strokes. Warm sand, 1px, never heavier.
- **Muted** (`#79746a`): Secondary text — card URLs, form labels. **Only legible on Surface** (4.65:1), not on Paper (4.08:1). See The White-Backing Rule.
- **Faint** (`#c7c2b4`): The rest state of hover-revealed icon buttons only. Never used for text of any kind.

### Tertiary
- **Alert** (`#b3261e`): Destructive intent only — the hover color of delete controls. It never appears at rest, never fills a surface, and never marks anything non-destructive.

### Named Rules

**The One Signal Rule.** Instrument Blue means *this responds to you*. If an element is blue and cannot be clicked, dragged, focused, or dropped into, the color is wrong. The moment blue becomes ambient, it stops being a signal and the room loses its only instrument. No blue body text, no blue fills on inert elements, no blue used to decorate.

**The Section Flag Exception.** One structural use of Instrument Blue is sanctioned, and only one: the `3px` left rule on a category label. It is a flag marking where a section of the filing scheme begins — the operator's own structure, which is the closest thing this product has to a second signal worth spending the color on. The exception is deliberately narrow and does not generalize: it applies to the category label alone, never to cards, list items, callouts, alerts, or any other heading. Anything else reaching for a colored side border is decoration and takes Patina or nothing.

**The White-Backing Rule.** Muted text (`#79746a`) clears AA only against Surface, not against Paper. Secondary text therefore lives inside white panels, always. If a design needs quiet text directly on the paper ground, darken it to Ink or give it a white panel to sit on — do not place Muted on Paper and do not invent a fourth grey.

**The Warm Spine Rule.** Every neutral in this system shares the paper's warm hue. There are no cool greys and no pure blacks anywhere in the room, in either theme. A `#666` or a `#f5f6f8` entering this palette is drift, not a shade.

### Dark theme

Dark is an obligation of this system, not an option — every surface owes both themes. The dark room is the same warm room with the lights down, **not** a cool-grey inversion. The pairing is deliberately reciprocal: light Ink becomes the dark Surface, and light Paper becomes the dark Ink.

- **Paper Dark** (`#1a1815`) — ground · **Surface Dark** (`#24211d`) — panels · **Ink Dark** (`#f2f0ec`) — text
- **Rule Dark** (`#3a352d`) — hairlines · **Muted Dark** (`#a39d90`) — secondary · **Faint Dark** (`#6b6558`) — icon rest
- **Instrument Blue Dark** (`#7b93e8`) — the signal, lifted for contrast on a dark ground · **Deep Dark** (`#9aabee`) — hover, which moves *lighter* in dark rather than darker
- **Patina Dark** (`#c98c46`) · **Alert Dark** (`#f2b8b5`)

**The Lights-Down Rule.** Dark mode raises the accent and inverts the direction of hover (lighter, not darker); it never changes the hue family, never introduces a cool grey, and never drops the warmth. If the dark theme could be mistaken for a generic dark UI, it has been built wrong.

## Typography

**Display Font:** none — the system deliberately has no display face
**Body Font:** system UI stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)
**Label/Mono Font:** none distinct

**Character:** The native system face, used at small sizes with heavy weights and tight hierarchy. This is not a typographic system — it is a labeling system. Type here identifies things quickly and gets out of the way; the interest in this design lives in color, rule, and arrangement, not in letterforms. The practical payoff matters: zero webfont requests, instant first paint, and text that looks native in a popup utility window on macOS.

### Hierarchy
- **Headline** (600, `1.4rem`, 1.5): The page title, set in Instrument Blue. One per document, identifying the room.
- **Title** (600, `1.2rem`, 1.5): Modal headings. Ink.
- **Body** (700, `1rem`, 1.5): Card names — the primary scanning target of the entire product, which is why it is bold at body size rather than a larger light weight. Ink.
- **Label** (700, `0.9rem`, `1px` tracking, uppercase): Category names, set in Patina and hung off a 3px Instrument Blue rule. Also appears at `0.7rem` with `0.5px` tracking for the window-mode chip.
- **Caption** (400, `0.75rem`, 1.5): Card URLs and form labels, set in Muted, wrapping with `word-break: break-all` so a long URL never overflows its panel.

### Named Rules

**The Scan-Target Rule.** The card name is the only thing a user actually reads on this surface, so it is the boldest text in the system regardless of size. Never let a heading out-weight a card name; hierarchy here runs by function, not by document structure.

**The Small-Caps Spine Rule.** Uppercase plus letter-spacing is reserved for structural labels — category names and mode chips. It never appears on a button, a card name, or running text. Uppercase in this system means *this is a divider in the filing scheme*.

## Layout

The grid is the product. A single-column stack of category sections, each containing a self-reflowing card grid: `repeat(auto-fill, minmax(160px, 1fr))` with a `15px` gap. No breakpoints, no media queries, no column-count logic — the grid is intrinsically responsive and adapts from a popup utility window to a wide desktop browser with no code path of its own. `160px` is the deliberate floor: narrow enough to fit many tools across a desktop viewport, wide enough that a two-line card name and a wrapped URL stay readable.

Spacing runs on a **5px base**: `5 / 10 / 15 / 20 / 25 / 30`. Body padding is `20px`, category sections are separated by `30px`, category headers sit `12px` above their grid, and the header rule clears by `25px`. Cards hold a `120px` minimum height so a one-line entry and a three-line entry produce rows of equal weight — ragged card heights would break the scan.

Content is full-bleed to the body padding with no max-width container. This is correct for the hub, where more visible tools is strictly better; long-form or table surfaces (the passkey tracker) may cap at `960px` instead.

**The Ragged-Bottom Rule.** Categories are never padded, stretched, or balanced to make rows even. A category with three tools is three cards wide and stops. The grid's raggedness is the shape of the operator's real toolkit, and smoothing it would be a lie about the data.

**The Frozen-Order Rule.** Card order within a category, and category order down the page, are set by hand and are load-bearing data. Nothing in this system alphabetizes, re-sorts, auto-groups, or "tidies" them — not on render, not on import, not on add. New items append; they never insert.

## Elevation & Depth

**Flat at rest; depth is a response.** Panels sit on the paper ground held by a 1px Rule hairline and distinguished by tone — white on warm off-white. That tonal step is the primary depth mechanism, and it carries the entire resting state without a single shadow doing meaningful work.

Shadow enters only when the interface is reacting: a card lifts `2px` and takes a real shadow under the cursor; a modal floats decisively above a dimmed room; a primary button carries a tight blue-tinted shadow that reads as *pressable* rather than *raised*. The near-invisible resting shadow on cards (6% opacity) is an ambient seat, not elevation — it keeps a white card from looking pasted onto the paper, and it should never be strengthened to imply hierarchy.

Every shadow is tinted with the Ink hue (`rgba(36, 33, 29, …)`) rather than pure black, so shadows stay in the warm family with everything else.

### Shadow Vocabulary
- **Seat** (`0 1px 3px rgba(36, 33, 29, 0.06)`): Cards at rest. Prevents the pasted-on look. Not elevation.
- **Lift** (`0 4px 10px rgba(36, 33, 29, 0.1)`): Cards under the cursor, paired with `translateY(-2px)`.
- **Press** (`0 1px 2px rgba(54, 84, 209, 0.35)`): Primary buttons — blue-tinted, tight, reads as a key rather than a plane.
- **Float** (`0 8px 24px rgba(36, 33, 29, 0.15)`): Modals only. The only genuinely elevated surface in the system.
- **Focus** (`0 0 0 3px rgba(54, 84, 209, 0.15)`): Focused inputs. A ring, not a shadow — it never offsets.

### Named Rules

**The Reaction-Only Rule.** If a shadow is not the answer to something the user just did — hovering, dragging, focusing, opening — it does not belong. Static depth to signal importance is forbidden; importance is expressed with tone, rule, and position.

**The Warm-Shadow Rule.** No shadow uses pure black. Every one is tinted toward Ink or Instrument Blue.

## Shapes

A three-step radius scale where the size of the corner tracks the size of the object: `4px` for inline chrome (mode chips, inputs, the icon-button backdrop), `6px` for buttons, `8px` for panels (cards, modals). Corners are softened, never rounded — nothing in this system is a pill or a circle, because full-round shapes read as decorative and this room is instrumentation.

Borders are the system's structural language: **1px, Rule-colored, everywhere**. Cards, inputs, secondary buttons, the header divider, and table rows all share the same hairline, which is why the interface holds together despite carrying almost no shadow. The one intentional deviation is the category label's `3px` left border in Instrument Blue — a flag, not a border, marking where each section of the filing scheme begins.

Drag state is expressed by *changing the border's nature rather than adding chrome*: the dragged card drops to 40% opacity and its border switches to dashed Instrument Blue. The card becomes a hole with a marked edge — the shape of where it will land.

**The Hairline Rule.** Borders are 1px and Rule-colored. A 2px border, a darker stroke, or a double rule is not available in this system; if something needs more presence, change its tone or its position, not its border weight.

## Components

### Buttons
- **Shape:** Softly rounded (`6px`), compact padding (`8px 14px`), weight 500 at `0.9rem`.
- **Primary:** Instrument Blue fill, white text, carrying the tight blue Press shadow. Reserved for the single most likely action on the surface — on the hub, that is **+ Add App** and nothing else.
- **Secondary:** White fill, Rule hairline, Ink text, no shadow. Everything else — Export, Import, + Add Category. On hover the whole control adopts the signal: Wash background, Instrument Blue border and text.
- **Hover / Focus:** Primary deepens to Instrument Blue Deep. Transitions are fast (`0.2s`) and affect color only — buttons do not move.

### Cards / Containers
The signature component, and the one the whole system is built to serve. Tactile and confident: a real target you can hit without aiming. **It is an `<a>`, never a `<div>`** — the card is a link, so keyboard focus, status-bar URL preview, context menu, ⌘-click and middle-click are native rather than reimplemented.
- **Corner Style:** `8px`
- **Background:** Surface on the Paper ground
- **Border:** 1px Rule; becomes Instrument Blue on hover, dashed Instrument Blue while dragging
- **Shadow Strategy:** Seat at rest → Lift on hover (see Elevation)
- **Internal Padding:** `15px`, `104px` minimum height, left-aligned row
- **Motion:** `translateY(-2px)` on hover over `0.2s`; opacity to 0.4 while dragged
- **Anatomy, left to right:** a `34px` monogram tile, then a stacked column of name (Body, bold, Ink) → host (Caption, Muted) → mode chip on popup entries only

### Monogram Tile
The recognition signal, and the reason a card can be found without being read. A `34px` sunken tile with a `6px` radius carrying two letters (Label weight) derived from the name's meaningful words. **It is deliberately not colour-coded** — a hashed palette would install a second saturated voice and break The One Signal Rule, so recognition rides on the letterform alone. Its one variation is semantic: entries that resolve only on this machine take Patina letters and a Patina border, which is also the only place the local/remote distinction is drawn.

### Chips
- **Style:** Instrument Blue Wash ground, Instrument Blue text, `4px` radius, `2px 6px` padding, uppercase with `0.5px` tracking at `0.7rem`.
- **Role:** Marks the exception only — it appears on popup entries and is absent from tab entries, which are the majority. Read-only; it reports, it does not filter.

**The Exception-Only Rule.** A marker that fires on most of the set is wallpaper, not information. Any status chip in this system marks the minority case and stays silent on the default one. If a chip would appear on more than half the cards, invert it or delete it.

### Inputs / Fields
- **Style:** Paper-colored ground inside a white modal — a recessed well, inverting the panel relationship so fields read as *cut into* the surface. 1px Rule border, `4px` radius, `8px` padding.
- **Focus:** Border shifts to Instrument Blue and a 3px Wash-opacity ring appears. No offset, no movement, no glow.
- **Labels:** Caption size, Muted, block-level, `4px` above the field.

### Navigation
There is no navigation. The grid *is* the navigation, and the header carries only actions. Any future surface should reach the hub by returning to it, not by growing a persistent nav — a control room with a menu bar is an admin panel, which this explicitly is not.

### Modal
- Centered on a `rgba(36, 33, 29, 0.45)` warm scrim, `320px` max width, `8px` radius, Float shadow, 1px Rule border.
- Enters by opacity over `0.2s` with `pointer-events` gated — no scale, no slide.
- Actions right-aligned, `10px` apart, secondary before primary.

### Category Header
The system's most distinctive small component: an uppercase Patina label, letter-spaced `1px`, hung off a `3px` Instrument Blue left rule, with Rename and Delete links revealed alongside it. The whole header is the drag handle for reordering the section (`cursor: grab`), and the section drops to 40% opacity while it moves.

## Do's and Don'ts

### Do:
- **Do** keep Instrument Blue (`#3654d1`) exclusively on things that respond to input — The One Signal Rule.
- **Do** back secondary text with a white Surface; Muted (`#79746a`) fails AA on Paper at 4.08:1.
- **Do** hold every surface flat at rest and let shadow appear only as a reaction to hover, drag, focus, or open.
- **Do** ship both themes on every new surface, keeping the dark room warm and reciprocal (Ink becomes Surface, Paper becomes Ink).
- **Do** tint every shadow toward Ink (`rgba(36, 33, 29, …)`) or Instrument Blue — never pure black.
- **Do** keep hairlines at exactly 1px in Rule (`#e4e0d6`); the only wider stroke in the system is the 3px category flag.
- **Do** preserve hand-set order on render, import, and add — new items append and never insert.
- **Do** stay on the 5px spacing base (`5 / 10 / 15 / 20 / 25 / 30`).
- **Do** use the system font stack, so surfaces paint instantly and feel native in a popup window.
- **Do** let the grid reflow intrinsically via `auto-fill / minmax(160px, 1fr)` rather than adding breakpoints.

### Don't:
- **Don't** introduce a cool grey or a pure black. Every neutral shares the paper's warm hue — The Warm Spine Rule. The `#f5f6f8`/`#2f6fed` palette in `passkey-tracker.html` and the `#1e1e1e`/`#00adb5` palette in `ollama-chat.html` are drift, not sanctioned variants.
- **Don't** add a second saturated accent. One signal color is the entire premise; a green, an amber, or a purple would each cost the system its only instrument.
- **Don't** use Instrument Blue as decoration — no blue body text or fills on inert elements. The `3px` category flag is the single sanctioned structural use (The Section Flag Exception) and does not license a second one.
- **Don't** apply static shadows to imply importance. Depth is a response, never a rank.
- **Don't** use full-round or pill shapes. The radius scale stops at `8px`.
- **Don't** alphabetize, auto-sort, auto-group, or otherwise "tidy" cards or categories — The Frozen-Order Rule.
- **Don't** pad or balance a short category to even out the grid — The Ragged-Bottom Rule.
- **Don't** set Faint (`#c7c2b4`) as text; it is a 1.78:1 icon rest state and nothing else.
- **Don't** add a webfont. The zero-request type stack is a performance commitment, not a placeholder.
- **Don't** grow persistent navigation, a sidebar, an avatar menu, or other multi-user chrome. There is one operator.
- **Don't** add start-page furniture — clocks, weather, wallpaper, or a search field that impersonates the browser's.
