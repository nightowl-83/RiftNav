# Handoff: Rift Finder — Astral Rifts Reward Finder

## Overview

Rift Finder is a reference/lookup tool for Stellaris **Astral Rifts** and **Archaeological Dig Sites**. A player picks a rift, picks the reward they want, and the tool walks them step-by-step through the exact chain of chapter choices that produces that reward. Dig sites work similarly but are reference-only (phases and payouts, no branching path).

The UI is styled as a holographic ship console: dark space backdrop (animated galaxy map or looping video), glass panels, scanlines, corner HUD brackets, amber + cyan accents, monospace/techno type.

**The two things this handoff exists to document precisely are the two variant systems:**

- `layout` — Grid / Split column / Notched split
- `filterUI` — Menu / One line / Chips

Both must be implemented as component props/variants, not as separate screens. They are independent of each other (3 × 3 = 9 valid combinations).

## About the design files

The files in this bundle are **design references created in HTML** — working prototypes showing intended look and behavior. They are **not production code to copy directly**.

The task is to **recreate these designs in the target codebase's existing environment** (React, Vue, Svelte, native, etc.) using its established patterns, component library, and styling approach. If no environment exists yet, pick the framework most appropriate for the project and implement there.

The prototype uses a small custom template runtime (`support.js`). Ignore it — it is scaffolding, not part of the design. What matters is the markup structure, the computed inline styles, and the state logic in the `Component` class.

## Fidelity

**High-fidelity.** Colors, typography, spacing, radii, shadows, animation timings, and interaction states are final. Recreate pixel-accurately. Every value in this document is lifted from the prototype source.

---

# Variant system

## Prop: `layout`

Type: `'Grid' | 'Split column' | 'Notched split'`, default `'Grid'`.

Controls the home/browse screen only (rift detail, dig detail, and the step-by-step reader are identical across all three). Derived booleans used throughout:

```
split = layout === 'Split column' || layout === 'Notched split'
notch = layout === 'Notched split'
```

### Grid (default)

| Property | Value |
|---|---|
| Content container | `max-width: 1180px; margin: 0 auto; padding: 28px 34px 110px` |
| Card grid | `display: grid; grid-template-columns: repeat(auto-fill, minmax(266px, 1fr)); gap: 16px` |
| Browse-landing grid (the two "ASTRAL RIFTS / DIG SITES" tiles) | `display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; max-width: 760px` |
| Page title size | `44px`, letter-spacing `.1em` |
| Card min-height | `152px` |
| Pin rail width | `56px` |
| Galaxy map x-offset | `0` (centered) |
| Corner HUD opacity | `.85` |

### Split column

Content collapses to a narrow left column so the galaxy map backdrop stays visible on the right.

| Property | Value |
|---|---|
| Content container | `width: min(37vw, 520px); min-width: 320px; margin: 0; padding: 28px 26px 110px 34px` |
| Card grid | `display: flex; flex-direction: column; gap: 12px` |
| Browse-landing grid | `display: flex; flex-direction: column; gap: 14px` |
| Page title size | `29px`, letter-spacing `.06em` |
| Card min-height | `86px` |
| Pin rail width | `40px` |
| Rift/Dig segmented toggle | stacks vertically: `flex-direction: column; align-items: stretch; gap: 3px; padding: 3px` |
| Galaxy map x-offset | `0.17` (map shifts right so its core clears the column) |
| Corner HUD opacity | `.72` |

### Notched split

Same column geometry as Split column, but cards and the header panel take a **folder-tab silhouette** instead of a plain rounded rectangle. The card follows Figma node `82:17` (Rift Nav file), and the header panel shares the same frame so the notches line up down the column. Full geometry below.

| Property | Value |
|---|---|
| Card grid gap | `20px` (vs 12px in Split column) |
| Card width | `width: 100%; min-width: 320px; max-width: 920px` |
| Card padding | `31px 66px 18px 16px` (top clears the 25px notch; right clears the 52px + column) |
| Card min-height | `122px` |
| Card corner radius | `24px`; + column right corners `20px` |
| Card background/border | **none** on the card element itself. The shape comes from layers underneath plus one SVG outline (see below) |
| Corner brackets | **none** on the notched card (Grid and Split column keep them) |
| Header panel | Same frame as the card (no hover, no + column). Padding `44px 24px 22px`, height from content, `width: 100%; min-width: 320px; max-width: 920px` |

---

## The notched folder shape

### Card

The top edge steps down: a raised left tab, a 25px-deep notch across the middle, then back up to a right tab the width of the + column. **Only the left tab scales** (it ends at `25%` of the card width). Every other measurement is fixed px, so the slopes, notch depth and right tab look the same at any width.

| | Value |
|---|---|
| Left tab ends | `25%` of card width |
| Left slope | `42px` across × `25px` down |
| Notch depth | `25px` |
| Notch floor | `calc(25% + 42px)` → `calc(100% - 78px)` |
| Right slope | `26px` across × `25px` down |
| Right tab | `52px` wide, same as the + column; its inner edge lines up with the + divider |

Check at 683px wide (Figma 82:17): tab end `171`, floor `213 → 605` at `25` deep, right tab edge `631`.

Markup (the `.rf-fcw` wrapper carries the hover lift, because `c.wrap` runs the `wipeIn` entrance animation, which owns `transform`):

```html
<div class="rf-fcw">
  <div class="rf-fc" role="button" tabindex="0" aria-label="Ruined Planet, 10 chapters">
    <div class="rf-fc-shadow"></div>  <!-- z 0 -->
    <div class="rf-fc-fill"></div>    <!-- z 0 -->
    <div class="rf-fc-wash"></div>    <!-- z 1, hover only -->
    <div class="rf-fc-bar"></div>     <!-- z 1 -->
    <div class="rf-fc-outline"></div> <!-- z 3, SVG drawn by script -->
    <div class="rf-fc-body">…</div>   <!-- z 2 -->
  </div>
  <button class="rf-fc-cta" aria-label="Monitor Ruined Planet" aria-pressed="false">+</button>
</div>
```

All layers are `position: absolute; inset: 0; pointer-events: none` unless noted.

**Shadow**
```css
border-radius: 24px;
box-shadow: 0 18px 50px rgba(0,6,16,.4);
```

**Fill** (clipped glass body, no border)
```css
border-radius: 24px;
clip-path: polygon(0 0, 25% 0, calc(25% + 42px) 25px, calc(100% - 78px) 25px,
                   calc(100% - 52px) 0, 100% 0, 100% 100%, 0 100%);
background-image: linear-gradient(160deg, rgba(22,48,74,.44), rgba(6,16,28,.5));
background-size: 100% calc(100% + 26px);
background-position: 0 -26px;        /* pulls the gradient up so the notch doesn't lighten */
backdrop-filter: blur(20px) saturate(140%);
```

**Recessed bar** (fills the notch floor, capped with a hairline)
```css
top: 13px; height: 12px; left: calc(25% + 21px); right: 67px;
clip-path: polygon(0 0, 100% 0, calc(100% - 11px) 100%, 21px 100%);
border-top: 1px solid rgba(176,214,255,.26);
background: linear-gradient(185.7deg, rgba(13,32,53,.5) 36.5%, rgba(11,25,40,.5) 70.7%);
```

**Outline.** One SVG replaces the old tab and wedge layers. It is `position: absolute; inset: 0; overflow: visible; pointer-events: none` and a `ResizeObserver` redraws it from the card's live size:

```js
function folderPath(W, H) {
  const r = 24, h = -0.5, L = W * 0.25;   // stroke sits half a pixel outside the box, as in Figma
  return `M${h} ${r} A${r-h} ${r-h} 0 0 1 ${r} ${h} H${L} L${L+42} ${25-h}
    H${W-78} L${W-52} ${h} H${W-r} A${r-h} ${r-h} 0 0 1 ${W-h} ${r}
    V${H-r} A${r-h} ${r-h} 0 0 1 ${W-r} ${H-h} H${r}
    A${r-h} ${r-h} 0 0 1 ${h} ${H-r} Z`;
}
```

Stroke `1px`, no fill, horizontal `linearGradient` from `#fff` at 30% opacity to `#fff` at 16%. This is deliberately softer than Figma's 60% → 35%. Three paths share the same `d`, in this order: base, corner accents, hover (below). All ids are unique per card instance (`rf-fc-{n}-b`, `-h`, `-r`, `-m`).

**Corner accents.** A brighter copy of the outline shows only near the four outer corners. It fades along the line into the base stroke, with no visible start or end and no change in line weight.
```html
<path class="rf-fc-corners" fill="none" stroke-width="1"
      stroke="rgba(255,255,255,.42)" mask="url(#<id>-m)"/>

<radialGradient id="<id>-r">
  <stop offset="0"   stop-color="#fff" stop-opacity="1"/>
  <stop offset=".3"  stop-color="#fff" stop-opacity=".6"/>
  <stop offset=".65" stop-color="#fff" stop-opacity=".18"/>
  <stop offset="1"   stop-color="#fff" stop-opacity="0"/>
</radialGradient>
<mask id="<id>-m" maskUnits="userSpaceOnUse">
  <circle fill="url(#<id>-r)"/> × 4
</mask>
```
On each redraw, with `R = 72`, the mask box is set to `x = -R, y = -R, width = W + 2R, height = H + 2R`. The four circles get `r = R` and sit at `(0,0)`, `(W,0)`, `(0,H)` and `(W,H)`.

