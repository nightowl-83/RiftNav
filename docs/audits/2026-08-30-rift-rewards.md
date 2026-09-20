# Astral Rift reward audit — 30 Aug 2026

**Verdict: your suspicion was right, but not where you'd expect.**

The 32 per-rift **chapter tables** in `Astral Rifts — Complete Event, Requirement & Reward Reference.docx`
are essentially complete. I re-checked all 32 rifts against
`stellaris.paradoxwikis.com` (per-rift pages where they exist; the main `Astral_rift`
page for The Tower, The Vortex, Whiteout, Tropical Habitat, Volcanic Plane,
Windswept Planet, Psionic Stranger and Siege on Paradise, which have no
dedicated pages). I found **no rift missing, no chapter missing, and no chapter
reward missing** — only four wording gaps, listed at the bottom.

The gap was in **section 3, the reward finder**. It indexed 61 rewards. The
chapter tables it is supposed to summarise contain 122. **Half the rewards in
your own document were unreachable from the finder.**

## What was missing, by category

| Category | Was | Now | Biggest omission |
|---|---|---|---|
| Specimens (Grand Archive) | 1 | 13 | 12 of the 13 rift specimens were absent — only Repurposed Cleaning Drone was indexed |
| Technologies | 3 | 15 | every Biology / Particles / Computing / Psionics progress payout |
| Leader traits | 5 | 14 | Rift Warped (5 rifts), Partially Digested, Maimed, Obelisk's Curse |
| Paragons & leaders | 5 | 12 | all four Ruined Planet leader grants; the four "scientist returns in 5 years" outcomes |
| Warnings | 1 | 10 | there was no index of scientist deaths, the 20-year ageing, or the Lone Object crystalline fleet |
| Empire modifiers | 24 | 29 | Lonely Planet, Vortex Fuel, both Volcanic Plane follow-ups, Zroni Insight Storm Safeguard |
| Species & pops | 2 | 6 | every Evolutionary Predators DNA payout except Rockworms |
| Other | 1 | 4 | the Rift Fluid Samples effect, the Formless follow-up |
| **Total** | **61** | **132** | |

Relics (8), Edicts (3), Planetary decisions (6), Unlocks (2), Rift deposits (7),
Diplomacy, Situations, Systems were already complete and are unchanged.

### The specimen problem in particular
If you were using the finder to answer "which rifts feed the Grand Archive", it
would have told you *one*. The real answer is thirteen: Repurposed Cleaning Drone
(Chemical Wasteland), Genesis Core, Interdimensional Treaty, Wormhole Fur,
Mutative Digestive Fluids, Extreme Contortionist DNA, Leviathan Scale,
Dimensional Endothelial Lining, Symbiotic Fruit, Mini Moon Dust,
Obsidian Obelisk Fragment, The Writer's Sphere, Extradimensional Fungus.

## Four wording corrections applied to the chapter tables

1. **The Advisor** ch. 3/4-A and **The Corridors** ch. 4-A-fail — "Rift Warped plus a
   random trait" → the wiki names the pool: Spark of Genius, Meticulous or Roamer.
2. **Dimensional Dump** ch. 4 — the Level 6 Commander also arrives with a random
   specialization.
3. **The Fluid** ch. 4/5-A and 4/5-B-fail — Rift Fluid Samples now states its effect
   (+10% Biology research speed).

## What I checked and did *not* change

- **Reward code expansions.** I pulled `Template:Reward` to verify the ladder.
  Your table is correct: `rsh3` really is 24x (500–1,000,000), `rsh4` 48x, `rsh5` 96x.
  An intermediate reading suggested rsh3 was 18x; the literal template source
  disproved it. No change made.
- **Non-wiki cross-check.** I searched the Paradox forum balance thread, Steam and
  Reddit for rewards the wiki omits or gets wrong. Nothing corroborated turned up —
  the discussion there is balance opinion, not errata. Nothing was added on the
  strength of an uncorroborated player report.

## Assumptions to pressure-test

- The wiki is one hop from the game files, and Astral Planes has been patched since
  these tables were written. Before shipping tooling, spot-check the high-traffic
  rifts against your installed version: The Mechanism, Desert Ruins, The Garden,
  The Crystal Rift.
- I verified *presence* of rewards, not *magnitude*. If a patch retuned a payout
  tier, this audit would not catch it.
- "Rewards on entering" vs "on completing" — the rift doc's column header says
  entering; the wiki's tables read as on completion of the chapter. Worth resolving
  before you build a planner on the timing.
- The Crystal Rift's paragon / Luminarium / Eternal Throne rewards sit behind the
  *Seal situation* and an Aberrant fleet fight, not behind the rift itself. Treat
  them as conditional.

## Files

- `Astral Rifts — Complete Event, Requirement & Reward Reference.docx` — updated in place
- `Astral Rifts — Complete Event, Requirement & Reward Reference (pre-audit backup 2026-08-30).docx` — the version before this pass
- `data/astral_rifts.json` — machine-readable: 32 rifts, 289 chapters, 132 finder rows, reward-code key
- `Archaeological Sites — Complete Site, Requirement & Reward Reference.docx` — new companion, 110 sites
- `data/archaeological_sites.json` — 110 sites, 429 chapters, 210 finder rows
