# Audit — archaeology to v3, merged file resolved, recurrence scoped

**Date:** 2026-09-26 · **Wiki version:** 3.14 · **Validator:** 50 checks, all passing

## 1. The merged file was lying — resolved

`stellaris_discovery.v2.1.json` was the file the UI had been pointed at. It held **pre-v3 rift
data and no situations** — 4 entities and 25 reward rows behind `astral_rifts.v3.json` — with
nothing in the filename to say so. A consumer loading it silently rendered a Seal that was one
sentence instead of seven rewards.

Replaced by **`stellaris_discovery.v3.json`**, generated from both v3 datasets so it cannot
drift again. The old file moved to `data/_superseded/` with a note saying why.

Also retired: `astral_rifts.json` (v2.0), `archaeological_sites.json` (v1.0), and the
rifts-only `build_v3.py` / `validate_v3.py`, now replaced by `build_all_v3.py` /
`validate_all_v3.py`.

## 2. Archaeological sites migrated to v3

110 sites, 429 chapters. **184 rewards + 453 payouts + 30 chain edges, zero unclassified.**

Getting there took work the rift migration didn't: site reward lines carry reward **codes as
prefixes** (`art1 minor artifacts`, `mat2 Physics research`) where rift lines spell the payout
out (`Small astral threads (40 / 50 / 60)`). The first classifier run left **466 of 686 lines
unclassified** purely on that difference. The archaeology rule set now handles both forms, and
rifts stayed at zero throughout — no regression.

**Two bulk currencies, not one.** Sites pay minor artifacts; rifts pay astral threads.
`payout_types` is now `[threads, artifacts, research, resource]`.

### A new array: `chains[]`

30 site reward lines are of the form "Reveals the X site". Those are **not rewards to your
empire** — they are edges in the dig-site graph. Filing them under a reward group would have
mixed "this unlocks the next dig" with "this gives you a modifier" under one chip, which are
different player questions.

They now live in `chains[]`, with targets resolved **against the real entity list** rather than
by regex capture — which is what caught `In Memoriam → Last Stand` dropping its "The". 26 of 30
resolve to real sites; the other 4 are typed (`event_chain`, `special_project`, `system`)
because they correctly point at things that are not dig sites. `entities[].unlocks[]` is the
same graph denormalised; 25 entities unlock another.

### The gap sweep — and why it found something different

The rift audit's lesson was "assume there is an unread wiki page." Applied here, the answer was
**no missing rewards, but one thing worth flagging**:

- 8 site reward lines point at situations documented on *other* pages (Embodied Identity,
  Adaptive Evolution, Horrific Inverse Mass, Genetic Crossroads, the Remnant chain). The
  **site's own reward is captured**; what the referenced situation then pays out is not. That is
  a different entity class, not a hole in the site data.
- **The Broken Gates references "Horrific Inverse Mass", but the Situations wiki page documents
  that name against the Automated Dreadnought guardian instead.** Unverified. Do not assume the
  two are the same thing.

This is a materially weaker gap than `Astral_rift_situations` was, where whole rewards were
absent. Recorded rather than fixed.

## 3. Recurrence — scoped, not built

Quantified before proposing anything. **Only 29 of 1,156 typed objects (2.5%) carry any time
dimension at all**, in seven shapes:

| shape | rows | example |
|---|---|---|
| `duration` | 13 | "+10% Physics research for 10 years" |
| `delayed` | 7 | "Scientist returns in 5 years with Rift Warped" |
| `permanent` (explicit) | 4 | "Home Cooking permanent empire modifier" |
| `uses` | 3 | "Incubate Wind Creatures (usable 3 times)" |
| `cycle` | 1 | The Seal, every 10 years |
| `while_active` | 1 | "Astral Cloaking (+1 Cloaking Strength while active)" |
| `ongoing_cost` | 0 | — (the Volcanic Plane pop cost lands in `duration`) |

The cadence vocabulary is tiny: 10y ×10, 6y ×3, 15y ×1, 1y ×1, every-10y ×1, 3-uses ×1.

**Conclusion: a `recurring` type was the wrong shape for the problem.** One special-cased row
does not describe this. A small `timing: {mode, years, cycle_years, uses, delay_years}` object
on every reward covers all seven shapes, is derivable from text already in the data, and makes
The Seal ordinary instead of exceptional.

### The bigger finding, which outranks it

**Relic effects are not in the dataset at all.** There are 23 relic rewards; only 2 carry any
effect text. A relic in Stellaris has a *passive* and a *triumph* with a **cooldown** — which
means the largest recurrence class in the game is entirely absent, while we were preparing to
model recurrence for a single row.

Recommended order: capture relic passive/triumph/cooldown from the Relics wiki page **first**,
then add `timing` — by which point the schema will have to handle cooldowns anyway, so design
it once.

## 4. Coverage is provable

`ignored_lines[]` is new. The parser deliberately drops branch flags and "narrative only" lines;
those are now **recorded** rather than counted, so the validator asserts an exact identity:
every v2.1 reward string appears in `rewards` + `payouts` + `chains` + `ignored_lines`. It does,
for all 437 rift strings and all 686 site strings.

This replaced an approximate check that was passing by way of a hand-written exclusion list —
which is the same class of mistake as the hand-curated finder v3 was built to eliminate.

## Assumptions to pressure-test

- **Reward magnitudes remain unverified against a live patch.** Presence and typing only.
- **Choice-line rewards inherit the chapter of the choice, not the payout** (24 rows).
- **`chains[]` covers only what the wiki states explicitly.** A dig that unlocks another without
  saying so is not in the graph.
- The Broken Gates / Horrific Inverse Mass mismatch above.
- Site chapter difficulties are still absent — the wiki does not publish them per site.
