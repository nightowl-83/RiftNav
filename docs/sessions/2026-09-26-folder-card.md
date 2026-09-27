# Session — folder card: Figma match, responsive, hover, outline and header

**Date:** 2026-09-26
**Surface:** Cowork (cloud session linked to mikes-macbook-pro-local), with Claude Design and Figma
**Status at close:** design settled; first pass implemented and committed; follow-up prompt not yet run

## What we set out to do

Compare the "Notched split" folder card in the Claude Design handoff against the Figma folder card
(`Rift-Helper-UI`, node `82:17`), with Figma as the source of truth, and work out how to fix it.

## What actually changed

- Measured the Figma card from a render (the vector couldn't be downloaded). It differed from the
  handoff in almost every dimension: tab break, slope angles (the Figma slopes don't match each other),
  notch floor, right tab width, corner radius and outline construction. Full table in the artifact.
- Built a reference page, **Folder Card Fix**: current vs fixed vs Figma, an overlay in difference
  mode, a resize slider (320–920px), a hover demo, the header panel in context, and copyable CSS/JS.
- Mike iterated on it: responsive left tab, max width 920, a hover state, a softer outline, corner
  accents (a second pass after the first read as too obvious), and the header panel matching the cards.
- Claude Code ran the **first** handoff prompt (the geometry, responsive width, Figma stroke and hover). Those
  edits are in `design_handoff_rift_finder/Rift Finder Holo.dc.html` and `README.md` and in the
  "follows Figma 82:17" entry in `docs/DECISIONS.md`. **None of that is committed.** The prompt asked
  Claude Code to show the diff first.
- This close-out commits only this note and the new DECISIONS entry. The ARTIFACTS row for Folder Card
  Fix was already added by the Claude Code run and is committed with this close-out.

## Decisions made

In `docs/DECISIONS.md`:
- "The notched folder card follows Figma 82:17" (written by the Claude Code run, not yet committed).
- "Folder outline softened, corner accents, header panel shares the card shape" (this close-out).

## What's still open

1. ~~Review and commit Claude Code's first-pass diff.~~ Done: Mike approved it, committed 2026-09-26.
2. **Run the follow-up prompt below** in Claude Code (softer outline, corner accents, header panel).
3. ~~Uncommitted archaeology session work.~~ Done: committed separately 2026-09-26 after validate_all_v3.py passed. It was blocked by a stale `.git/index.lock`, which has been removed. Originally:: `data/*`, `CLAUDE.md`,
   `data/README.md`, the audit and the session note `2026-09-26-archaeology-v3-and-merge.md`. This
   close-out did not commit it. It needs its own review and commit.
4. The Figma file has no hover state and no header panel. Consider adding both so Figma stays the
   source of truth.
5. The Figma geometry was measured from a 1× render, so it's ±1px. The Claude Code run noted the Figma
   corner curve may be closer to 30px than 24px. 24px was kept.

## Next three things

1. Run the follow-up prompt in Claude Code, review the diff, then commit.
2. Add a hover state and the header panel to Figma so it stays the source of truth.
3. Pick up the archaeology session's open item 1 (the UI data contract).

## Follow-up prompt for Claude Code

```
Follow-up to the notched folder card change you already made in design_handoff_rift_finder/Rift Finder Holo.dc.html (folderPath / buildFrame / drawFrame). Three changes: a softer outline, blended corner accents, and the header panel moving to the same construction.
Reference page ("In context" section): https://claude.ai/artifact/QgUXDCxutvEKSuoWZMXNFU

1. SOFTER OUTLINE (buildFrame)
- Base gradient: grad(id + '-b', '#fff', 0.3, 0.16). It was 0.6 → 0.35.
- Hover gradient: grad(id + '-h', '#8ecbff', 0.7, 0.35). It was 0.9 → 0.5.

2. CORNER ACCENTS (buildFrame + drawFrame)
- Add a third path between the base path and the hover path: class rf-fc-corners, fill none, stroke-width 1, stroke rgba(255,255,255,.42), mask="url(#<id>-m)".
- In <defs>:
  <radialGradient id="<id>-r">
    <stop offset="0"   stop-color="#fff" stop-opacity="1"/>
    <stop offset=".3"  stop-color="#fff" stop-opacity=".6"/>
    <stop offset=".65" stop-color="#fff" stop-opacity=".18"/>
    <stop offset="1"   stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="<id>-m" maskUnits="userSpaceOnUse"> containing four <circle fill="url(#<id>-r)">
- In drawFrame, with R = 72: set the mask's x/y/width/height to -R, -R, W+2R, H+2R, and set the circles to r=R at (0,0), (W,0), (0,H), (W,H). All paths keep sharing the same d.
- On card :hover / :focus-visible, transition the .rf-fc-corners stroke to rgba(191,230,255,.6) over 180ms, alongside the existing hover rules.
- The accents should read as a gentle lift that eases into the line. No visible start or end, and no change in line weight.

3. HEADER PANEL: same construction as the card
- The browse-screen header panel in Notched split (back button, title, subtitle, rift/dig-site toggle, search field, Filter, Monitoring) currently uses tabCss() / wedge() with the 38% / 76px / 88px geometry. Replace that with the same frame the cards use: the same clip-path on the fill, the same folderPath() geometry (left tab 25%, 42×25 left slope, 25px notch, 26×25 right slope, 52px right tab, 24px radius), the same recessed bar, and the same base + corners paths via frameRef / buildFrame. Skip the hover path, or leave it at opacity 0.
- Reuse the card's code path; don't duplicate it. If tabCss() and wedge() have no remaining callers afterwards, delete them.
- Height comes from content. Padding 44px 24px 22px (the top padding clears the 25px notch). Width 100%, min 320px, max 920px, same as the cards.
- No hover, lift, wash or + column on the header.
- Grid and Split column headers are unchanged.

4. VERIFY
- In Notched split, the header and cards stack in one column with their notches lined up vertically at 320px, 683px and 920px.
- At rest the corners are slightly brighter than the edges without drawing attention, and hover still reads clearly.
- Check reduced motion and keyboard focus still work on the cards.

5. DOCUMENT
- design_handoff_rift_finder/README.md: update the stroke values, add the corner accent spec under "The notched folder shape", and rewrite "### Header panel" to say it shares the card construction (drop the old 38% / 76px / 88px layer spec).
- docs/DECISIONS.md already has an entry "2026-09-26 — Folder outline softened, corner accents, header panel shares the card shape". Don't add another. Remove the line in the "follows Figma 82:17" entry that says the header keeps its old construction.
- Show me the diff before committing.
```

## Links

- Figma: https://www.figma.com/design/1MdYxgxTFL90Cp1HXiBwAz/Rift-Helper-UI?node-id=82-17
- Folder Card Fix (reference page): https://claude.ai/artifact/QgUXDCxutvEKSuoWZMXNFU
- Claude Design project: https://claude.ai/design/p/03be95db-3869-4f61-81e5-31ca2661406c
