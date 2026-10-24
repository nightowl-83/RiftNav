# Prompt — "Reward Ledger, V2 Two-tone" (for Claude Code)

Written 2026-10-24. Source design: Figma "Rift Helper UI", page "Rewards Ledger", panel
"V2 · Two-tone (recommended)" (https://www.figma.com/design/1MdYxgxTFL90Cp1HXiBwAz/Rift-Helper-UI?node-id=97-449).
Web mock: claude.ai artifact 9ZXKeVAY5fQJPtC9nXKiZT (Ledger Color Variations, V2).
Paste everything below the line into Claude Code.

---

Replace the reward card grid in the rift detail view ("SELECT TARGET REWARD") with a compact,
grouped list, the "Reward Ledger" in its V2 Two-tone color treatment. Work on a new branch.

SETUP
- Run /pick-up first.
- git checkout -b reward-ledger
- File: design_handoff_rift_finder/Rift Finder Holo.dc.html
  - Template: the block that starts at the `SELECT TARGET REWARD // {{ rewardCountLabel }}` label
    (around line 1125) and the `<sc-for list="{{ rewardCards }}">` grid under it.
  - Logic: `rewardCards:` in the Component class (around line 2853) and `rewardGroups(rift)` (around 2137).
- Do NOT edit anything in data/ or the generated *-data.js files. All new fields are derived in the
  Component class at render time.
- If the Figma MCP is connected, look at the source panel above for reference. Styling still comes
  from the existing file's colors and fonts. Don't add new fonts.

WHY
The current cards are ~194px tall, show ~4 per screen, repeat the same category eyebrow on
most cards (13 of 19 on Ruined Planet say "EMPIRE MODIFIERS") and lead with a hash code (RWD-###)
that means nothing to players. The ledger shows the whole list on one screen, leads with the effect,
and groups by what the reward does.

LAYOUT
1. Group rewards by a derived `domain` (see DATA). Groups render in this order and only if
   non-empty: Economy, Rift ops, Military, Defense, Fleet, Species & pops, Leaders, Unlocks,
   then Other.
2. Group header: uppercase label + count, then a 1px rule that fills the rest of the row.
   IBM Plex Mono 11px, letter-spacing .2em. 16px between groups, 8px from header to first row.
3. Reward row: one button per reward, 6px between rows. Keep the existing onClick / onKeyDown /
   aria-label behavior from the current card (r.open, r.key, r.aria).
   Columns, left to right, vertically centered, 14px gap:
   a. Icon tile (34×34, radius 9) with an 18px stroke icon for the domain.
   b. Text block (fills the remaining width, min-width 0):
      - Title: Chakra Petch 600, 17px, line-height 1.2, color #f6fbff.
      - Detail line under it, 12.5px:
        - If the route has a cost: "Costs <cost>" in IBM Plex Mono 400.
        - Otherwise a short note (e.g. "Black Curtain ending") in the body face, color #8ba7bf.
   c. Faction chip: pill, IBM Plex Mono 500 10.5px uppercase, letter-spacing .12em, 1px border.
      Shows the chapter 2 faction route ("BLACK CURTAIN", "STARLIGHT VANGUARD") or "ANY ROUTE".
      Hide the chip entirely for rifts with no faction branch.
   d. Meta: "<n> STEPS" (IBM Plex Mono 500 11px, tabular-nums) + 5 roll pips (6×10px, radius
      1.5, 3px gap). Filled pips = hardest roll on the route, the same value the old card's bar
      used (`hard`). Keep the "N ROUTES · SHORTEST" prefix when g.routes > 1.
   e. A 14px chevron in #5f7d95.
   Row box: padding 10px 14px 10px 10px, radius 11, background rgba(2,8,16,.32),
   border 1px rgba(176,214,255,.08). Hover/focus-visible: background rgba(142,203,255,.06),
   border rgba(142,203,255,.3). Keep the existing visible focus ring.
4. Relic rewards: keep the existing compact relic card (`r.relics` / rf-relic-*) but render it
   inside the row's text block, under the title, so relics still show passive/triumph/cost.
5. Mobile (state.mob) and narrow widths (<= 640px): the icon + text block stay on row 1; the
   faction chip and meta drop to a second line aligned under the text. No horizontal scroll.

COLOR — V2 TWO-TONE (the rule that matters)
Only two hues, both already in the file. Blue means structure. Warm means "this costs you
something or it's hard".
- Blue #8ecbff: group header label; group rule (gradient rgba(142,203,255,.3) → transparent);
  icon stroke; icon tile bg rgba(142,203,255,.08) and border rgba(142,203,255,.22); filled pips
  for roll 1–4.
- Warm: cost text #ffc796; filled pips for roll >= 5 #ffb87a (same threshold the old bar used).
- Neutral: titles #f6fbff; notes, step counts and faction chips #8ba7bf with border
  rgba(176,214,255,.16); empty pips rgba(176,214,255,.14).
- No per-domain colors anywhere. Define these as CSS custom properties in the file's <style>
  block (e.g. --ldg-accent, --ldg-warm…) instead of repeating literals inline.

ICON TOGGLE
- Add state `ledgerIcons` (default true), persisted the same way the file already persists
  other UI prefs (check for an existing localStorage helper and reuse it, wrapped in try/catch).
- Put a small "ICONS" on/off switch at the right end of the SELECT TARGET REWARD label row.
- When off, hide the icon tile and set the row's left padding to 16px. Nothing else changes.

DATA (derived in the Component class, no data-file edits)
- `domain`: map from r.cat plus keyword rules on r.effect / r.short:
  - "Empire modifiers" splits by keyword:
    - "rift" → Rift ops
    - "weapon|damage" → Military
    - "armor|shield|hull" → Defense
    - "sublight|ship build|fleet" → Fleet
    - "resource|job|energy|minerals|food|alloys" → Economy
  - "Paragons & leaders" and "Leader traits" → Leaders.
  - "Species & pops" → Species & pops.
  - "Unlocks", "Situations" and "Systems" → Unlocks.
  - Everything else → Other.
  - Put the rules in one small table near TYPE_SHORT so they're easy to edit.
  - Exclude any text containing "specimen" from keyword matching. This is the same class of bug
    as the old "Relic Rails" false positive.
- Title: use r.short, except when r.short is a route label rather than an effect (matches
  /\bbase$/i or contains " + "). In that case use r.effect.
- Cost: parse "cost: …" from the choice notes along the route the old card already walks
  (this.steps(rift, r)). Join multiple costs with " + ". Shorten "food / minerals / energy" to
  "res" only when there are 2+ costs.
- Faction: from the route step whose choice text mentions "Black Curtain" or "Starlight
  Vanguard". Otherwise "ANY ROUTE" when the rift has a faction branch, else none.
- Remove the RWD-### code from the UI. Leave `this.code()` alone if anything else uses it.

OUT OF SCOPE (report, don't change)
- Deduplicating the chapter 7 restatement rows (e.g. "Black Curtain + astral threads" duplicates
  the +25% rift speed reward). Unconfirmed whether they stack, so leave all rows in. List which
  rows look like duplicates in the session notes.
- The chapter 7 rows on Ruined Planet all carry the "Recruit scientist" path (pathSource:
  computed), so their faction/steps may be wrong. Flag it, don't patch around it.
- Dig site detail uses a different reward layout (digHeadline etc.). Don't change it. Note
  whether the ledger would fit there.
- Rift Finder Split.dc.html has its own copy of the old grid. Leave it.

CHECK
- Screenshot Ruined Planet, plus one linear rift and one rift with a relic reward, at 390×844,
  820×1180, 1180×820 and 1440×900, icons on and off. Save to
  design_handoff_rift_finder/screenshots/ as ledger--<rift>--<w>x<h>[--noicons].png.
- Confirm: no horizontal scroll at 390, keyboard focus visible on rows, clicking a row still
  opens the step view for that reward, and the count label still matches the row count.
- Commit after each working step. Finish with /close-out. Add the decision "Reward section uses
  the Ledger, V2 Two-tone" to docs/DECISIONS.md with today's date and the WHY above.
