# Session — archaeology to v3, merged file resolved, recurrence scoped

**Date:** 2026-09-26
**Surface:** Cowork (cloud session linked to mikes-macbook-pro-local)
**Status at close:** data settled; **one new finding needs Mike's decision** (see open items)

## What we set out to do

Mike asked for a sit rep on the data behind the rift finder, then for three things: (1) fix the
merged-file inconsistency, (2) migrate archaeological sites to v3, (3) information on modelling
recurring rewards.

## What actually changed

**Both halves are now on v3. 50 validator checks, all passing, zero unclassified.**

- **`data/stellaris_discovery.v3.json`** (new, 768 KB) — 146 entities, 723 chapters, 341 rewards,
  815 payouts, 30 chains. Generated from both v3 datasets so it cannot drift.
- **`data/archaeological_sites.v3.json`** (new, 448 KB) — 110 sites migrated: 184 rewards,
  453 payouts, 30 chain edges.
- **`data/astral_rifts.v3.json`** — regenerated (157 rewards, 362 payouts) with `ignored_lines[]`.
- **Retired to `data/_superseded/`** with a README explaining each: the old merged
  `stellaris_discovery.v2.1.json` (held pre-v3 rift data behind an innocent filename),
  `astral_rifts.json` (v2.0), `archaeological_sites.json` (v1.0), the rifts-only
  `build_v3.py`/`validate_v3.py`, and `stellaris-discovery-2.1.schema.json` (described
  `reward_finder[]`, which v3 replaced).
- **`data/tools/build_all_v3.py`** and **`validate_all_v3.py`** replace the rifts-only scripts.
  One entry point builds all three files.
- `data/README.md` rewritten; `CLAUDE.md` data rules corrected (they still said archaeology was
  on v2.1).
- Audit: `docs/audits/2026-09-26-archaeology-v3-and-merge.md`.
- Also committed a `design_handoff_rift_finder/` bundle that was **staged but uncommitted** from
  an earlier Claude Design session — see open items, it matters.

### Three things worth knowing about how the migration went

1. **The first classifier run left 466 of 686 site lines unclassified.** Cause was structural:
   site reward lines carry reward *codes as prefixes* (`art1 minor artifacts`) where rift lines
   spell the payout out (`Small astral threads (40 / 50 / 60)`). Rifts stayed at zero throughout.
2. **Sites needed a fourth array.** 30 lines read "Reveals the X site" — graph edges, not rewards
   to your empire. They are in `chains[]`; `entities[].unlocks[]` is the same graph denormalised.
   Targets resolve against the real entity list, not regex — which caught
   `In Memoriam → Last Stand` silently losing its "The".
3. **Two bulk currencies.** Sites pay minor artifacts, rifts pay astral threads.
   `payout_types` is `[threads, artifacts, research, resource]`.

### The gap sweep found something weaker than last time

Applying the `Astral_rift_situations` lesson to archaeology: **no missing rewards.** Eight site
lines point at situations documented on other pages (Embodied Identity, Adaptive Evolution,
Genetic Crossroads, the Remnant chain) — the site's own reward is captured, what the referenced
situation pays out is not, and that is a different entity class. One genuine flag recorded:
The Broken Gates references "Horrific Inverse Mass", but the Situations wiki page documents that
name against the Automated Dreadnought guardian.

## Decisions made

Three, all in `docs/DECISIONS.md`: archaeology on v3 and the merged file regenerated; chain
unlocks are graph edges not rewards; dropped lines are recorded in `ignored_lines[]`.

## What's still open

**1. The UI is reading a third, stale copy of the data. This needs a call.**
`design_handoff_rift_finder/rift-data.js` and `dig-data.js` are hand-shaped snapshots —
`window.RIFT_DATA = {"rifts":[{name, group, req, restrict, notes, …}]}` — matching none of the
v2.1 or v3 schemas, carrying **no version or provenance marker**, and referencing none of the
JSON datasets. What they are missing:

- all 4 rift situations (`A Rift in Space` and `Destroy the Crystal Sphere` appear zero times)
- every v3 finding: no Zadigal, no Formless Haven, no Peace in This Dimension, no
  Temporal Distortions, no `recurring`
- the rewards/payouts split, `type`, `chains`, `unlocks`

The design header reads `32 RIFTS · 289 CHAPTERS · 71 REWARDS`. v3 has **157 rewards for rifts
alone**, 341 across both kinds. The design is showing under half.

This is the same failure the merged file just had, one layer further out: a copy with no way to
tell it is stale. Proposal — generate `rift-data.js` / `dig-data.js` from the v3 JSON as a build
step, stamped with `schema`, `version` and `generated`, so it cannot silently drift. Not done:
it changes the UI's data contract and that is Mike's call.

**2. Recurrence is scoped but not built**, and the recommended order changed — see the decision
log entry and §3 of the audit. Short version: only 29 of 1,156 objects carry any time dimension,
in 7 shapes, so a `timing` object beats a `recurring` type. But **relic effects are absent from
the dataset entirely** (23 relic rewards, 2 with any effect text), and relic triumphs have
cooldowns — so capture relic passive/triumph/cooldown first, then design timing once.

**3. No JSON Schema for v3.** The v2.1 one was retired rather than left lying; `data/README.md`
documents the shape instead.

**4. Still true from before:** reward magnitudes unverified against a live patch; choice-line
rewards carry the choice's chapter not the payout's (24 rows); site chapter difficulties absent;
`resources/images/` still empty pending the licensing call; `reference/_graphics/` film stills
must come out before this repo could go public.

## Next three things

1. **Decide on the UI data contract** (open item 1). Generating the `.js` from v3 is maybe an
   hour and removes a whole class of silent staleness.
2. **Capture relic passive / triumph / cooldown** from the Relics wiki page — biggest visible
   gap, and it settles the timing schema.
3. Resume Holo Deck direction — `docs/sessions/2026-09-06-holo-deck.md` §7 first; the
   `reference/_graphics/` film stills are probably the input.

## Links

- Audit: `docs/audits/2026-09-26-archaeology-v3-and-merge.md`
- Claude Design canvas: https://claude.ai/design/p/03be95db-3869-4f61-81e5-31ca2661406c
- Sources: `Astral_rift_situations`, `Archaeological_site`, `Situations`, `Template:Reward` on
  stellaris.paradoxwikis.com (game v3.14)
