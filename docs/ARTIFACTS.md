# Artifact & research index

Everything belonging to this project that does **not** live in this repo. Conversations get
closed and artifacts get orphaned; this file is how they stay findable from any machine.

Add a row whenever a Claude Design page, published artifact, or research output is created.

---

## Claude Design — Rift Nav (the UI)

**Project canvas:** https://claude.ai/design/p/03be95db-3869-4f61-81e5-31ca2661406c

| Page | Status |
|---|---|
| `Astral Rifts Wireframes` | superseded |
| `Rift Finder` | superseded |
| `Rift Finder HUD` | superseded |
| **`Rift Finder Holo.dc.html`** | **current — work here** |

Canvas controls present on the current page: `videoDim` (46%), `holoScan`, `cornerBrackets`,
`skipBoot`.

Header copy in the design reads: `32 RIFTS · 289 CHAPTERS · 71 REWARDS`. **All three numbers are
now wrong.** As of v3 (2026-09-26) rifts are 36 entities / 294 chapters / 157 rewards, and the
combined dataset is 146 / 723 / 341. Update when the design is next touched.

**The bundled UI data is a third copy and it is stale.** `design_handoff_rift_finder/rift-data.js`
and `dig-data.js` are hand-shaped snapshots (`window.RIFT_DATA`) matching no dataset schema, with
no version or provenance marker. They are missing all 4 rift situations and every v3 finding. See
`docs/sessions/2026-09-26-archaeology-v3-and-merge.md` open item 1 — the proposal is to generate
them from the v3 JSON as a build step.

## Published artifacts

When an artifact is published to claude.ai, add it here: name, URL, what it's for, date.

| Name | URL | Purpose | Date |
|---|---|---|---|
| Stellaris Helper Style Guide | https://claude.ai/code/artifact/8b4f99af-a76c-4f44-84c2-92a208920505 | Live design system built from the Mobbin/GitHub reference screens — tokens, type scale, components, rift patterns | 2026-08-21 |
| Folder Card Fix | https://claude.ai/artifact/QgUXDCxutvEKSuoWZMXNFU | Notched split folder card: before/after, overlay against Figma 82:17, and the hover spec | 2026-09-26 |

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
