# Session — Reward Ledger, V2 Two-tone (rift detail reward list)

**Date:** 2026-10-24
**Surface:** Claude Code (desktop app), editing `design_handoff_rift_finder/Rift Finder Holo.dc.html`
**Status at close:** built, verified and pushed to the `reward-ledger` branch (`f2ff18e`, `454adfc`);
**not merged**. The decision to use the ledger is recorded below.

## What we set out to do

Run `docs/prompts/2026-10-24-reward-ledger-v2.md`: replace the rift detail's "SELECT TARGET REWARD"
card grid with the grouped "Reward Ledger" in its V2 Two-tone colour treatment.

## What actually changed

- **Ledger** (`f2ff18e`, which also commits the prompt file):
  - **Grouping:** rewards are grouped by a derived domain, in this order: Economy, Rift ops,
    Military, Defense, Fleet, Species & pops, Leaders, Unlocks, Other.
  - **Rows** run icon tile · title · cost or note · faction chip · steps + 5 roll pips · chevron.
    Each row keeps the old card's `role="button"`, click, keyboard and aria-label.
  - **Relic rewards** keep the compact relic card under the title.
  - **Icons switch:** an ICONS switch (state `ledgerIcons`, `localStorage['rf-ledger-icons']`)
    hides the tiles.
  - **Phones, touch tablets and widths ≤ 640px:** the chip and meta drop to a second line.
  - **Colour:** two hues only, as CSS variables `--ldg-*`. Blue is structure; warm is cost or
    roll ≥ 5.
  - **Removed:** the `RWD-###` code.
- **Derived at render time, with no data edits:**
  - **Tables:** the domain rules (`LEDGER_CAT`, `LEDGER_KEYWORDS`, `LEDGER_ICON`, next to
    `TYPE_SHORT`).
  - **Helpers:** `ledgerDomain`, `ledgerCost` (parses `cost:` along the route; joins with " + ";
    "food / minerals / energy" becomes "res" when there are 2+ costs) and `ledgerFaction`.
- **Deviations from the prompt, deliberate:**
  - **Faction:** it reads the reward's own label first ("Starlight Vanguard + alloys"), then the
    last route step whose choice *or chapter title* names a faction. Choice text alone mislabels
    the armor and shield rewards as Black Curtain, because their computed routes pass through
    "Visit the Black Curtain" before reaching the Starlight Vanguard chapter.
  - **Title rule:** it also treats "… offering bonus" as a route label (two Ruined Planet rows).
  - **Notes:** a note is dropped when it only restates the title (Symbiotic Fruit).
  - **Glass blur:** rows get a 14px glass blur (colours unchanged), so faction chips stay legible
    over the galaxy sphere.
- **Screenshots and README** (`454adfc`):
  - **Screenshots:** 24 PNGs in `design_handoff_rift_finder/screenshots/`, named
    `ledger--{ruined-planet,the-microverse,the-garden}--{390x844,820x1180,1180x820,1440x900}[--noicons]`.
  - **README:** §7 now documents the ledger.
- **Verified** headless in Chrome at all four sizes:
  - The count label matches the row count (19, 2, 5).
  - No horizontal scroll at 390.
  - Tab from the switch lands on the first row with the 2px cyan ring, and Enter opens its step
    view (STEP 1 OF 4).
  - The icons switch works.
  - No page errors.
- **Data:** no data changed. `data/*.json`, `rift-data.js` and `dig-data.js` are untouched, so
  there was nothing to rebuild or validate.
- **Figma:** the MCP wasn't authorised, so the Figma panel wasn't consulted. The web mock (artifact
  `9ZXKeVAY5fQJPtC9nXKiZT`, V2) was the visual reference, and its icon set was reused.

## Decisions made

"Reward section uses the Ledger, V2 Two-tone", in `docs/DECISIONS.md`.

## What's still open (out of scope, reported, not changed)