**+ column.** A separate `<button>`, a sibling of the card rather than a child, so clicking it never triggers the card's click and there are no nested interactive elements.
```css
position: absolute; top: 0; right: 0; bottom: 0; width: 52px;
border-left: 1px solid rgba(255,255,255,.15);
border-radius: 0 20px 20px 0;
font: 100 32px/1 'JetBrains Mono';  /* the "+" glyph */
color: #a3e5ff;
```
When monitored it shows `⦿` (19px, `#ffd9b0`) on the amber pin-rail gradient, `aria-pressed="true"` and the label "Stop monitoring {name}".

### Hover and focus

Applied on `:hover` and `:focus-visible`. Timing is `180ms cubic-bezier(.2,.7,.2,1)` throughout.

| Part | Rest | Hover / focus |
|---|---|---|
| Lift (`.rf-fcw`) | `translateY(0)` | `translateY(-2px)`; `:active` snaps back to `0` over `60ms`. No lift under `prefers-reduced-motion` |
| Shadow | `0 18px 50px rgba(0,6,16,.4)` | `0 24px 56px rgba(0,6,16,.55)` |
| Cyan outline | opacity `0` | opacity `1`. Same `d`, gradient `#8ecbff` 70% → 35%. SVG `filter: drop-shadow(0 0 5px rgba(142,203,255,.35))` |
| Corner accents | `rgba(255,255,255,.42)` | `rgba(191,230,255,.6)` |
| Wash | opacity `0` | opacity `1`. Same clip-path and radius as the fill, `linear-gradient(160deg, rgba(142,203,255,.09), rgba(142,203,255,0) 55%)` |
| Bar border-top | `rgba(176,214,255,.26)` | `rgba(142,203,255,.55)` |
| Group label | `#a8c4dc` | `#8ecbff` |
| + border-left | `rgba(255,255,255,.15)` | `rgba(142,203,255,.35)` |
| + glyph | `#a3e5ff` | `#d6f3ff` |

- **Pointer on the + itself:** background `rgba(163,229,255,.1)`, glyph `#fff`.
- **Keyboard focus:** same as hover, and the cyan path's `stroke-width` goes to `2px`. The card sets `outline: none`, and the lift comes from `.rf-fcw:has(> .rf-fc:focus-visible)`.
- **Tab order:** card, then its + button. The + shows a `1px #8ecbff` outline inset `5px` on focus.
- **Accessibility:** the card is `role="button"`, `tabindex="0"`, opens on Enter or Space, and is named "{title}, {n} chapters" (dig sites: "{n} phases").

### Header panel

In Notched split, the browse header panel (back button, title, subtitle, rift/dig-site toggle, search, Filter, Monitoring) uses **the same frame as the card**. It has the same fill clip-path, `folderPath()` geometry, recessed bar, and base and corner-accent paths, built by the same `frameRef()`/`buildFrame()` code. Its left tab, slopes, notch and 52px right tab therefore line up with the cards below it at every width. The Galactic index panel on the home screen uses the same frame.

```html
<div class="rf-fc-shadow"></div><div class="rf-fc-fill"></div><div class="rf-fc-bar"></div>
<div class="rf-fc-outline"></div>   <!-- frameRef('head', true): base + corner paths, no hover path -->
```

Differences from the card:

- **Size:** height comes from the content. Padding `44px 24px 22px`, where the top clears the 25px notch.
- **Width:** `100%`, `min-width: 320px`, `max-width: 920px`, the same as the cards.
- **Interaction:** no hover, lift, wash or + column.

The Grid and Split column headers are unchanged: a plain glass panel.

### Corner brackets (Grid and Split column cards)

Two L-brackets, radially masked so they fade out along their length. The notched card has none.

```css
/* top-left, amber */
position: absolute; left: 0; top: 0; width: 30px; height: 30px; z-index: 4;
border-left: 1.5px solid rgba(255,224,190,.85);
border-top: 1.5px solid rgba(255,224,190,.85);
border-top-left-radius: 14px;
mask-image: radial-gradient(circle 34px at 0 0, #000 22%, transparent 100%);

/* bottom-right, cyan */
border-right / border-bottom: 1.5px solid rgba(174,225,255,.8);
border-bottom-right-radius: 14px;
mask-image: radial-gradient(circle 34px at 100% 100%, #000 22%, transparent 100%);
```

---

## Prop: `filterUI`

Type: `'Menu' | 'One line' | 'Chips'`, default `'Menu'`.

Controls how the **reward-type filter** is presented on the rift browse screen (`browse === 'rift'`). It has no effect on the dig-site browse screen, which has no filter.

All three drive the same state: `cat`, a string that is either `'ALL'` or a reward category name. Category list is derived at runtime from the distinct `cat` values across all rewards, sorted alphabetically, with `'ALL'` prepended. Each entry carries a count (`ALL` = total reward count; otherwise rewards in that category).

Shared item styling — `catItem(c, mode)`:

```
/* base, all modes */
font-family: inherit; font-size: 10px; letter-spacing: .16em; cursor: pointer;

/* unselected */
border: 1px solid rgba(176,214,255,.2);
background: rgba(10,24,40,.36);
color: #a8c4dc;
box-shadow: inset 0 1px 0 rgba(255,255,255,.12);

/* selected */
border: 1px solid rgba(255,224,190,.7);
background: linear-gradient(180deg, rgba(255,214,170,.22), rgba(142,203,255,.1));
color: #fff8ef;
box-shadow: 0 10px 30px rgba(0,6,16,.36), inset 0 1px 0 rgba(255,255,255,.26);

/* count badge */
font-size: 9px; color: #ffd9b0 (selected) / #7f9cb4 (unselected)

/* glass (chip + strip modes only) */
backdrop-filter: blur(18px) saturate(140%);
```

### Menu (default)

A dropdown trigger that sits inline in the control row next to the search field.

**Trigger:**
```css
order: 1; flex: none; box-sizing: border-box; height: 40px;   /* 36px when condensed */
display: flex; align-items: center; cursor: pointer; user-select: none;
border-radius: 11px;
gap: 11px; padding: 0 16px;                 /* condensed: gap 7px; padding 0 11px */
backdrop-filter: blur(18px) saturate(140%);

/* cat === 'ALL' */
border: 1px solid rgba(176,214,255,.24);
background: rgba(10,24,40,.42); color: #cfe6ff;
box-shadow: inset 0 1px 0 rgba(255,255,255,.13);

/* a category is active */
border: 1px solid rgba(255,224,190,.6);
background: linear-gradient(180deg, rgba(255,214,170,.2), rgba(142,203,255,.08));
color: #fff8ef;
box-shadow: 0 10px 30px rgba(0,6,16,.36), inset 0 1px 0 rgba(255,255,255,.24);
```

Trigger contents, left to right: label (`ALL REWARD TYPES` or the category uppercased, `font-size: 10px; letter-spacing: .16em`, ellipsised, `max-width: 140px` when condensed), count (`font-size: 9px; color: #ffd9b0`), caret `▾` (`font-size: 9px; color: #8ecbff; transition: transform .22s ease`, rotates `180deg` when open).

When a category is active, a `✕ CLEAR` button appears next to the trigger: `order: 2; background: transparent; border: none; font-size: 9px; letter-spacing: .18em; color: #ffb87a`.

**Panel:**
```css
position: absolute; top: calc(100% + 9px); right: 0;
width: min(620px, 100%);
display: grid; grid-template-columns: repeat(auto-fill, minmax(184px, 1fr)); gap: 4px;
padding: 10px; border-radius: 14px;
background: linear-gradient(160deg, rgba(18,40,64,.97), rgba(5,13,24,.99));
border: 1px solid rgba(176,214,255,.24);
box-shadow: 0 26px 70px rgba(0,6,16,.55), inset 0 1px 0 rgba(255,255,255,.16);
animation: hudFade .16s ease-out; z-index: 600;
```

Rows use `catItem(c, 'row')`: `display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 10px 13px; border-radius: 9px`. Unselected rows are fully transparent (`border-color: transparent; background: transparent`); only the selected row shows the amber treatment. Picking a row sets `cat` **and closes the panel**.

### One line

A horizontally scrolling single row above the card grid.

Section header above it:
```
"REWARD TYPE"  font-size: 9px; letter-spacing: .22em; color: #a8c4dc
+ 1px flex-fill rule  rgba(176,214,255,.16)
+ "✕ CLEAR FILTER" (only when a category is active), color #ffb87a
margin-bottom: 11px
```

Rail:
```css
display: flex; gap: 8px; overflow-x: auto;
padding-bottom: 9px; margin-bottom: 22px;
mask-image: linear-gradient(90deg, #000 0, #000 93%, transparent 100%);
```

Items use `catItem(c, 'strip')`: `display: flex; align-items: center; gap: 8px; padding: 9px 15px; border-radius: 11px; flex: none; white-space: nowrap` + glass. Picking does **not** close anything.

### Chips

Same section header (`margin-bottom: 12px`), then a wrapping chip field:

