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

---

# Continuation — mobile navigation rework (from Mike's iPhone test)

**Date:** 2026-09-27 (late; commit timestamps read 09-28 UTC)
**Surface:** Claude Code (desktop app), editing `design_handoff_rift_finder/Rift Finder Holo.dc.html`
**Status at close:** settled and pushed (`969c771`). One behaviour, the keyboard opening on tap, still needs a real iPhone.

## What we set out to do

Implement the "Rift Nav Mobile Dock" proposal (see `docs/ARTIFACTS.md`): move search, filter, monitoring
and the reader's controls out of the crowded top of the screen into a bottom dock and bottom drawers, stop
iOS zooming into the search field, and get rift/dig detail content up the screen.

## What actually changed

Everything is in `969c771` ("Mobile: bottom dock, full-screen search, drawers, compact detail headers").
It touched only the screen file and `design_handoff_rift_finder/README.md`, which has a new "Mobile
navigation" section with the full spec.

- **One switch:** `matchMedia('(max-width: 1023px), (pointer: coarse)')` sets `state.mob`, and the root gets
  `.is-mob`. Desktop-only blocks carry `.rf-d`, which is hidden under `.is-mob`.
- **Bottom dock:** Filter · Search · Monitoring on browse; Search · Monitoring on detail screens; Log ·
  Prev · Next in the reader. It sits 16px above the safe area, and the viewport meta gained
  `viewport-fit=cover`. It shrinks to icons while scrolling down. The footer and compact bar are hidden on
  mobile.
- **Full-screen search:** a 16px field, scope chips (All / Rifts / Dig sites / Rewards / Relics) and results
  grouped by type. It shares `searchIndex()` with the desktop dropdown.
- **One bottom-drawer component** for the filter, monitoring, event log, mission parameters and target
  details. It has dialog semantics, keeps focus inside, returns focus to the opener, and closes on scrim,
  swipe, Escape, selection and screen change.
- **Menus close everywhere, desktop included:** on an outside click, Escape, scrolling and a screen change.
  The compact bar's menus now open under its own triggers.
- **Detail headers:** the back link moved into the top bar, a compact MONITOR toggle sits beside the title,
  and requirements take one expandable `REQUIRES …` line. The Microverse's first reward moved from about
  65% to 31% of the screen height at 390×844.
- **Reader:** a mission strip above the card; Abort and Mission parameters moved into the ⋯ menu; the target
  card, radar and log column are hidden on mobile.
- **Fixed on the way:** the phone browse title was squeezed beside the toggle (it now stacks at 767px and
  below; this also resolves open item N6 above), and the toast wrapped onto three lines.
- **Not changed:** the data (`data/*.json`, `rift-data.js`, `dig-data.js`), so there was no rebuild and no
  validator run this part of the session.

**Verified** in headless Chrome over CDP, with real key, mouse and touch input, at 390×844 and 820×1180
(touch) and 1440×900 and 1180×820 (desktop regression walk: no horizontal scroll, nothing off screen, no
undersized text). The scratch scripts were not committed.

## Decisions made

Two are in `docs/DECISIONS.md`: the mobile navigation model, and "never block zoom; 16px fields instead".

## What's still open

1. **iPhone keyboard:** on a real iPhone in Safari, check that tapping Search raises the keyboard
   immediately. The code focuses the field inside the tap, which is what iOS needs, but headless Chrome
   can't prove it.
2. **Abort:** the spec mentioned an "existing confirm behavior", but there is none. Abort still goes straight
   back to the rift list. Decide whether to add a confirmation.
3. **Filter drawer model:** tapping a type marks it and "Show N" applies it. This was an interpretation;
   the spec also listed "a selection" as a close trigger. Confirm it on the phone.
4. **N5** from the list above (toggle accessible names) wasn't re-checked in this pass.

## Next three things

1. Test the build on Mike's iPhone in Safari: dock, search keyboard, drawer swipe, home-indicator clearance.
2. Decide on an Abort confirmation.
3. Resume the Holo Deck background direction (`docs/sessions/2026-09-06-holo-deck.md` §7).

## Links

- Rift Nav Mobile Dock (the spec and sketches): https://claude.ai/artifact/9kSf28hfwDHdugvtk5B4tM

---

# Continuation — test hosting and bug intake (Claude, cloud session)

**Date:** 2026-09-27
**Surface:** Claude (cloud session linked to the Mac), alongside the Claude Code work above
**Status at close:** the password gate is pushed (`6d3250b`). The Bug Drop is live. The Cloudflare setup itself is Mike's to do.

## What we set out to do

Let Mike put the build in front of the people he plays with, behind a password, and give him a way to
send bug photos from his phone straight into this project.

## What actually changed

- **Phone Test artifact (dead end):** we tried publishing the UI as a claude.ai artifact so it could be
  opened on a phone. It loads blank: the dc runtime (`support.js`) compiles JSX with Babel through
  `new Function`, which the artifact CSP blocks (`unsafe-eval`). This was confirmed locally. Don't retry
  this route without first precompiling the JSX.
- **Password gate (`6d3250b`):** `functions/_middleware.js` is Cloudflare Pages basic auth. It accepts any
  username plus the shared password from the `SITE_PASSWORD` secret, compared as SHA-256 digests in constant
  time. It sends `/` to `/Rift%20Finder%20Holo.dc.html` and sets `Cache-Control: private, no-store` and
  `X-Robots-Tag: noindex`. On the Pages project: connect the GitHub repo, no build command, output
  directory `design_handoff_rift_finder`, and the encrypted secret `SITE_PASSWORD`. To revoke everyone,
  change the secret and redeploy.
- **Bug Drop artifact:** a phone-friendly form, opened from a QR code, that stores reports in its own
  database (`reports` collection: `createdAt, kind, screen, note, images[], device, browser, viewport,
  status, reply`) with photos in its asset store. Claude reads it with ArtifactData `list` on `reports`,
  then fetches each image with Artifact `read` (`url` + `path` = asset id, **one call per id**; `paths`
  fails for assets). The first report (`pd16ywlh5w2zi7r04e2g`) was Mike's iPhone notes. It became the
  Mobile Dock proposal and is marked `seen` with a reply.

## Decisions made

Two new entries in `docs/DECISIONS.md`: the test site is Cloudflare Pages behind a shared password, and
bug reports come in through the Bug Drop.

## What's still open

1. **Cloudflare setup:** Mike creates the Pages project and sets `SITE_PASSWORD`. Until then there's no
   shared URL.
2. **Mobile polish from the verification pass:** "STEP 1 OF 3" shows in both the mission strip and the
   step card. On phones the reward cards are about 200px tall and mostly empty.
3. **CLASSIC link:** it points to `Rift Finder HUD.dc.html`, which isn't in `design_handoff_rift_finder/`
   (it 404s on the hosted site).
4. **Figma:** it still lacks the folder card hover state and the header panel.
5. **Phone Test artifact:** it's dead and can be deleted from claude.ai if Mike wants.

## Next three things

1. Stand up the Cloudflare Pages site and share the URL and password with the group.
2. Test on the iPhone. File anything odd through the Bug Drop, then have Claude read the reports.
3. Fix the duplicate step count and the tall phone reward cards.

## Links

- Rift Nav Bug Drop: https://claude.ai/artifact/NBFJNT3LBjFFpR14nfkZV2
- Rift Nav Phone Test (broken, CSP): https://claude.ai/artifact/Syk8scgbf83q5fWCQTznth

