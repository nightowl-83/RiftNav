# Decision log

Decisions that still bind, newest first. Each entry: what was decided, when, why, and what
would overturn it. If a decision is reversed, don't delete it — add a new entry that
supersedes it and say so.

---

## 2026-09-26 — Folder outline softened, corner accents, header panel shares the card shape

**Decided:** Refines the "notched folder card follows Figma 82:17" entry below, and supersedes its
**Outline** bullet and its line saying the header panel keeps its old construction.

- **Outline:** softer than Figma. White gradient `#fff` 30% → 16% left to right (was 60% → 35%).
  Hover outline `#8ecbff` 70% → 35% (was 90% → 50%).
- **Corner accents:** a third path on the same outline, 1px, `rgba(255,255,255,.42)`, masked to a
  72px radial falloff (stops 100% / 60% at .3 / 18% at .65 / 0%) at the four outer corners. On hover
  it goes to `rgba(191,230,255,.6)`.
- **Header panel:** the browse-screen panel (title, search, Filter, Monitoring) uses the same
  shape, stroke and corners as the cards, including the 52px right tab, so the notches line up
  down the column. Height from content, padding `44px 24px 22px`, width 320–920px, no hover.

**Why:** At the Figma stroke strength the outline competed with the content. Mike wanted it pulled
back but with the corners still carrying some emphasis. A first pass (75%, 1.25px, 40px falloff) read
as a separate element stuck on each corner. Matching the line weight and stretching the falloff makes
it read as light catching the edge. The header shares the construction so the column reads as one
system rather than two shapes stacked.

**What would overturn it:** a Figma revision that defines the header panel or a stroke treatment.

---

## 2026-09-26 — The notched folder card follows Figma 82:17

**Decided:** The "Notched split" card in `design_handoff_rift_finder/Rift Finder Holo.dc.html`
is drawn to Figma node `82:17`:

- **Geometry:** the left tab ends at `25%` of the card width and scales with it. Everything else
  is fixed px: slopes `42×25` and `26×25`, notch depth `25`, right tab `52` (matching the +
  column), corner radius `24`.
- **Width:** `100%`, clamped to `320–920px`.
- **Outline:** the Figma white gradient stroke (`#fff` 60% → 35%), drawn as one SVG path per card
  and redrawn on resize. It replaces the blue hairline built from tab and wedge `<div>`s.
- **Corner brackets:** none on the notched card. Grid and Split column keep theirs.
- **Hover and focus:** lift `-2px` (none under reduced motion); deeper shadow; a cyan outline
  (`#8ecbff` 90% → 50%) fades in with a soft glow; a cyan wash over the fill; the bar hairline,
  group label and + column turn cyan. Keyboard focus adds a 2px outline stroke. The + is its own
  button and never opens the card.

The full spec is in the handoff README under "The notched folder shape" and "Hover and focus".
The header panel keeps its old construction (38% / 76px / 88px).

**Why:** The old card broke at 34% on both sides, so the notch and right tab stretched with
width. The + divider never lined up with the right tab, and the hairline was assembled from six
layers that didn't meet cleanly at the slopes. A single path from one function can't drift, and
fixing everything except the left tab keeps the notch looking the same from 320 to 920px.

**Open:** Figma's corner curve measures closer to ~30px than the specified `24px`; `24` was kept
per spec. The monitored-state glyph (`⦿`) is carried over and not yet designed in Figma.

**What would overturn it:** a Figma revision of 82:17, or the header panel moving to the same
construction (which would supersede the header half of the README section).

---

## 2026-09-26 — Both halves on v3; the merged file is generated, never authored

**Decided:** Archaeological sites move to the v3 shape (`archaeological_sites.v3.json`), and
`stellaris_discovery.v3.json` is **generated from both v3 datasets** by `build_all_v3.py`. The
old `stellaris_discovery.v2.1.json` is retired to `data/_superseded/`.

**Why:** The v2.1 merged file held pre-v3 rift data and no situations — 4 entities and 25 reward
rows behind `astral_rifts.v3.json` — with nothing in the filename to say so. A consumer loading
it silently rendered stale rifts. Hand-maintaining a merged file is how that happened; generating
it means it cannot drift from its parts. The validator now asserts merged == rifts + sites on
every count.

**Supersedes:** the "load `stellaris_discovery.v2.1.json` for a combined UI" guidance in
`data/README.md`.

**What would overturn it:** rifts and sites diverging enough that one schema stops fitting both.

---

## 2026-09-26 — Chain unlocks are graph edges, not rewards

**Decided:** "Reveals the X site" lines live in `chains[]` with resolved `targets[]`, plus
`entities[].unlocks[]` denormalised. They are **not** in `rewards[]` and get no reward group.

**Why:** 30 archaeology lines are of this form. "This unlocks the next dig" and "this gives you a
modifier" are different player questions; putting them under one chip would have made the finder
harder to scan, which is the problem v3 exists to solve. As a graph it also became useful —
25 entities unlock another, so precursor chains are now navigable.

**Consequence to respect:** 4 of 30 chains resolve to no site because they point at event chains,
a special project and a system. They carry `target_kind` rather than an empty `targets[]`, so
"unresolved" is never ambiguous with "not yet parsed".

---

## 2026-09-26 — Dropped lines are recorded, not counted