```css
display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 30px;
```

Items use `catItem(c, 'chip')`: `display: flex; align-items: center; gap: 8px; padding: 9px 15px; border-radius: 11px` + glass. Identical to strip items minus `flex: none` / `white-space: nowrap`.

---

## Other props

| Prop | Type | Default | Effect |
|---|---|---|---|
| `backdrop` | `'Galaxy map' \| 'Video'` | `Galaxy map` | Galaxy map = procedural animated starfield (`galaxy-map.js`), reacts to the current screen via a `mode` of `galaxy` / `rift` / `dig`. Video = looping `uploads/bg-scene-1.mp4`, `object-fit: cover`, `animation: holoBreath 40s ease-in-out infinite`; first pass plays from 0, every loop after restarts at 2s. |
| `videoDim` | number 0–85, step 1, unit % | `46` | Only with Video backdrop. Renders `position: fixed; inset: 0; background: rgba(4,10,20, videoDim/100)`. |
| `holoScan` | boolean | `true` | Two fixed overlays at `z-index: 2`: a `repeating-linear-gradient(to bottom, rgba(174,225,255,.05) 0 1px, transparent 1px 4px)` at `opacity: .5; mix-blend-mode: screen`, plus a 34vh sweep band running `holoScan 11s linear infinite`. |
| `cornerBrackets` | boolean | `true` | Top-right and bottom-right fixed HUD bracket clusters. Auto-hidden when the content column would collide — see below. |
| `skipBoot` | boolean | `false` | Skips the boot sequence overlay. |

### Corner bracket collision rule

Both HUD clusters share one check, `checkHud()`, which measures the real content rather than using layout constants. After every render and on resize, it takes the right edge of the current screen's content (the union of the `.rf-main` wrapper's children, from `getBoundingClientRect`). Both clusters show only when that edge stays at least 16px clear of the 180px corner column:

```js
right   = max(child.getBoundingClientRect().right for child of .rf-main)
visible = vw >= 768 && right <= vw - 180 - 16
```

In practice they show beside the narrow browse column and home panel at desktop widths, and hide on the rift, reader and dig detail screens, where content runs to the right edge.

Bottom cluster: `position: fixed; right: 0; bottom: 34px; width: 180px; height: 180px; z-index: 860`.
Top cluster: `position: fixed; right: 0; top: 56px; width: 180px; height: 210px; z-index: 860`.
Opacity `.72` when `split`, `.85` otherwise.

---

# Screens

## 1. Boot overlay

Full-screen modal, `z-index: 9000`, `background: rgba(4,10,20,.62)` + `backdrop-filter: blur(26px) saturate(130%)`. Panel `width: min(540px, 88vw); padding: 34px 34px 30px; border-radius: 18px`, glass gradient `linear-gradient(160deg, rgba(24,52,80,.5), rgba(6,16,28,.6))`, `border: 1px solid rgba(176,214,255,.24)`, amber top-left + cyan bottom-right corner brackets (26px, 1.5px, radius 18px).

Six log lines reveal one at a time at `170ms × index`, plus 2 extra ticks (the last one delayed a further 220ms):

```
POWER ON SELF TEST ......... OK
OBSERVATION DECK FEED ...... LIVE
ASTRAL PLANE TELEMETRY ..... OK
RIFT INDEX 32 / CHAPTERS 289
REWARD MANIFEST 71 ENTRIES
GUIDE PROJECTION ........... OK
```

Each line: `font-size: 11px; letter-spacing: .14em; color: #bcd6ea`, prefixed `› `, `animation: hudFade .18s ease-out`. Container `min-height: 150px; gap: 7px`.

Progress bar: 3px track `rgba(176,214,255,.16)`, fill `linear-gradient(90deg, #8ecbff, #ffd9b0)` with `box-shadow: 0 0 14px rgba(174,225,255,.6)`, `transition: width .18s linear`.

Footer row: `PROJECTING HOLOGRAPHIC GUIDE` (left, `#7fa3c0`) / percentage (right, `#8ecbff`), both `font-size: 10px; letter-spacing: .2em`. When complete, `LINK ESTABLISHED` appears — Chakra Petch 13px, `letter-spacing: .24em`, `color: #ffd9b0`, `animation: blink 1s infinite`.

Header: 16px rotated-45° diamond outlined `#8ecbff` with `box-shadow: 0 0 14px rgba(142,203,255,.8)` and `animation: blink 1.4s infinite`; `RIFT NAV` Chakra Petch 19px/700, `letter-spacing: .24em`, `#f2f9ff`; `HOLO v5.0` 10px, `letter-spacing: .2em`, `#7fa3c0`.

## 2. Top navigation (sticky, all screens)

```css
display: flex; align-items: center; gap: 20px;
height: 56px; padding: 0 34px;
position: sticky; top: 0; z-index: 900;
background: linear-gradient(180deg, rgba(10,24,40,.62), rgba(6,14,26,.38));
backdrop-filter: blur(20px) saturate(140%);
border-bottom: 1px solid rgba(176,214,255,.16);
box-shadow: 0 12px 40px rgba(0,6,16,.35);
```

Contents: 13px diamond mark → `RIFT NAV` (Chakra Petch 15px/700, `.18em`, `#f2f9ff`) → `// HOLO DECK` (10px, `.22em`, `#7fa3c0`) → stat run `32 RIFTS · 289 CHAPTERS · 71 REWARDS` (10px, `.16em`, `#7fa3c0`, `gap: 18px`) → right cluster: camera toggle button, CLASSIC/HOLO segmented link pair, and a `GUIDE ONLINE` status pip (6px dot `#ffd9b0`, `box-shadow: 0 0 10px #ffd9b0`, `animation: blink 2.4s infinite`).

## 3. Compact scroll bar

On the browse lists only (not the rift, reader or dig detail screens), scrolling past **130px** cross-fades in a fixed compact bar; it fades back out below **90px** (hysteresis — do not use a single threshold, it causes jitter).

```css
position: fixed; left: 0; right: 0; top: 56px; z-index: 840;
display: flex; align-items: center; flex-wrap: nowrap; gap: 10px;
padding: 11px 34px;
background: linear-gradient(180deg, rgba(7,17,30,.97), rgba(7,16,28,.92));
backdrop-filter: blur(26px) saturate(140%);
border-bottom: 1px solid rgba(176,214,255,.18);
box-shadow: 0 16px 34px rgba(0,6,16,.55);
transition: opacity .26s ease,
            transform .3s cubic-bezier(.16,.86,.24,1),
            visibility .26s;

/* shown */  opacity: 1; transform: translateY(0);    pointer-events: auto; visibility: visible;
/* hidden */ opacity: 0; transform: translateY(-12px); pointer-events: none; visibility: hidden;
```

Contains: back chevron, the ASTRAL RIFTS / DIG SITES toggle, a 34px search field (`flex: 1 1 170px; max-width: 300px`), the category trigger (Menu mode only), spacer, monitoring count.

**Important:** the compact bar is a separate fixed element that cross-fades. The page header does **not** resize itself on scroll — an earlier version did and it caused a feedback loop (header shrinks → scroll position changes → header grows).

## 4. Home / Galactic index

No browse mode selected. Title `GALACTIC INDEX`, subtitle `AWAITING QUERY // {n} RIFTS · {n} DIG SITES`.

Two entry tiles (`browseGrid`), each: `border-radius: 14px; padding: 22px; min-height: 140px`, glass `linear-gradient(160deg, rgba(22,48,74,.44), rgba(6,16,28,.5))`, `border: 1px solid rgba(176,214,255,.2)`, `box-shadow: 0 18px 50px rgba(0,6,16,.4), inset 0 1px 0 rgba(255,255,255,.13)`. One 20px corner bracket each (amber top-left on the first tile, cyan bottom-right on the second).

Tile content: `BROWSE` eyebrow (9px, `.22em`, `#8ecbff`) → pushed to bottom: name (Chakra Petch 22px/600, `#f6fbff`) → count line (10px, `.12em`, `#8ba7bf`).

Hover: `border-color: rgba(174,225,255,.6); transform: translateY(-2px); box-shadow: 0 22px 60px rgba(0,6,16,.5), inset 0 1px 0 rgba(255,255,255,.2), 0 0 0 1px rgba(174,225,255,.18)`.

Entrance: `animation: wipeIn .55s cubic-bezier(.2,.75,.2,1) both` at `.36s` / `.43s`.

## 5. Browse — rifts / dig sites

Title `SELECT RIFT` / `SELECT DIG SITE`, subtitle `SCAN COMPLETE // {n} SIGNATURES IN RANGE` / `SURVEY COMPLETE // {n} SITES CATALOGUED`.

Header block contains: back-to-galaxy button, title block, the rift/dig segmented toggle, and the control row (search + filter + monitoring). In Notched split this whole block takes the folder-tab treatment; in Grid and Split column it is a plain glass panel (`padding: 16px 18px 14px; border-radius: 16px`).

**Card anatomy** (identical structure for both rifts and dig sites, only accent color and meta differ):

