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