1. **Chapter 7 restatement rows on Ruined Planet look like duplicates.** They're unconfirmed
   whether they stack, so all rows were left in:
   - "Black Curtain + resources" (+0.5 basic resource from the matching job category) ≈
     "+0.5 basic resource per job"
   - "Black Curtain + astral threads" ≈ "+25% rift speed, −50% fail chance"
   - "Starlight Vanguard + alloys" ≈ "+10% armor HP and hardening"
   - "Starlight Vanguard + astral threads" ≈ "+10% shield HP and hardening"
   - "Astral threads offering bonus" (+5% sublight speed) ≈ "+5% Sublight Speed"
   - "Energy offering bonus" (+5% ship build speed) ≈ "+5% Ship Build Speed"

   Only "Black Curtain base" and "Starlight Vanguard base" are distinct chapter 7 rewards.
2. **Ruined Planet's chapter 7 rows all carry the "Recruit scientist" route** (`pathSource:
   computed`). Their steps (6) and costs ("1,000 res + 100 astral threads") come from that one
   route, so they're likely wrong. "Starlight Vanguard base" sits on a Black Curtain route. Its
   faction chip is still right, because the label wins. Not patched.
3. **Dig site detail** (headline outcomes + phase timeline) wasn't changed.
   - **Where the ledger could go:** it could replace the four-item "Headline outcomes" block.
   - **Where it can't:** the phase timeline is the core of that screen, and dig rewards are
     per-phase lines with PICK / OR choices.
   - **What it would need:** specimens and relics would all land in "Other". The ledger would need
     Specimens, Relics and Technology as domains first.
4. **`Rift Finder Split.dc.html`** still has its own copy of the old grid (left alone).
5. **Merge order (corrected the same day):** `reward-ledger` was first cut from `main`, so the
   preview lost the inline-detail side list and panel. The ledger was only meant to replace the
   cards, so `inline-detail` was merged into `reward-ledger` (`e4e0247`). The branch now holds
   inline detail plus the ledger inside its panel, and the desktop screenshots show that view.
   Merging `reward-ledger` therefore brings inline detail with it.
6. **Untracked folder:** `reference/_graphics/resources/` was untracked in the working copy
   before this session; it isn't part of this work and wasn't committed.

## Next three things

1. Review the ledger screenshots, or the preview (pane wider than 1024px), and merge
   `reward-ledger`.
2. Decide on the Ruined Planet chapter 7 duplicates and fix its computed chapter 7 paths in the
   data.
3. Pick between `split-tabs` and `inline-detail`, then merge it on top of the ledger.

## Links

- Prompt: `docs/prompts/2026-10-24-reward-ledger-v2.md` (on the `reward-ledger` branch)
- Figma: https://www.figma.com/design/1MdYxgxTFL90Cp1HXiBwAz/Rift-Helper-UI?node-id=97-449
- Ledger Color Variations (web mock): https://claude.ai/artifact/9ZXKeVAY5fQJPtC9nXKiZT
- Branch: https://github.com/nightowl-83/RiftNav/tree/reward-ledger

---

# Later the same day: inline detail refinement rounds 3–6, then live

**Status at close:** `reward-ledger` merged into `main` (`8012e8e`) and pushed, so the Cloudflare
Pages production site now serves inline detail plus the Reward Ledger. The deploy itself wasn't
checked: `gh` isn't installed here, and the site is password-gated.

## What we set out to do

Mike reviewed the branch in the preview and sent four more rounds of edits, then asked for the build
to go live. Every round is written up in `design_handoff_rift_finder/README.md` under "Inline detail"
(Round 3 through Round 6).

## What actually changed

- **Round 3** (`fa0e3a7`, screenshots fixed in `12249b1`):
  - A sticky "Rift Index" title row.
  - « / » double-arrow icons.
  - Header buttons all 38px tall.
  - A fading folder container.
  - The ICONS switch removed, with tiles at half opacity.
  - A full-width reader bar (Abort / step / Prev / Next) above the footer.
  - Mission parameters moved into the requirements sheet.
  - The radar removed.
  - "Retarget" renamed "Change target".
  - The compact bar's back button gained an arrow and a "BACK" label.
  - The footer halved.
- **Fade fix** (`f462fdf`). The first fade masked the folder outline directly. Its stroke sits
  half a pixel outside the box, so the border disappeared entirely, and Mike called it out. The
  outline, notch bar and shadow now sit in `.rf-inl-fade` wrappers that extend 80px past the panel.
  The top 30% was checked pixel-identical.
- **Round 4** (`c9557ec`):
  - The detail and reader cards (`.rf-cardx`) lost their coloured corner brackets and took the
    folder's border and fill instead.
  - The reader's three columns start on one line.
  - Footer at 14px.
  - GUIDE ONLINE hides below 1140px, because it overflowed at 1024.
- **Round 5** (`b4f0a1e`):
  - The footer gained 4px of padding top and bottom.
  - The browse header became three rows: title; the toggle with Monitoring; search with the filter.
  - The monitoring tabs now sit as a fixed strip under the compact bar. They had been hidden
    behind it.
  - The reward-type menu is a root-level popover beside its trigger, or the filter sheet when it
    won't fit.
  - The step card fades like the folder.
  - The Rift Index row is a single button and only gets a background once stuck.
  - The panel's » appears only while the list is hidden.
- **Round 6** (`af10113`):
  - Search takes the spare width, and the filter label shortens: ALL REWARD TYPES, then
    ALL REWARDS, then ALL.
  - Both query fields got search icons.
  - The monitoring strip shows no scrollbar and gained 8px of top padding.
  - A "SHOW LIST" label sits beside the panel's ».
  - While the list is open, the reader bar spans the viewport minus the list.
  - The phone dock order is now Search, Filter, Monitoring, and the dock has room for the badge.
  - **Collapse flicker:** found by a frame-by-frame screencast. The panel's content re-wrapped on
    every frame, and at 1280 the reader jumped between stacked and three columns partway through
    the slide. The `rfinl` size container moved from the panel to `.rf-inl-scroll`. During the
    slide that element holds the narrower of the two widths, pinned right, so the layout changes
    once.
- **Live:** merged into `main`, with the decision recorded (`174b71e`).
- **Verified:**
  - **Every round:** headless Chrome over CDP from `file://`, at 1440, 1280, 1024 and 390, with no
    page errors.
  - **Folder graphics:** `folderPath`, `frameRef`, `bindFrame`, `buildFrame`, `drawFrame` and all
    `.rf-fc*` rules are identical to `main` before the merge.
  - **Screenshots:** the 12 ledger screenshots were regenerated after each visual round. The
    `--noicons` set was removed along with the switch.