- Row 1: 5px status dot (`#8ecbff` for rifts, `#7fe0d4` for dig sites, with matching 8px glow) → group label (9px, `.2em`, `#a8c4dc`) → signature code pushed right (9px, `.14em`, `#6f8ea6`). Codes are deterministic hashes: `SIG-{hash % 9000 + 1000}` for rifts, `ARC-…` for dig sites.
- Title: Chakra Petch 19px/600, `letter-spacing: .03em`, `line-height: 1.15`, `#f6fbff`, `text-wrap: pretty`, pushed to bottom with `margin-top: auto`.
- 1px rule `rgba(176,214,255,.18)`, `margin-top: 9px`.
- Meta row (10px, `.12em`): rifts → `{n} CHAPTERS` (`#8ba7bf`) / `{n} REWARDS` or `{n} MATCH` (`#ffd9b0`); dig sites → `{n} PHASES` (`#8ba7bf`) / DLC name (`#7fe0d4`).

**Dig site list** (audit step 3). The dig list differs from the rift list:

- **Filter.** The same reward-type filter as rifts (Menu, One line or Chips, per `filterUI`), fed by the dig reward categories in `dig-data.js`. On the dig list the counts are **sites**, not rewards, so `RELICS 10` answers "which digs give a relic?" in one tap. Rift and dig filters keep separate state (`cat` / `digCat`). Every filter item is a `<button>` with `aria-pressed`.
- **Section headings** replace the group label on every card. One heading per site group, in `DIG_DATA.groups` order (Base game, Unique system, Origin, Precursor, Ancient Relics, Other expansion). A heading is Chakra Petch 14px/600 uppercase `#d6ecff`, followed by an `{n} SITES` count (11px `#7f9cb4`) and a fading rule. Empty groups are hidden; with nothing left, the list shows "No dig sites match…".
- **Card content** (folder card shape, hover and focus unchanged):
  - Row 1: teal dot → `{n} PHASES` (11px mono, takes the card's hover colour) → `ARC-####` pushed right. The code is decorative: 11px `#56738a`.
  - Name: Chakra Petch 19px/600.
  - Rule.
  - **Yields line**: up to 3 chips, ranked relic → technology → specimen → modifier → planet/deposit → everything else. Risks are never a yield, and each kind shows once.
    - Chips are 11px mono, `border-radius: 999px`, `rgba(176,214,255,.24)` border.
    - A relic chip is amber (`#ffd9b0` on `rgba(255,217,176,.1)`, 12px since it carries the relic's name) and reads `◆ {relic name}`.
    - A teal outline chip shows the DLC, only when it isn't the base game.
  - The card's `aria-label` reads name, phase count and yields.

**Pin rail** (Grid and Split column; the notched card uses its own + column, see [The notched folder shape](#the-notched-folder-shape)). A full-height strip on the card's right edge that toggles monitoring:

```css
flex: none; position: relative; align-self: stretch;
display: flex; align-items: center; justify-content: center; cursor: pointer;
width: 56px;                                   /* 40px when split */
margin: -14px -16px -14px 14px;
border-radius: 0 13px 13px 0;
border-left: 1px solid rgba(176,214,255,.16);  /* .34 when active */
transition: background-color .2s, color .2s, border-color .2s;

/* inactive */ background: rgba(8,18,32,.34);  color: #7f9cb4;
/* active   */ background: linear-gradient(180deg, rgba(255,214,170,.22), rgba(255,196,132,.09));
               color: #ffd9b0;
```

Icon `✚` → `⦿` when monitored, 19px. Hover shows a tooltip above: `MONITOR SITUATION` / `STOP MONITORING`, `padding: 6px 9px; border-radius: 7px; font-size: 8px; letter-spacing: .2em; color: #07111e; background: #ffd9b0; border: 1px solid rgba(255,255,255,.5)`.

**Card hover** (Grid and Split column; the notched card has its own, see [Hover and focus](#hover-and-focus)): the card slides right and grows an amber left edge —
```css
border-color: rgba(174,225,255,.6);
box-shadow: -6px 0 0 -3px rgba(255,224,190,.7),
            0 22px 60px rgba(0,6,16,.5),
            inset 0 1px 0 rgba(255,255,255,.2),
            0 0 0 1px rgba(174,225,255,.18);
transform: translateX(9px);
z-index: 520;
```

**Card entrance:** `animation: wipeIn .8s cubic-bezier(.16,.86,.24,1) both`, delay `0.42 + min(index, 16) × 0.075` seconds.

**Search** — live. On the browse lists it filters by name. From home, the dropdown returns, in order:
- up to 6 rifts;
- up to 5 **rift rewards** (badge `RIFT REWARD`, `#a8d8ff`; picking one opens that reward's reader);
- up to 4 dig sites (named first, then sites whose rewards match);
- up to 4 dig payouts.

A reward matches on its short name, full name, effect, category or relic name. Matches on the name, the category or the relic's name rank ahead of matches that only appear in the effect text, so "relic" returns rift relics, dig relics and the sites that give them. Result rows are a grid: the badge on the left, the name (12px) on the first line and the meta (11px) on the second, so names don't wrap word by word at 390px. Empty state: `NO SIGNATURE MATCHES`.

Dropdown panel: `top: calc(100% + 8px); padding: 8px; border-radius: 14px; background: linear-gradient(160deg, rgba(16,36,58,.98), rgba(5,13,24,.985))` + `backdrop-filter: blur(30px)` (see **Overlays** below; was `.97 / .99`; border: 1px solid rgba(176,214,255,.24); box-shadow: 0 26px 70px rgba(0,6,16,.55), inset 0 1px 0 rgba(255,255,255,.16)`. Row hover: `background: rgba(176,214,255,.1)`.

## 6. Monitoring

Users pin rifts and dig sites to a watch list. State is `monitored: [{ type: 'rift'|'dig', name }]`.

- **Wide viewport, detail screen open** → a tab strip sticks under the nav at `top: 56px`, `z-index: 480`. Active tab: `padding: 8px 12px 9px; background: rgba(20,44,70,.72); color: #fff8ef; border-bottom-color: transparent`. Inactive: `padding: 6px 12px 7px; background: rgba(8,18,32,.4); color: #8ba7bf`. Both `border-radius: 7px 7px 0 0; margin-bottom: -1px`.
- **Narrow viewport (< 720px)** → the strip becomes a dropdown.
- **On the browse screen** → a dropdown trigger in the control row, amber-tinted: `border: 1px solid rgba(255,224,190,.44); background: linear-gradient(180deg, rgba(255,214,170,.16), rgba(142,203,255,.06)); color: #fff8ef`.

Switching tabs **preserves per-item progress** (`reward`, `cur`, `railOpen` are stashed in `progress` keyed by `type:name` and restored on return).

Toggling monitoring fires a toast: `position: fixed; left: 50%; bottom: 30px; transform: translateX(-50%); z-index: 950; padding: 11px 18px; border-radius: 11px`, glass `linear-gradient(160deg, rgba(24,52,80,.86), rgba(6,16,28,.94))`, border amber `rgba(255,224,190,.5)` on add / cyan `rgba(176,214,255,.3)` on remove, `animation: hudIn .24s cubic-bezier(.16,.86,.24,1)`, auto-dismiss after **2600ms**.

## 7. Rift detail — select target reward

Container `max-width: 1180px; margin: 0 auto; padding: 40px 34px 110px; animation: hudIn .32s ease-out`.

Header: `‹ ABORT / ALL RIFTS` button + monitor toggle → eyebrow is the category, `{GROUP} RIFT` (`UNIQUE RIFT`, `PRECURSOR RIFT`, `GENERAL RIFT`) or `RIFT SITUATION`; "RIFT LOCKED" read as "you can't access this" (11px, `.22em`, `#a8c4dc`) → `<h1>` Chakra Petch 44px/700, `letter-spacing: .04em`, `#f6fbff`, `text-shadow: 0 4px 30px rgba(3,10,20,.9), 0 0 40px rgba(142,203,255,.22)`.

Right-aligned `ACCESS REQUIREMENTS` panel: `max-width: 400px; border-radius: 14px; padding: 16px 18px`, glass `linear-gradient(160deg, rgba(22,48,74,.4), rgba(6,16,28,.5))`, `border: 1px solid rgba(176,214,255,.2)`, amber 20px top-left bracket. Body 11px / `line-height: 1.7` / `#cfe0ef`; restriction line prefixed `⚠` in `#ffb87a`.

Divider: `height: 1px; background: linear-gradient(90deg, rgba(255,222,186,.5), rgba(174,225,255,.3) 40%, transparent); margin: 22px 0 26px`.

Reward grid: `repeat(auto-fill, minmax(336px, 1fr)); gap: 18px`. Each card `border-radius: 16px; padding: 24px; min-height: 194px`, glass `linear-gradient(155deg, rgba(26,54,82,.46), rgba(6,16,28,.54))`, `backdrop-filter: blur(22px) saturate(140%)`, `box-shadow: 0 22px 60px rgba(0,6,16,.42), inset 0 1px 0 rgba(255,255,255,.14)`, **four** 22px corner brackets (amber TL + BR, cyan TR + BL).

A relic reward also shows a compact **Relic card** (below) between its name and the progress bar. Card content: category (9px, `.2em`, `#8ecbff`) + code `RWD-{hash % 900 + 100}` right → name Chakra Petch 26px/600 pushed to bottom → 3px progress bar + meta `{n} STEPS / ROLL {n}` or `/ NO ROLLS`. Bar gradient is amber (`#ffb87a → #ffd9b0`) when the hardest roll is ≥ 5, cyan (`#8ecbff → #d6ecff`) otherwise; width `min(100, steps/9 × 100)%`.

Hover: `border-color: rgba(174,225,255,.62); transform: translateY(-2px); box-shadow: 0 26px 70px rgba(0,6,16,.5), inset 0 1px 0 rgba(255,255,255,.2)`.

## 8. Step-by-step reader

Three columns, `max-width: 1460px; gap: 22px; padding: 28px 34px 96px; align-items: flex-start`.

**Left — EVENT LOG** (`flex: 1 1 246px; max-width: 300px`, sticky at `top: 84px`, or `127px` when the monitoring strip is present). One row per step, expandable to show all choices at that chapter with the picked one marked `◆` (`#ffd9b0`) and the rest `◇` (`#5a7893`). Active row: `border: 1px solid rgba(174,225,255,.6); background: linear-gradient(180deg, rgba(142,203,255,.18), rgba(142,203,255,.06))`. Scroll region `max-height: calc(100vh - 208px)`. A `◆ CLAIM REWARD` row pins to the bottom of the list. Below: `✕ ABORT RIFT` button in the danger palette (`background: rgba(30,14,10,.4); border: 1px solid rgba(255,150,110,.34); color: #ffb87a`).

**Center — step card** (`flex: 100 1 470px`). `border-radius: 18px; padding: 36px 38px 38px`, glass `linear-gradient(165deg, rgba(24,52,80,.5), rgba(6,16,28,.62))`, `backdrop-filter: blur(26px) saturate(145%)`, four 28px corner brackets (the amber pair carries an extra `16px` glow shadow).

- Meta row: `STEP n OF m`, the **only** progress count on the screen; the claim step isn't counted (11px, `.22em`, `#8ecbff`) + rule + route pill when applicable (`color: #ffd0a0; border: 1px solid rgba(255,208,160,.45); border-radius: 9px; padding: 5px 11px; background: rgba(255,190,130,.08)`).
- `<h2>` Chakra Petch 36px/700, `line-height: 1.1`.
- **Choice callout** — the key element: `border-radius: 14px; border: 1px solid rgba(174,225,255,.45); background: linear-gradient(160deg, rgba(142,203,255,.16), rgba(142,203,255,.05)); box-shadow: inset 0 1px 0 rgba(255,255,255,.2), 0 0 30px rgba(142,203,255,.1); padding: 22px 24px`. Label row: blinking 5px cyan dot + one of `SELECT THIS OPTION` / `ONLY OPTION AVAILABLE` / `NO CHOICE NEEDED HERE` / `FINAL OPTION`. Choice text Chakra Petch 23px/500, pure `#ffffff`.
- `OTHER OPTIONS ON SCREEN // DO NOT SELECT` — amber warning list, each row `border-left: 2px solid rgba(255,184,122,.5); padding: 3px 0 3px 13px; color: #ffc79a`, prefixed `✕`.
- `SALVAGE ACQUIRED AT THIS STEP` — rows prefixed `▸`, 12px, `#cfe0ef`.

**Final card** (after the last step): `background: radial-gradient(120% 100% at 50% 0%, rgba(142,203,255,.24), rgba(6,16,28,.66) 62%)`, `border: 1px solid rgba(174,225,255,.5)`, `box-shadow: 0 30px 90px rgba(0,6,16,.55), inset 0 1px 0 rgba(255,255,255,.22), 0 0 50px rgba(142,203,255,.14)`, `padding: 46px 38px`. Header `RIFT CLOSED // PAYLOAD SECURED` with blinking amber dot; reward name Chakra Petch 44px/700 in `#ffffff`.

**Right rail** (`flex: 1 1 262px; max-width: 302px`, sticky `top: 84px`):
- `TARGET INFORMATION` panel — the reward's **short name**, its **full effect text** (the one place it appears), category, a compact **Relic card** when the target is a relic, progress bar (width = current step ÷ steps, full on the claim; no percentage label), and a `RETARGET` button carrying two ambient animations: `retGlow 7s ease-in-out infinite` on the button and a `retSwipe 7s ease-in-out infinite` sheen sweep overlay.
- Radar widget, `height: 186px` — decoration only (no step number since audit step 4): concentric rings, 152px solid, 114px dashed amber spinning `24s`, 74px cyan counter-spinning `9s`, and a small blinking amber dot at the centre.
- `MISSION PARAMETERS` panel — requirement text, restriction line.

Footer buttons: `‹ PREV` (ghost, disabled at step 0) / `NEXT STEP ›` (primary) → becomes `◆ CLAIM REWARD ›` on the last step → `RETURN TO RIFT INDEX ›` on the final card. Trace counter right-aligned.

## 9. Dig site detail

Container as the rift detail (`max-width: 1180px; padding: 40px 34px 110px`, 16px sides on phones). Top to bottom:

**a. Header.**
- Back button + monitor toggle (11px labels).
- Eyebrow `{GROUP LABEL} // {n} PHASES` in teal. This replaced "DIG SITE LOCKED", which read as "you can't access this".
- `<h1>` Chakra Petch `clamp(30px, 6vw, 44px)`/700.
- A stat run of 11px mono labels over 12px values: PHASES, GROUP, SYSTEM (if any), DLC (only when not the base game), PRECURSOR (if any).
- Right: a `REQUIREMENTS` panel (`.rf-panel`) with the requirement, the restriction in amber with `⚠`, and notes. All 12px / `line-height: 1.7`.

**b. Relic card** (only when the site gives a relic). See **Relic card** below. The eyebrow reads `◆ RELIC · PHASE {n}`. When the relic comes through a choice or a fight rather than finishing the phase, one line says so: "Through a choice in phase 6: … ; or …" (Planetary Machinery), "Phase 5: awakens Shard, a guardian…" (Kleptomaniac Rats).

**c. Headline outcomes.** `HEADLINE OUTCOMES`: up to 4 payouts ranked by type with the same ranking as the list's yields, not list order.
- The relic is left out because it has its card, and so are risks and duplicates.
- Items sit in a `repeat(auto-fill, minmax(min(260px,100%),1fr))` grid.
- Each item has a type chip (`TECHNOLOGY`, `SPECIMEN`…, plus `· ONE OPTION` when it is one side of a choice), `PHASE n`, and the payout's main text at 13px. Conditions are dropped here; the timeline shows them.

**d. Phase timeline.** One `.rf-tl` glass panel, one `.rf-ph` row per phase. Rows are a two-column grid: a `PH 01` label (11px teal mono, 58px column) and a body sized to its content, so there are no equal-height cards and no progress bars. On phones the rows stack. Body items keep the source order:

- **Guaranteed payouts**: plain 13px lines.
  - A condition moves into 12px `#8ba7bf` secondary text on its own line under the payout. That means a parenthetical that mentions `without / if / unless / only / instead / closed / blocked / requires / needs / when / otherwise`, or a trailing "— instead if …".
  - Clamp brackets such as `(50 / 150 / 250 by game stage)` stay in the main line.
- **Risks** are amber (`#ffc79a`, prefixed `⚠`): penalty-typed rewards, plus scientist deaths, losses, hostile spawns, and the Maniacal / Paranoid / Maimed / Traumatized traits.
- **The relic's line** is warm white with an amber `◆`.
- **Option groups** (`chapter.choices[]`) use the reader's option styling: cyan-bordered boxes, a mono key column, and wrapping text. Options wrap freely, so a label of about 150 characters is fine at 390px.
  - `choice`: header `PICK ONE`, options keyed `PICK` / `OR`. These are real `<button aria-pressed>` elements. Picking one highlights it and dims the rest, and picking it again clears it. The pick is session-only.
  - `random`: header `RANDOM — THE GAME PICKS ONE`, keyed `ROLL` / `OR`, dashed and not interactive, because the player doesn't choose.
  - `either`: header `ONE OF THESE`, keyed `EITHER` / `OR`, not interactive.
  - A labelled option ("proceed cautiously") shows the label, with its payout as secondary text.

**e. Unlocks.** For each `site.unlocks` entry, a `UNLOCKS → {site}` link button (teal outline) that opens that site. Targets that aren't dig sites render as a dashed, non-interactive chip.

**f. How digs work.** A collapsed `HOW DIGS WORK` button (`aria-expanded`, caret rotates). It opens a 3-column table: ROLL / RESULT / XP. The table is CSS grid with `role="table"`, not a `<table>`, because the template runtime can't put loops inside `<tbody>`.

| Roll | Result | XP |
|---|---|---|
| 14+ | Completes the phase | 75 |
| 11–13 | 2 clues toward the next roll | 40 |
| 6–10 | 1 clue | 25 |
| 5 or less | Risks a mishap event | 10 |

Under the table: the "6x" glossary line from `mechanics[]` in warm white, then the remaining mechanics lines (site requirements, deposit chance, mishap outcomes) at 12px.

### Relic card

One component (`.rf-relic`), used in three places: the dig detail page, a rift's reward cards (compact) and the step reader's `TARGET INFORMATION` panel (compact). It reads `reward.relic` and never needs the catalogue lookup.

```
◆ RELIC · PHASE 4                    ← eyebrow, 11px mono .2em #ffd9b0 (rifts: ◆ RELIC · {CATEGORY})
Crystal of Odryskia                  ← Chakra Petch 24px/600 #fff3e4 (17px compact; hidden where the card already names it)
Through a choice in phase 6: …       ← optional one-line route, 12px #f0d7b8
PASSIVE              TRIUMPH         ← 11px mono labels #b9a58c; two columns ≥ 480px, one column compact
▸ +15% Monthly…      ▸ 60 months…    ← 12px list, amber ▸ bullets
───────────────────────────────────  ← rgba(255,217,176,.22)
COST          COOLDOWN
3,000 Unity   3,600 days (10 years)  ← 12px #fff3e4; years = days / 360 (a Stellaris year)
```

- **Shell:** `border-radius: 16px` (13px compact); `border: 1px solid rgba(255,217,176,.48)`; `background: linear-gradient(160deg, rgba(255,206,150,.14), rgba(6,16,28,.58) 62%)`; the same blur as the other glass.
- **Cost and cooldown:** cost is `relic.triumphCost`, or "Cannot be activated" when `activatable` is false. When `cooldownDays` is null, cooldown reads "None — cannot be activated".
- **No catalogue entry** (`reward.relic === null`, e.g. The Advisor's Advisor Core): the card shows its eyebrow and the line "Not on the wiki's Relics page, so its effects aren't documented." It shows no effect lists.

### Data fields used

| Screen | Fields |
|---|---|
| Dig list | `DIG_DATA.sites[].{name, group, dlc, chapters.length}`, `DIG_DATA.groups[]`, `DIG_DATA.rewards[].{site, cat, type, raw, relic.name}` |
| Dig detail | `site.{groupLabel, system, dlc, precursor, req, restrict, notes, unlocks[]}`; per chapter `rewards[]` (display text), `raw[]` (matching only, never shown), `guaranteed[]`, `choices[].{kind, options[].{label, payouts[], line}}`; rewards `{chapter, type, text, raw, relic, relicId}`; `mechanics[]` |
| Rift reward cards, reader | `RIFT_DATA.rewards[].{type, relic, relicNote}` |
| Header stats | `RIFT_DATA.counts` |

## 10. Footer (fixed)

```css
position: fixed; left: 0; right: 0; bottom: 0; z-index: 880;
height: 34px; padding: 0 34px;
display: flex; align-items: center; gap: 16px;
border-top: 1px solid rgba(176,214,255,.12);
background: rgba(4,10,20,.55);
backdrop-filter: blur(16px) saturate(140%);
font-size: 9px; letter-spacing: .18em; color: #7f9cb4;
```

Left: `ASTRAL PLANES // RIFT NAVIGATION HOLO v5.0`. Right: context status — `GALACTIC MAP // IDLE` → `BROWSING ASTRAL RIFTS` → `RIFT: {NAME}` → `TARGET: {REWARD}` / `DIG SITE: {NAME}`.

---

# State

```ts
{
  // navigation
  browse:   null | 'rift' | 'dig'   // which index is open
  rift:     string | null           // selected rift name
  dig:      string | null           // selected dig site name
  reward:   number | null           // index into the rift's reward list
  cur:      number                  // current step index; === steps.length means the final card
  railOpen: Record<string|number, boolean>

  // filtering
  q:        string                  // search query
  cat:      string                  // 'ALL' or a category name
  catOpen:  boolean

  // monitoring
  monitored: Array<{ type: 'rift'|'dig', name: string }>
  progress:  Record<`${type}:${name}`, { reward, cur, railOpen }>
  monMenuOpen: boolean
  tip: string                       // hovered pin key, `${type}:${name}`
  toastText: string
  toastAdd: boolean

  // chrome
  boot:      number                 // boot sequence tick
  condensed: boolean                // scrolled past threshold
  narrow:    boolean                // viewport < 720px
  monTight:  boolean                // control row wrapped to a second line
  vw:        number
  hudClear:  boolean                // corner HUDs have room (checkHud)
  navOpen:   boolean                // phone menu (Camera, Classic/Holo) open

  // camera (dev tool). Saved to localStorage 'rf-holo-cam-v2'; the key changes whenever CAM0
  // changes so old saved views don't override the new default (CAM0 is PRESET 1)
  cam: object | null
  ctlOpen: boolean
  presetName: string
  presets: Array<{ name, cam }> | null
  copied: boolean
}
```

## Path parsing — the core logic

Each reward carries a `path` string such as:

```
Chapter 1 "Investigate the signal" -> Chapter 2-A "Send a probe" -> Chapter 4
```

`parsePath` splits on `->`, and per segment extracts a chapter id (matching `[0-9]+(-[A-Za-z])?`), a quoted choice, and any trailing prose. `steps()` then resolves each segment against the rift's chapter data:

1. Find the chapter by id.
2. Find the choice by exact text; fall back to a case-insensitive prefix match on the first 18 characters.
3. If there is still no match and the chapter has exactly one choice, use it.
4. Everything else in that chapter becomes `alts` (the DO NOT SELECT list).
5. When no choice is specified: if the chapter ends the rift → `"No option to pick — this event closes the rift"`, else → `"Any option — just reach this event"` and `anyRoute = true`.

**Branch detection:** reward and chapter reward strings sometimes lead with a branch name (`Voidspawn + something: …`). `branchOf` extracts a leading capitalized phrase followed by `+`, `base`, or `route`. Reward lines belonging to a branch the player is not on are filtered out.

**Text cleaning** (`clean`) rewrites chapter references into player-facing prose, because raw data leaks internal ids:

| Pattern | Replacement |
|---|---|
| `(sets you on the X branch)` | removed |
| `chapters 4/5 by any route` | `this step is reachable by any route` |
| `from/via/at chapter 4` | `from an earlier step` |
| bare `chapter 4` / `chapters 4, 5` | `an earlier step` |
| `4-A` style ids | `{route name} route` or `the other route` |

`rewardLine` strips leading chapter prefixes, converts `X + condition: body` into `Only if you gave {condition} — {body}`, and drops any line identical to the target reward name.

---

# Design tokens

## Color

| Token | Value | Use |
|---|---|---|
| Void | `#040a14` | Page background |
| Ink | `#e8f2fb` | Body text |
| Ink bright | `#f6fbff` | Headings |
| Ink white | `#ffffff` | Choice text, final reward name |
| Cyan | `#8ecbff` | Primary accent, eyebrows, rift dot |
| Cyan light | `#d6ecff` | Link hover, bar gradient end |
| Cyan pale | `#a8d8ff` | Choice callout label |
| Teal | `#7fe0d4` | Dig-site accent |
| Teal pale | `#dffaf5` | Active phase number |
| Amber | `#ffd9b0` | Selection, monitoring, secondary accent |
| Amber warm | `#ffb87a` | Warnings, clear actions, destructive |
| Amber soft | `#ffc79a` | Warning body text |
| Amber cream | `#fff8ef` | Text on amber surfaces |
| Amber deep | `#ffe6c8` | Retarget button label |
| Muted 1 | `#cfe0ef` | Secondary body |
| Muted 2 | `#a8c4dc` | Labels |
| Muted 3 | `#8ba7bf` | Tertiary |
| Muted 4 | `#7f9cb4` / `#7fa3c0` | Quaternary |
| Muted 5 | `#6f8ea6` | Codes, faint meta |
| Muted 6 | `#5a7893` | Placeholder, unpicked marks |
| Disabled | `#4f6a80` | Disabled button text |

Recurring alpha values:

```
rgba(176,214,255, .1 / .12 / .14 / .16 / .18 / .2 / .22 / .24 / .26 / .3 / .34)   cool hairlines
rgba(174,225,255, .3 / .34 / .4 / .42 / .45 / .5 / .6 / .62 / .7 / .8 / .9)        bright cyan edges
rgba(255,224,190, .34 / .4 / .44 / .5 / .55 / .6 / .62 / .7 / .75 / .8 / .85 / .95) amber edges
rgba(255,214,170, .16 / .2 / .22 / .24 / .26 / .28 / .3)                            amber fills
rgba(255,255,255, .1 → .3)                                                          inset top highlights
rgba(0,6,16, .34 → .6)                                                              drop shadows
```

## Glass recipe

Every panel is a variation on:

```css
background: linear-gradient(160deg, rgba(22,48,74,.42), rgba(6,16,28,.5));
backdrop-filter: blur(20px) saturate(140%);
-webkit-backdrop-filter: blur(20px) saturate(140%);
border: 1px solid rgba(176,214,255,.2);
box-shadow: 0 18px 50px rgba(0,6,16,.4), inset 0 1px 0 rgba(255,255,255,.13);
```

Blur scales with elevation: `16px` (footer) → `18px` (buttons, chips) → `20px` (cards) → `22px` (reward cards) → `26px` (modals, compact bar). Gradient angle is `160deg` on most panels, `155deg` on reward/phase cards, `165deg` on the step card.

## Accessibility and polish (audit step 4)

These rules override any smaller or older figure elsewhere in this document.

**Type minimums (P2).**
- **Uppercase mono labels:** 11px minimum.
- **Reading text:** 12px minimum for anything the player reads, including counts, costs, conditions, requirements, choice text and search result names.
- **Decoration only:** the SIG / ARC / RWD codes, the corner HUD and the dial's `RIFT TRACE ACTIVE` stay at 8–9px.

**Keyboard (P4).**
- **Real buttons:** the home Astral Rifts and Dig Sites tiles, the Rifts / Dig sites toggle (`aria-pressed`), the reward filter trigger (`aria-expanded`) and its options, Prev / Next / claim, Retarget, Abort and Monitor.
- **`role="button"` with Enter / Space (`onActivate`):** reward cards on a rift, event-log rows, the event log's claim row, search results and the monitoring tabs.
- **Focus style:** every focusable control shows `outline: 2px solid #8ecbff; outline-offset: 2px` on `:focus-visible`. The folder card keeps its own focus treatment (the 2px cyan outline stroke), and nothing else uses `outline: none` without a replacement.
- **Verified:** home → rift → reward → every step → claim, using only Tab, Enter and Space.

**Overlays (P5).** Surfaces that sit over other content are near-opaque; cards keep their glass.

| Surface | Background | Blur |
|---|---|---|
| Top bar | `rgba(9,21,36,.95)` → `rgba(6,14,26,.93)` | 30px |
| Footer | `rgba(6,14,26,.94)` | 30px |
| Compact bar | `.96` → `.94` | 30px |
| Search dropdown, filter menu, monitoring menus | `.98` → `.985` | 30px |

The dropdowns and menus sit inside animated ancestors that stop `backdrop-filter` from rendering. That's why they're more opaque than the others: at 95%, bright card text still showed through them unblurred.

**One progress counter (U1).**
- `STEP n OF m` by the step title is the only count, and the claim step isn't counted.
- The target card's progress bar matches it and fills on the claim.
- `TRACE n/m`, the `PROGRESS n%` label and the dial's `01 OF 03` are gone.

**Short reward names (U2).**
- **Short name:** headings, reward cards, the event log's claim row, the final card and the footer use `reward.short`, the generated heading-length name (60 characters maximum).
- **Full effect text:** `reward.effect` appears once, in the target card.
- **Dig options:** the heading is the option's `short`, and the rest of its text is secondary.
- **Duplicate cost:** a bare amount a path appends after a choice (`· (-100 threads)`) is dropped when the choice's own note already carries `cost:`.

**Short names are names (U2, follow-up).**
- **Generated names:** a reward's short name is generated from its data.
- **Hand-written names:** where the generated name would be a truncation ("…") or run over 40 characters, it comes from `data/overrides/reward_names.json` instead, reviewed by hand (119 names).
- **No chapter references:** "at chapter N" is wiki jargon and is stripped from the short names and effect text the UI shows. It stays in the data.
- **Headline outcomes:** these use short names too. A conditional item carries `· CONDITIONAL` on its chip, so the condition isn't lost.

**One card per reward (N1).**
- **Grouping:** the same reward reachable by several routes (same short name and type on one rift) is one card, with meta `N ROUTES · SHORTEST n STEPS`.
- **Reader:** opens the shortest route.
- **Counts and search:** rift card counts and search results use the same grouping, so Celestial Tear appears once, not three times.

**Rift count (N2).** One definition everywhere, `32 RIFTS · 4 SITUATIONS` (`riftCountText()`), used in:
- the top bar;
- the index subtitle (`AWAITING QUERY // 32 RIFTS · 4 SITUATIONS · 110 DIG SITES`);
- the browse subtitle (`SCAN COMPLETE // … IN RANGE`, counting the filtered list);
- the home tile.

**DLC label (N3).** On dig cards, DLC is muted text, `DLC · Ancient Relics` (11px mono, `#6f8ea6`, no outline), pushed right. It's hidden for the base game. It no longer looks like a yield chip.

**Headline ranking (N4).** Unconditional payouts rank above conditional ones ("if you have…", "if…", "only…", "unless…", or `conditional` in the data). Ties break by type ranking.

**Footer (B3, P5, follow-up).**
- **768–1023px:** the footer shows `RIFT NAV // HOLO v5.0` instead of the long product string. The target text takes the remaining width and truncates with an ellipsis.
- **Phones:** the footer is solid `#08131f`.

**Touch and names (P3, P4, follow-up).**
- **Toggle:** on touch screens the Rifts / Dig sites toggle buttons are at least 44px tall.
- **Back button:** the compact bar's `‹` is labelled "Back to galaxy". Every button now has an accessible name.

**Filter (U4).**
- **Reward types only:** the rift filter lists reward types only (no Warnings, Other or Unlocks); the dig filter drops Risks and Other.
- **Card counts:** rift cards count real rewards (`N REWARDS`). A rift with none shows what it leads to (`LEADS TO …`, from `unlocks` or its follow-up rewards), else `NO REWARD`, never `0 REWARDS`. No rift in the current data needs the fallback.

**Labels (U5).** The rift eyebrow is `{GROUP} RIFT` or `RIFT SITUATION`. The dig eyebrow is the singular group, e.g. `UNIQUE SYSTEM SITE // 4 PHASES`.

## Typography

Two families, loaded from Google Fonts:

- **Chakra Petch** (400/500/600/700) — display. All headings, card titles, choice text, numerals in the radar and phase badges.
- **IBM Plex Mono** (400/500/600) — everything else. Set on `body`, so it is the default.

| Role | Size / weight / tracking |
|---|---|
| Page h1 | Chakra Petch 44px / 700 / `.04em`–`.1em` |
| Split-column h1 | Chakra Petch 29px / 700 / `.06em` |
| Final reward name | Chakra Petch 44px / 700 / `.01em` |
| Step h2 | Chakra Petch 36px / 700 / `.02em` |
| Reward card title | Chakra Petch 26px / 600 / `.01em` |
| Choice text | Chakra Petch 23px / 500 |
| Browse tile title | Chakra Petch 22px / 600 / `.04em` |
| Rift/dig card title | Chakra Petch 19px / 600 / `.03em` |
| Target panel title | Chakra Petch 17px / 600 |
| Phase payout | Chakra Petch 15px / 500 |
| Claim button | Chakra Petch 14px / 700 / `.18em` |
| Rail step title | Chakra Petch 12px / 600 / `.09em` |
| Body | Plex Mono 11–13px / `line-height: 1.6`–`1.8` |
| Label | Plex Mono 10px / `.2em`–`.22em` |
| Micro label | Plex Mono 9px / `.2em`–`.24em` |
| Nano label | Plex Mono 8px / `.2em`–`.24em` |

Nearly every uppercase label carries wide tracking (`.12em`–`.24em`). This is load-bearing for the console aesthetic — do not drop it.

## Spacing

Page padding `34px` horizontal (all breakpoints), `28px`–`40px` top, `96px`–`110px` bottom (clears the fixed footer). Panel padding `14px 16px` (compact card) → `16px 18px` (info panel) → `18px` (rail panel) → `22px 24px` (callout) → `24px` (reward card) → `36px 38px` (step card) → `46px 38px` (final card). Gaps: `2px` (segmented control) · `4px` (menu grid) · `8px` (chips, meta rows) · `10px`–`12px` (control row, card stacks) · `16px`–`18px` (grids) · `20px`–`22px` (notch stack, columns) · `26px` (detail header).

## Radii

`4px` (tab outer corners) · `6px` (badges, pin button) · `7px` (tooltip, monitor tab top) · `8px`–`9px` (small buttons, menu rows) · `10px`–`11px` (buttons, chips, controls) · `12px`–`13px` (rail rows, toast, claim button) · `14px` (cards, panels) · `16px` (reward cards, header panel) · `18px` (step card, boot panel) · `999px` (dots, rings).

## Shadows

```
inset 0 1px 0 rgba(255,255,255,.12 → .3)          top highlight, on nearly every surface
0 10px 30px rgba(0,6,16,.36)                      selected chip
0 12px 34px rgba(0,6,16,.34 → .4)                 small panel / primary button
0 14px 40px rgba(0,6,16,.36 → .4)                 rail row
0 16px 34px rgba(0,6,16,.55)                      compact bar
0 18px 50px rgba(0,6,16,.4)                       card
0 22px 60px rgba(0,6,16,.42 → .6)                 reward card, toast
0 26px 70px rgba(0,6,16,.55 → .6)                 dropdown
0 30px 80px rgba(0,6,16,.5)                       step card
0 30px 90px rgba(0,6,16,.55 → .6)                 boot panel, final card
```

Glow shadows use the accent at low alpha: `0 0 8px` (dots) · `0 0 12px`–`0 0 14px` (small marks) · `0 0 30px`–`0 0 50px` (callout, final card).

## Motion

| Keyframe | Definition | Used on |
|---|---|---|
| `hudIn` | `opacity 0→1`, `translateY(12px)→0` | Detail page enter, toast |
| `hudFade` | `opacity 0→1` | Dropdowns, boot lines, reader enter |
| `blink` | `1 → .28 → 1` | Status dots, boot diamond |
| `spin` / `spinR` | `rotate(±360deg)` | Radar rings |
| `holoScan` | `translateY(-40vh → 120vh)` | Scan band, 11s linear infinite |
| `holoBreath` | `scale(1.04 → 1.09 → 1.04)` | Video backdrop, 40s |
| `retGlow` | box-shadow pulse at 84% of cycle | Retarget button, 7s |
| `retSwipe` | `translateX(-130% → 130%)` at 68–90% | Retarget sheen, 7s |
| `wipeIn` | `opacity 0→1` + `clip-path: inset(-60% 100% -60% -60%)` opening left-to-right + `translateX(-18px)→0` | Card entrances |

Standard easings: `cubic-bezier(.16,.86,.24,1)` for layout motion (`.3s`–`.8s`), `ease` for color/border (`.18s`–`.22s`), `cubic-bezier(.2,.75,.2,1)` for the browse tiles.

```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
```

## Scrollbars

```css
::-webkit-scrollbar { width: 6px; height: 6px }
::-webkit-scrollbar-thumb { background: rgba(176,214,255,.28); border-radius: 9px }
::-webkit-scrollbar-track { background: transparent }
```

---

# Responsive behavior

Desktop layout is set by inline styles. The responsive rules live in one block of classed `@media` rules at the end of the helmet `<style>` (search for "Responsive (audit"). Verified at 1440×900, 1180×820, 820×1180, 390×844 and 360×740. At all five sizes there is no horizontal scroll, nothing is clipped at the right edge, no panel draws over another while scrolling, the footer never covers content, and the corner HUD never covers a card.

| Breakpoint | Behavior |
|---|---|
| `< 1090px` | **Step reader stacks** (`.rf-read`). The Event Log and Target/Mission columns go `position: static`, so nothing stays pinned. Order: step card and Prev/Next, then event log, then target information and mission parameters (radar last). The event log's inner scroll is removed so the page scrolls as one. The breakpoint is where the three columns (246 + 470 + 262px plus gaps and padding) stop fitting side by side. Above it the desktop layout is unchanged. |
| `< 1024px` | **Notched split browse column** (`.rf-home-notch`) goes full width: `width: 100%; max-width: 960px` (cards and header stay within 320–920px), centred, 20px side padding. The top bar's stats are hidden. |
| `< 768px` | **Top bar:** 16px padding, near-opaque background. Stats and `GUIDE ONLINE` are hidden. Camera and Classic/Holo move into one ☰ menu button at the right (`.rf-top-menu`, popover `.rf-nav-pop`). `RIFT NAV` never wraps. |
| `< 768px` | **Footer:** one short line, `RIFT NAV // HOLO v5.0`, on the same background as the top bar. The status text is hidden. `.rf-scroll` gets `padding-bottom: 34px` (the footer height). |
| `< 768px` | **Compact bar:** back button, search (takes the remaining width, `min-width: 120px`) and the reward filter collapsed to a funnel icon with its count. The Rifts/Dig sites toggle and the Monitoring label are dropped from the bar; the toggle is still in the header. |
| `< 768px` | Detail pages (`.rf-main`) use 16px side padding. Grid minimums use `minmax(min(Npx, 100%), 1fr)`, so a single column can shrink below its desktop minimum. |
| `< 768px` | Corner HUDs hidden. |
| `< 720px` | `narrow = true`. Monitoring strip → dropdown. Search field drops its `min-width: 160px`. |
| All sizes | **Footer** stays on one line; a long target name is truncated with an ellipsis rather than wrapped. |
| All sizes | **Compact bar** only on the browse lists (`browse` set, no rift or dig site open), never on the rift, reader or dig detail screens. |
| Control row wraps to a second line | `monTight = true`, monitoring dropdown hides its text label and keeps only the count. Measured with a `ResizeObserver` checking whether children share an `offsetTop`. Requires ~90px of recovered width before reverting (hysteresis). |
| Scroll > 130px / < 90px | Compact bar in / out. |
| `pointer: coarse` | **Touch targets** are at least 44px tall: the Rifts/Dig sites toggle (options side by side), Classic/Holo, Camera, the menu button, back buttons, filter buttons, the compact bar controls and the + monitor buttons. |

---

# Data

Two global data files, loaded as plain scripts.

**`rift-data.js`** → `window.RIFT_DATA`

```ts
{
  rifts: Array<{
    name: string
    group?: string
    req?: string
    restrict?: string
    chapters: Array<{
      id: string                    // '1', '2-A', …
      title: string
      ends?: boolean
      rewards: string[]
      choices: Array<{ text: string, to?: string, diff?: number, note?: string }>
    }>
  }>
  rewards: Array<{
    rift: string                    // FK → rifts[].name
    name: string
    cat?: string                    // drives the filter
    path: string                    // 'Chapter 1 "…" -> Chapter 2-A "…"'
  }>
}
```

**`dig-data.js`** → `window.DIG_DATA`

```ts
{
  sites: Array<{
    name: string
    groupLabel?: string
    dlc?: string
    precursor?: string
    req?: string
    restrict?: string
    notes?: string
    chapters: Array<{ id: string, rewards: string[] }>
  }>
  rewards: Array<{ site: string, name: string, cat?: string, chapter?: string }>
  mechanics: string[]
  groups: string[]
}
```

Source: the Stellaris wiki and in-game data, compiled in `uploads/Archaeological Sites - Complete Site, Requirement & Reward Reference.md`.

---

# Assets

| Asset | Notes |
|---|---|
| Chakra Petch, IBM Plex Mono | Google Fonts, weights listed above |
| `galaxy-map.js` | Self-contained procedural starfield web component. Props: `mode` (`galaxy`/`rift`/`dig`), `speed`, `pitch`, `dist`, `ang`, `zoom`, `xoff`, `yoff`, `glow`, `core`. Renders to canvas — port as-is or substitute an equivalent background. |
| `uploads/bg-scene-1.mp4` | Optional video backdrop. Not bundled (large); swap for your own footage or drop the Video option. |

No icons or image assets — every glyph is a Unicode character (`✚ ⦿ ✕ ◆ ◇ ▸ ▪ ‹ › ▾ ◎ ✦ ⚠ ›`) and every graphic element is CSS.

---

# Files in this bundle

| File | What it is |
|---|---|
| `Rift Finder Holo.dc.html` | **Primary reference.** Contains all three layouts and all three filter UIs. The `Component` class at the bottom holds every computed style and all state logic. |
| `Rift Finder Split.dc.html` | Standalone split-column build, for reference |
| `rift-data.js` | Astral rift dataset |
| `dig-data.js` | Dig site dataset |
| `galaxy-map.js` | Animated backdrop component |
| `support.js` | Prototype runtime — **scaffolding, not design.** Ignore when porting. |

## Screenshots

`screenshots/` holds one capture per variant, all taken on the rift browse screen:

| File | `layout` | `filterUI` |
|---|---|---|
| `layout-grid--filter-menu.png` | Grid | Menu |
| `layout-grid--filter-one-line.png` | Grid | One line |
| `layout-grid--filter-chips.png` | Grid | Chips |
| `layout-split-column--filter-menu.png` | Split column | Menu |
| `layout-notched-split--filter-menu.png` | Notched split | Menu |

The filter variants are shown against Grid because `filterUI` renders identically in all three layouts. The two split layouts are shown with Menu so the column geometry and the notched folder silhouette read clearly against the galaxy backdrop.

**Dig redesign (audit step 3)**: `audit3--{scene}--{width}x{height}.png`, Notched split, at 1440×900, 1180×820, 820×1180 and 390×844 (phone sizes with touch emulation):

| Scene | Shows |
|---|---|
| `dig-list-relics` | dig list with the Relics filter on (10 sites under section headings, amber relic chips) |
| `dig-debris-belt` | dig detail: relic card, risk and relic lines in the timeline |
| `dig-ancient-facility-phase3` | phase 3's PICK / OR pair with one option picked, conditions as secondary text |
| `rift-relic-reward` | Subnautical's reward cards with the compact relic card |

To view a prototype: open the `.dc.html` file directly in a browser. Both are self-contained apart from the sibling `.js` files.

## Where to find things in the source

| What | Where |
|---|---|
| Layout switching | `renderVals()` → `lay`, `split`, `notch`, then `homeWrap`, `cardGrid`, `browseGrid`, `cardShell`, `titleStyle` |
| Card notch geometry | `.rf-fc*` rules at the end of the helmet `<style>`; `folderPath()`, `frameRef()`/`bindFrame()`/`buildFrame()`/`drawFrame()` methods; `notchCards`/`plainCards` in `renderVals()` |
| Header notch geometry | Same `.rf-fc-*` layers as the card; `headNotch`/`headFrameRef` in `renderVals()`, padding and width in `stickyWrap` |
| Filter UI switching | `catItem()` method; `filterMenu`/`filterScroll`/`filterChips`, `catChips`/`catStrip`/`catRows` |
| Path resolution | `parsePath()`, `steps()` |
| Copy cleanup | `clean()`, `rewardLine()`, `dispName()`, `branchOf()` |
| Scroll condense | `bindScroll()` |
| Control row wrap detection | `bindCtl()` |
| Monitoring | `isMon()`, `toggleMon()`, `monTab()`, `pinRail()`, `pinBtn()`, `monBtn()` |
| Button styles | `glassBtn()`, `claimBtn()` |
