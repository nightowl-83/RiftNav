# Artifact & research index

Everything belonging to this project that does **not** live in this repo. Conversations get
closed and artifacts get orphaned; this file is how they stay findable from any machine.

Add a row whenever a Claude Design page, published artifact, or research output is created.

---

## Rift Nav (the UI)

**Where the UI lives now (since 2026-09-27): `design_handoff_rift_finder/` in this repo.** Claude Code
edits `Rift Finder Holo.dc.html` directly; all audit work (steps 1–4 and the follow-up) happened there.
Default layout is Notched split; default camera is PRESET 1.

**Claude Design project (snapshot, not current):** https://claude.ai/design/p/03be95db-3869-4f61-81e5-31ca2661406c

| Page | Status |
|---|---|
| `Astral Rifts Wireframes` | superseded |
| `Rift Finder` | superseded |
| `Rift Finder HUD` | superseded |
| `Rift Finder Holo.dc.html` | **snapshot from 2026-09-26** — predates the audit fixes, v3 data and dig redesign. Don't work here without first copying the repo files in. |

Canvas controls on the page: `layout`, `backdrop`, `filterUI`, `videoDim`, `holoScan`, `cornerBrackets`, `skipBoot`.

**The bundled UI data is generated from v3** (since 2026-09-27). `rift-data.js` and `dig-data.js` are
written by `data/tools/build_ui_data.py` and carry a generated-file header; the header stats in
the design now read their counts. See `docs/DECISIONS.md`.

## Published artifacts

When an artifact is published to claude.ai, add it here: name, URL, what it's for, date.

| Name | URL | Purpose | Date |
|---|---|---|---|
| Stellaris Helper Style Guide | https://claude.ai/code/artifact/8b4f99af-a76c-4f44-84c2-92a208920505 | Live design system built from the Mobbin/GitHub reference screens — tokens, type scale, components, rift patterns | 2026-08-21 |
| Folder Card Fix | https://claude.ai/artifact/QgUXDCxutvEKSuoWZMXNFU | Notched split folder card: before/after, overlay against Figma 82:17, and the hover spec | 2026-09-26 |
| Rift Nav Audit | https://claude.ai/artifact/FvjddSmQviCrPB8VAvqVgY | UI/UX audit of the Notched split build at 5 screen sizes, dig site and relic deep dive, and two re-audits showing every finding fixed | 2026-09-27 |
| Rift Nav Mobile Dock | https://claude.ai/artifact/9kSf28hfwDHdugvtk5B4tM | Mobile navigation proposal from the iPhone test: bottom dock, full-screen search, drawers, compact detail headers, step reader strip. Implemented in `969c771` | 2026-09-27 |
| Rift Nav Bug Drop | https://claude.ai/artifact/NBFJNT3LBjFFpR14nfkZV2 | Phone bug intake (QR code): reports in the `reports` db collection, photos in the asset store. Read with ArtifactData; fetch images one asset id at a time | 2026-09-27 |
| Rift Nav Phone Test | https://claude.ai/artifact/Syk8scgbf83q5fWCQTznth | **Broken; don't use.** Loads blank because the artifact CSP blocks the `unsafe-eval` that the dc runtime needs. Test through the Cloudflare Pages site instead | 2026-09-27 |
| Rift Nav — Split Browse Prototypes | https://claude.ai/artifact/HaAgwXd9qWinCuJ5uivkXv | Claude Design canvas: A icon rail, B condensed list, C icon rail + open tabs, a mobile recents strip, and a clickable "Test build" (C + list toggle, all 32 rifts). Source for `docs/prompts/2026-09-28-split-tabs.md` | 2026-09-28 |

## Research outputs

| Topic | Where it landed | Date |
|---|---|---|
| Archaeology to v3, merged file resolved, recurrence scoped | `docs/audits/2026-09-26-archaeology-v3-and-merge.md` | 2026-09-26 |
| Astral rift rewards — completeness audit | `docs/audits/2026-09-19-rift-rewards-v3.md` | 2026-09-19 |
| Rift reward audit (first pass) | `docs/audits/2026-08-30-rift-rewards.md` | 2026-08-30 |
| Claude Code / Cowork cross-machine session portability | `docs/sessions/2026-09-20-move-repo-online.md` | 2026-09-20 |

## Upstream sources

| Source | Used for |
|---|---|
| stellaris.paradoxwikis.com (game v3.14) | All rift and site data. Rifts captured 2026-08-30; rift situations 2026-09-14; sites migrated to v3 2026-09-26 |
| `Template:Reward` on the same wiki | Reward code expansions |
| Mobbin — GitHub Web | UI reference. 17 screens, each mapped to what it drove in the style guide: `reference/mobbin-github-web-reference-screens.md` |

## Retired

| What | Status |
|---|---|
| Google Drive folder "Stellaris Helper" | **Retired 2026-09-20.** Both Google Docs imported to `reference/` as Markdown; nothing live remains there. Daily parity audit paused. |
