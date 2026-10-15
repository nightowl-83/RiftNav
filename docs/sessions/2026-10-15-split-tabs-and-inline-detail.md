# Session — Split tabs and inline detail (two desktop layouts on branches), preview fix

**Date:** 2026-09-28 to 2026-10-06 (closed out 2026-10-15)
**Surface:** Claude Code (desktop app), editing `design_handoff_rift_finder/Rift Finder Holo.dc.html`
**Status at close:** both layouts built, verified and pushed to their own branches; **neither is merged**.
Mike hasn't picked between them yet.

## What we set out to do

Try the desktop "results collapse to the left, detail opens on the right" ideas from the
Rift Nav — Split Browse Prototypes canvas as real builds, each on its own branch, without touching
`main`, mobile or the folder card.

## What actually changed

- **`split-tabs` branch** (`0e2d9aa`, from board "Test build"): a new `layout` option, "Split tabs",
  which is the default on that branch only.
  - **Browsing** looks like Notched split.
  - **Opening an item** collapses the list into an 84px icon rail or a 330px list (the choice is
    remembered in `localStorage['rf-split-mode']`). The detail opens in one of up to 5 tabs, each
    keeping its own target and reader step.
  - **Codes:** two-letter codes have a clash rule plus 5 reviewed exceptions (Dimensional Dump DD,
    Coordinates A/B/C as CA/CB/CC, Copper and Chrome CP).
  - **Sizing:** the panel is a size container, so the reader stacks by panel width.
  - **Docs:** README "Split tabs" section.
- **`inline-detail` branch** (`8079c03`, `e5f13f8`, from board D), starting from `main`:
  - **Behaviour:** in Notched split on desktop, picking a rift or dig site keeps the page. The header
    collapses, the compact bar stays up, and the cards minimize to 44px rows with a Material Symbols
    Rounded folder icon and a pin. The existing detail, dig and reader screens load into a notched
    panel on the right.
  - **Folder graphics:** untouched, verified byte for byte against `main`: `folderPath`, `frameRef`,
    `bindFrame`, `buildFrame` and `drawFrame`, plus all 28 `.rf-fc*` rules. The panel reuses
    `frameRef('panel', true)`.
  - **Docs:** README "Inline detail (Notched split, desktop)" section.
- **Both branches:**
  - **Shared helper:** a `switchTo(type, name)` helper saves and restores each item's place in
    `state.progress`. The monitoring tabs use it too.
  - **Unchanged:** mobile, plus Grid and Split column.
- **Local preview fixed** (outside the repo):
  - **Before:** the `rift-finder-holo` preview (port 8743) was serving
    `~/Claude/Rift Finder Holo.preview.html`, a copy from **20 September**. It predated the folder
    card fix and every later change, which is why the cards "broke again" after a week away.
  - **Now:** it serves `~/Claude/rift-nav-current/`, a copy of the repo build, with its own
    `serve.py`. That's a copy rather than a live link because macOS won't let the preview server
    read the Desktop folder. It currently holds the `inline-detail` file.
- **Data:** no data changed this session. `data/*.json`, `rift-data.js` and `dig-data.js` are
  untouched, so there was nothing to rebuild or validate.

**Verified** headless in Chrome at 1440×900, 1280×800 and 1180×820, plus 390×844 for mobile.

- **Split tabs:**
  - Tab place survives switching (STEP 2 OF 3).
  - A 6th tab closes the oldest inactive one.
  - Close all returns to browse with focus on the first card.
  - Tooltips aren't clipped.
  - "relic" lists exactly the 10 rifts and 12 sites with a relic reward.
  - No horizontal scroll.
- **Inline detail:**
  - Browse with nothing selected is pixel-identical to `main`, with 0 pixels different and
    animations frozen.
  - The Garden shows its 5 rewards in the panel.
  - The reader resumes on step 2 after switching away.
  - A row's pin doesn't change the selection.
  - "relic" filters the rows.
  - ×, ‹ and Escape all return focus to the card.

## Decisions made

In `docs/DECISIONS.md`:

- the folder graphics are frozen;
- the local preview serves a copy of the repo build;
- desktop layout experiments live on branches until one is picked.

## What's still open (including what went wrong)

1. **Pick a direction:** `split-tabs` or `inline-detail`, or neither. Neither is merged; `main` is
   still plain Notched split.
2. **Search difference:** under inline detail and Split tabs, the search also matches reward names
   and types (so "relic" finds rifts). On `main` it matches rift names only. Decide whether `main`
   should do the same.
3. **Safari:** never tested. All checks were Chromium, and the notch relies on `clip-path` plus an
   SVG outline.
4. **Abort confirmation:** still not decided (carried over from the mobile session).
5. **What went wrong:**
   - My test preview opened a tab on top of Mike's in the shared browser pane and showed a file
     listing. From now on, testing runs headless from `file://`, with no tabs in Mike's pane.
   - A second session committed in the same checkout mid-task and left a stale `index.lock`.
     Don't run two sessions in one checkout.
   - Much of the session went on the stale-preview confusion. The preview now serves the repo build.

## Next three things

1. Look at both branches in the preview (pane wider than 1024px) and pick one.
2. If inline detail wins, merge `inline-detail` to `main` and decide on reward-aware search for
   all layouts.
3. Test the chosen layout in Safari on the Mac and on the iPhone.

## Links

- Split Browse Prototypes canvas (boards "Test build" and D): https://claude.ai/artifact/HaAgwXd9qWinCuJ5uivkXv
- Branches: https://github.com/nightowl-83/RiftNav/tree/split-tabs and https://github.com/nightowl-83/RiftNav/tree/inline-detail
