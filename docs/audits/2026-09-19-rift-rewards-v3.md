# Rift reward audit v3 — 19 Sep 2026

**You were right that rewards were missing. Two separate causes, and the second one is bigger.**

## Cause 1 — rewards hidden inside choice lines

The v2.1 reward finder was hand-curated from the chapter *reward* column. But rift chapter
tables also carry rewards inside the *choices* column, as `also grants:`, `cost:` and
`(species gains X)` payloads. Nobody indexed those. **24 named rewards** were sitting there,
including every one of Ruined Planet's chapter-7 modifiers, all three of its Level 3 leader
grants, and all six Genesis species traits.

## Cause 2 — a whole wiki page was never read

`stellaris.paradoxwikis.com/Astral_rift_situations` documents four rift situations. No earlier
version of this dataset touched it. It contributes **13 named rewards**, and one of them
changes what the schema has to express:

- **Destroy the Crystal Sphere** — 100 astral threads, 500 exotic gases, 500 rare crystals,
  and *Peace in This Dimension* (+10% happiness, 10 years). None of this existed in the data.
- **A Rift in Space** — 100 astral threads, 25% Rift Sphere progress, and *Temporal Distortions*
  (+100% resources from jobs, pop growth, pop assembly and building build speed, 1 year).
- **The Seal** — v2.1 had this as a single sentence. It is actually a size-40 Gaia world
  (Formless Haven), the **Zadigal** paragon, the Eternal Throne relic, the Luminarium subject
  type, 1000 astral threads, a +10% damage modifier against extradimensional invaders, **and a
  choice that repeats every 10 years for the rest of the game** (16 extradimensional cruisers /
  100 astral threads / a random Physics technology).
- **Study the Crystal Sphere** — the gate that spawns The Crystal Rift. A prerequisite, not a payout.

The recurring reward is the one to watch. It is the only reward in the dataset that fires more
than once, and the schema has no way to say so yet. It is typed `recurring` so you can find it,
but any "what does this rift give me" total will be wrong for The Seal until recurrence is modelled.

## What changed in the shape

The 16 loose free-text categories are gone. Every reward is now parsed deterministically and
carries two levels:

| group (6, for chips) | types inside it | rows |
|---|---|---|
| Loot | relic, specimen | 24 |
| Empire | modifier, edict, decision, deposit, contact, system, planet, situation, followup, recurring, undocumented | 57 |
| Leaders | leader, trait | 18 |
| Research | tech | 24 |
| Forces | species, unit | 18 |
| Risk | penalty | 15 |

Bulk resource payouts (astral threads, research points, minerals) moved to a separate
`payouts[]` array — **362 of them**, which is why the old finder felt like noise. The reward
index is now 157 rows of things people actually chase.

## Coverage is provable, not asserted

The parser classifies every reward line and every choice payload against ordered rules.
Anything matching no rule lands in `unclassified` and is reported. **The count is zero** —
506 source lines, 519 typed objects, nothing dropped, nothing guessed.

`data/tools/validate_v3.py` runs 17 checks: every v2.1 reward string survives verbatim, every
type maps to a declared group, every chapter back-reference resolves, every reward links from
exactly one chapter. All pass.

## Assumptions to pressure-test

- **Reward magnitudes are still unverified.** This audit proves reward *presence* and *typing*.
  If a patch retuned a payout tier, nothing here would catch it.
- **Choice-line rewards inherit the chapter of the choice, not the payout.** Ruined Planet's
  chapter-4 and chapter-5 offers actually resolve at chapter 7. If you render "rewards at this
  chapter" literally, those six modifiers will appear three chapters early.
- **The wiki is documented against 3.14**, unchanged since the August capture. So this was a
  completeness problem in how the wiki was read, not the wiki moving — which means the fix should hold.
- **`undocumented` is a real type with one member.** Destroy the Crystal Sphere gives Xenophobe
  and Genocidal empires something the wiki declines to name. Shown rather than hidden.
- Rift situation stage numbering is the wiki's, not the game files'.

## Files

- `data/astral_rifts.v3.json` — 36 entities (32 rifts + 4 situations), 294 chapters, 157 rewards, 362 payouts
- `data/tools/parse_rewards.py` — the classifier
- `data/tools/build_v3.py` — builds v3 from v2.1 + situations
- `data/tools/validate_v3.py` — the 17 checks
- `data/tools/situations.py` — the situations source data
- v2.1 files untouched, so anything already wired keeps working