- **Data:** none changed. No `data/*.json`, `rift-data.js` or `dig-data.js` edits, so there was
  nothing to rebuild or validate.

## Decisions made

"Inline detail and the Reward Ledger ship to the live site" in `docs/DECISIONS.md`. It supersedes
the 2026-10-06 "experiments stay on branches" entry for inline detail.

## What's still open

1. **The live deploy wasn't confirmed.** Open the site and hard-refresh.
2. **Collapse flicker:** if a flash of the folder itself (not the content) remains, the next
   suspect is the fill's `backdrop-filter` combined with its mask while the panel resizes.
   Headless capture can't show compositor flicker.
3. **A lighter horizontal band** shows across the list after scrolling in headless screenshots. It
   was also present before round 5. It's probably a headless artifact; check in a real browser.
4. **`split-tabs`** is unmerged and not deleted. Decide whether to drop it now that inline detail
   is live.
5. **Still open from this morning:** the Ruined Planet chapter 7 duplicates and their computed
   routes; the dig site detail has no ledger; `Rift Finder Split.dc.html` still has the old grid.
6. **Untracked folder:** `reference/_graphics/resources/` is still untracked and not part of
   this work.

## Next three things

1. Check the live site after the deploy, at desktop width and on a phone.
2. Decide `split-tabs`: delete it, or keep it as an alternative layout option.
3. Fix the Ruined Planet chapter 7 duplicates and routes in the data, through `build_v3.py`.
