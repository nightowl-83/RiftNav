# Session — hand-off to the Windows PC

**Date:** 2026-09-24
**Surface:** Cowork (cloud session linked to mikes-macbook-pro-local)
**Status at close:** Mac fully pushed; PC not yet cloned

## What we set out to do

Get the project ready to pick up on a Windows PC for the first time.

## What actually changed

- **Committed work that had been sitting only on the Mac.** Found at hand-off, added between
  20 and 21 Sept outside any Claude session, so the *intent* below is inferred from the files,
  not recorded at the time:
  - `resources/RiftHelperUI.fig` (2.5MB, 20 Sep) — a local Figma file for the Rift Helper UI
  - `resources/SideColumNCardLayouts-Notes.png` (1.6MB, 21 Sep) — side-column card layout notes
  - `reference/_graphics/` — four film-UI reference stills (Blade Runner 2049 / Territory
    Studio, Avengers: Age of Ultron ×2, a glowing DNA helix). Likely mood reference for the
    Holo Deck direction, which is still unsettled.
- **Added `.gitattributes`** so Windows and macOS checkouts agree on line endings. Without it,
  the first commit from the PC could mark every text file as changed.

## Decisions made

None new.

## What's still open

- **Mike to confirm what the new design files are for** — especially whether the `.fig` is
  the working copy or an export of a cloud Figma file. If it's a snapshot, it doesn't need
  re-committing on every save; every commit of a binary adds its full size to history.
- **The film stills are copyrighted.** Fine as private mood reference. If this repo is ever
  made public, `reference/_graphics/` has to come out first.
- **The Friday unpushed-work check only watches the Mac.** Work left unpushed on the PC won't
  be caught.
- From 2026-09-23: `/pick-up` and `/close-out` are Claude Code commands and don't exist in
  Cowork — in Cowork, say "pick up" / "close out". And pick-up currently needs the Mac online
  because the only GitHub credential lives there. Proposal on the table: mirror a short
  state-of-play doc into the claude.ai Stellaris Project at each close-out.

## Next three things

1. Clone onto the PC (steps in the chat of this session; Git for Windows → `git clone` →
   browser sign-in → connect folder in Claude app → "pick up").
2. Resume Holo Deck direction — read `docs/sessions/2026-09-06-holo-deck.md` §7 first. The new
   film references are probably the input.
3. Archaeological sites → v3 migration.