**Decided:** Lines the parser deliberately discards (branch flags, "narrative only") are written
to `ignored_lines[]`. The validator then asserts an exact identity: every v2.1 reward string
appears in `rewards` + `payouts` + `chains` + `ignored_lines`.

**Why:** The previous "nothing was lost" check passed by way of a hand-written exclusion list of
structural strings — the same class of mistake as the hand-curated reward finder that v3 was
built to eliminate. An approximate check that passes is worse than no check.

---

## 2026-09-26 — Recurrence: capture relic effects before modelling timing

**Decided:** Do **not** build a `recurring` reward type. When recurrence is modelled it will be a
`timing: {mode, years, cycle_years, uses, delay_years}` object on every reward. But relic
passive/triumph/cooldown data gets captured **first**.

**Why:** Only 29 of 1,156 typed objects carry any time dimension, across 7 shapes
(duration 13, delayed 7, permanent 4, uses 3, cycle 1, while_active 1) — a type describing one
row was never the right shape. More importantly, **relic effects are absent from the dataset
entirely**: 23 relic rewards, only 2 with any effect text. Relic triumphs have cooldowns, so the
largest recurrence class in the game is missing while we were preparing to model it for The Seal.
Capturing relics first means the timing schema gets designed once, against real cooldowns.

**Supersedes:** the 2026-09-19 entry "Recurring rewards are typed but not modelled" — that
entry's consequence still holds (totals are wrong for The Seal), but its implied next step
(model recurrence) is reordered behind relic effects.

**Cost note:** both datasets are generated, so adding `timing` later is a regeneration, not a
migration. There is no penalty for deciding after relic effects land.

---

## 2026-09-20 — This repository is the source of truth

**Decided:** The Git repository, hosted on GitHub (private), is authoritative for this
project. Any machine is a working copy.

**Why:** Work needs to move between machines. The previous arrangement made one laptop
authoritative with a Google Drive mirror, which meant the project only existed where that
laptop was. Git also gives real history — the `(pre-audit backup 2026-08-30).docx` file in
`reference/_superseded/` is exactly the kind of manual versioning that stops being necessary.

**Supersedes:** The 2026-08-22 decision that `~/Desktop/Projects/Stellaris` on
mikes-macbook-pro was the source of truth, with Drive as mirror. That setup and its daily
parity audit are retired; the notes are preserved in `docs/archive/`.

**What would overturn it:** Assets growing past what Git handles comfortably (large video,
many high-res PNGs). Current repo is ~15MB. Past roughly 1GB, or if `Holo/refs/` starts
churning binary stills every session, move heavy assets out and consider Git LFS.

---

## 2026-09-19 — Rewards are parsed deterministically, not hand-curated (v3)

**Decided:** `astral_rifts.v3.json` replaces the hand-curated rift reward index. Rewards
carry two levels — `group` (6, for chip rows) and `type` (18, for icons and detail labels).

**Why:** Two classes of reward were simply missing from v2.1. (1) 24 named rewards lived
inside chapter *choice* lines as `also grants:` / `cost:` / `(species gains X)` payloads and
were never indexed. (2) The `Astral_rift_situations` wiki page had never been read at all,
contributing 13 more. Hand-curation is how both happened.

**Source:** `docs/audits/2026-09-19-rift-rewards-v3.md`; wiki data from
stellaris.paradoxwikis.com, game version 3.14.

**Still open:** Archaeological sites have not been migrated to v3 — they remain on v2.1.

---

## 2026-09-19 — Recurring rewards are typed but not modelled

**Decided:** The Seal's every-10-years choice is typed `recurring` so it can be found, but
the schema has no way to express recurrence.

**Consequence to respect:** Any "total value of this rift" calculation is **wrong for The
Seal** until recurrence is modelled. Don't ship a totals view without special-casing it.

---

## 2026-09-07 — The background is a particle system, not video

**Decided:** Build the Holo Deck background as a canvas/WebGL particle simulation. The
video-based approach — a state graph of short generated clips with pixel-matched junction
frames — is the fallback, not the plan.

**Why:** With video, a transition can only begin at a loop boundary, so a click can sit for
up to 3 seconds with nothing happening. That was the worst problem in the video design. A
particle system morphs on the click frame. "Seamless loop" also stops being a problem, since
a continuous simulation has no loop to close.

**Artifact:** `Holo/Holo Deck Motion Spec — v1.3.html` is the superseded video spec, kept.

**Still open as of that session:** Mike's assessment of the latest prototype was "not really
what I am looking for." Direction is **not** settled. Read
`docs/sessions/2026-09-06-holo-deck.md` §7 before building.

---

## 2026-09-06 — "Events" are out of scope

**Decided:** The tool covers Astral Rifts and Archaeological Sites only. General events are
deferred.

---

## 2026-09-20 — Session close-out is a committed command, not a habit

**Decided:** `/close-out` and `/pick-up` live in `.claude/commands/` and are committed, so
they exist on every clone. A weekly scheduled task pushes unpushed commits and flags work
that happened without a close-out.

**Why:** Claude Code CLI conversation history is machine-local, isn't synced, and is swept
after ~30 days ([docs](https://code.claude.com/docs/en/sessions)). The transcript is not a
durable record and can't be made into one. The only thing that crosses machines is what gets
committed, so the discipline of writing down reasoning had to become a command rather than
something to remember.

**What would overturn it:** Anthropic shipping cross-device CLI session sync. Even then the
decision log stays useful — a transcript is not a decision record.
