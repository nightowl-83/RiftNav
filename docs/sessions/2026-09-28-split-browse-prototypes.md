# Session — Split browse prototypes (results collapse left, detail loads right)

**Date:** 2026-09-28
**Surface:** Claude (cloud session linked to the Mac), Claude Design canvas
**Status at close:** direction chosen for testing, not settled. The "Split tabs" build prompt is written
(`docs/prompts/2026-09-28-split-tabs.md`). Claude Code has created the `split-tabs` branch but hasn't committed anything yet.

## What we set out to do

Mike's idea: opening a rift or dig site shouldn't go to a new page. The results should collapse into
condensed icon cards on the left, and the detail should load on the right, so switching between events,
browsing and closing them is easier. The ask was to mock up a few versions. On mobile the current
dock layout stays, though he was open to suggestions.

Earlier the same day: finished the 2026-09-27 hosting/bug-intake close-out. GitHub refused the push from
the cloud container (no Claude GitHub App access on the repo), so it was applied from the Mac as `b09685b`.

## What actually changed

- **No code or data in this repo changed.** `data/*.json`, `rift-data.js` and `dig-data.js` are untouched,
  so no rebuild or validator run was needed.
- **Claude Design canvas "Rift Nav — Split Browse Prototypes"** (see ARTIFACTS). Five boards, all clickable;
  the first four use 12 sample rifts, the Test build uses all 32:
  - **A · Icon rail:** results shrink to an 84px column of two-letter icons with hover names;
    prev/next and close buttons; the most room for reward cards.
  - **B · Condensed list:** a 330px list of one-line rows, with search and group filters kept visible.
  - **C · Icon rail + open tabs:** each opened rift becomes a folder tab, up to 5, with its own close
    button and a "Close all".
  - **Mobile · Recents strip:** the current dock is kept; a row of the last 6 opened rifts sits under the
    top bar; reward cards are compacted to about 80px.
  - **Test build:** C, with a switch that turns the rail into B's list, and all 32 rifts with 150 rewards
    from `rift-data.js`. Search matches reward names and categories. Each tab keeps its own target reward
    (TARGET LOCKED bar with Retarget / Begin). Monitored rifts get an amber ring. The canvas opens
    focused on this board.
- **Prompt for Claude Code:** the "Split tabs" layout, saved at `docs/prompts/2026-09-28-split-tabs.md`.

## Decisions made

- Test "Split tabs" as a fourth `layout` option on a branch, not on main. See `docs/DECISIONS.md`.
- Recommended, not yet decided by Mike: C (tabs) as the model, with B (list) as a user switch. Icons
  alone don't work for search or for new players, and a 32-icon rail has to scroll (about 12 fit at
  900px tall).
- Mobile: keep the current dock layout. The recents strip is only a proposal.

## What's still open

1. Claude Code has to run the Split tabs prompt on `split-tabs` and push the branch.
2. The Cloudflare Pages project and its `SITE_PASSWORD` still aren't set up. Until they are, there's no
   branch preview URL for testers, so testing has to be local.
3. Nobody has clicked through the prototypes to confirm they render; that was left to Mike, and none
   were checked by Claude.
4. Two-letter icon codes are a stand-in; real per-rift icons would be separate design work.
   "Dimensional Conflict" and "Dimensional Dump" clash as DC, so DD is hand-assigned to Dump.
5. The rail's scale problem: about 12 of 32 icons visible, plus about 90 dig sites when the dig toggle is on.
6. Dig sites were not prototyped; they're assumed to use the same pattern with the teal accent.
7. Carried over: "STEP 1 OF 3" is duplicated on mobile; the CLASSIC link 404s; Figma lacks the hover
   state and header panel; the Holo Deck background direction is unsettled.

## Next three things

1. Run `docs/prompts/2026-09-28-split-tabs.md` in Claude Code on `split-tabs`, then have Claude verify it
   headless as in earlier passes.
2. Set up Cloudflare Pages (password secret) so `split-tabs.<project>.pages.dev` can go to testers.
3. Decide from testing: tabs vs list as the default left column, and whether mobile gets the recents strip.

## Links

- Rift Nav — Split Browse Prototypes (canvas): https://claude.ai/artifact/HaAgwXd9qWinCuJ5uivkXv
