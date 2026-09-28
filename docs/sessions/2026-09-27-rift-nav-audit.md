# Session — Rift Nav audit, fixes in four steps, two re-audits

**Date:** 2026-09-26 (evening) to 2026-09-27
**Surface:** Cowork (cloud session linked to the Mac), with Claude Code doing the edits
**Status at close:** settled. Every audit finding fixed and verified; two small new items open.

## What we set out to do

Audit the current Rift Finder (Notched split) for things that break or behave poorly on desktop,
tablet and mobile, find UX problems, and improve the dig site pages, especially showing what relics do.

## What actually changed

- **Audit:** every screen clicked through in Chromium at 1440×900, 1180×820, 820×1180, 390×844 and
  360×740, measuring overflow, text sizes, tap targets and keyboard focus. Published as the
  Rift Nav Audit artifact (see `docs/ARTIFACTS.md`).
- **Defaults:** layout now Notched split, camera PRESET 1 (see DECISIONS).
- **Step 1, layout breaks** (`c51caff`): reader panels no longer pinned when stacked, phone top bar menu,
  one-line opaque footer, compact bar only on browse, corner HUD overlap check, full-width tablet
  column, 44px touch targets, camera key `rf-holo-cam-v2`.
- **Step 2, data** (`beb5843`): `rift-data.js` and `dig-data.js` generated from v3 by
  `build_ui_data.py`; wiki reward codes translated; choices structured; new `data/relics.v3.json`
  (68 relics, passive / triumph / cost / cooldown) linked to relic rewards; header stats from data.
- **Step 3, dig redesign** (`10f1843`): reward type filter incl. Relics, grouped list, yields chips,
  relic card, phase timeline with PICK / OR choices, "How digs work" table, relic cards on rifts.
- **Step 4, polish** (`c2bac80`): type minimums, keyboard access, opaque overlays, one progress
  counter, short names, search covers rift rewards, filter lists reward types only, new labels.
- **Follow-up** (`5f3d844`, `e6c73ef`): reviewed short names in `data/overrides/reward_names.json`,
  duplicate routes merged, "32 rifts · 4 situations", DLC shown as muted text, conditional payouts
  ranked last, tablet footer, toggle size.
- **Re-audits:** after step 4 and after the follow-up. Final result: every finding fixed.

## Decisions made

In `docs/DECISIONS.md`: UI data generated from v3; relic catalogue from the wiki; UI work happens
in the repo and Claude Design is a snapshot; Notched split + PRESET 1 defaults; reward short names
are hand-reviewed overrides.

## What's still open

1. **N5:** the Astral Rifts / Dig Sites toggle buttons have no accessible name (labels sit outside the
   buttons). Add an `aria-label` to each.
2. **N6:** at 390px the browse subtitle is cut off with "…". Let it wrap.
3. Testing was in Chromium only. Safari and a real phone haven't been checked.
4. Figma has no hover state or header panel for the folder card. Add them so Figma stays the reference.
5. The Claude Design project is stale (see ARTIFACTS). Only matters if you go back to it.

## Next three things

1. Fold N5 and N6 into the next Claude Code pass.
2. Check the site on a real iPhone in Safari.
3. Resume the Holo Deck background direction (`docs/sessions/2026-09-06-holo-deck.md` §7).

## Links

- Rift Nav Audit: https://claude.ai/artifact/FvjddSmQviCrPB8VAvqVgY
- Folder Card Fix: https://claude.ai/artifact/QgUXDCxutvEKSuoWZMXNFU
- Figma folder card: https://www.figma.com/design/1MdYxgxTFL90Cp1HXiBwAz/Rift-Helper-UI?node-id=82-17
