# -*- coding: utf-8 -*-
"""The four astral rift situations, from stellaris.paradoxwikis.com/Astral_rift_situations
(captured 2026-09-14). These were absent from every earlier version of the dataset.
Stages are modelled as chapters so they flow through the same reward parser."""

SITUATIONS = [
 {"name":"A Rift in Space","group":"situation","dlc":"Astral Planes",
  "requirements":"Fires when the first astral rift appears in your space. Named 'Reaching into the Rift' for the Riftworld origin.",
  "restrictions":None,
  "notes":"2 stages, 50 progress each. Using aggressive approaches for 2+ months can fire the 'Unstable Spacetime' event, which has its own branch of outcomes.",
  "chapters":[
   {"id":"1","title":"Reaching into the Rift","rewards":[
     "100 Astral Threads",
     "25% progress toward Rift Sphere technology"],"choices":[]},
   {"id":"2","title":"Unstable Spacetime (aggressive approaches, 2+ months)","rewards":[
     "A new pre-FTL planet appears in the rift system",
     "OR a new random species appears on your nearest colony",
     "Temporal Distortions modifier for 1 year: +100% resources from jobs, +100% pop growth speed, +100% pop assembly speed, +100% building build speed"],"choices":[]}]},

 {"name":"Study the Crystal Sphere","group":"situation","dlc":"Astral Planes",
  "requirements":"Completing 'The Crystal Sphere' situation via the study approach",
  "restrictions":None,
  "notes":"1 stage, 100 progress. This is the gate that spawns The Crystal Rift — it is a prerequisite, not a payout.",
  "chapters":[
   {"id":"1","title":"Study the Crystal Sphere","rewards":[
     "Spawns The Crystal Rift"],"choices":[]}]},

 {"name":"Destroy the Crystal Sphere","group":"situation","dlc":"Astral Planes",
  "requirements":"Completing 'The Crystal Sphere' situation via the destroy approach",
  "restrictions":None,
  "notes":"1 stage, 100 progress. The mutually exclusive alternative to Study — taking it forfeits The Crystal Rift and everything downstream of it, including The Seal.",
  "chapters":[
   {"id":"1","title":"Destroy the Crystal Sphere","rewards":[
     "100 Astral Threads",
     "500 Exotic Gases",
     "500 Rare Crystals",
     "Peace in This Dimension modifier for 10 years: +10% happiness",
     "Xenophobe and Genocidal empires receive a separate reward the wiki does not name"],"choices":[]}]},

 {"name":"The Seal","group":"situation","dlc":"Astral Planes",
  "requirements":"Complete The Crystal Rift leaving the rift open, explore the Azilash system, then defeat the 8 Aberrant fleets",
  "restrictions":"If the Aberrants destroy the Formless first, Azilash goes nova and is lost along with everything below",
  "notes":"1 stage, 100 progress. The richest single payout attached to rifts, and the only one with a RECURRING reward — the 10-year choice repeats for the rest of the game.",
  "chapters":[
   {"id":"1","title":"The Seal","rewards":[
     "Formless Haven: a size 40 Gaia world in the Azilash system",
     "Zadigal paragon",
     "Recurring every 10 years, choose one: 16 extradimensional cruisers, 100 Astral Threads, or a random Physics technology",
     "Eternal Throne relic (conditional: via subjugation or victory)",
     "1000 Astral Threads (conditional: if you defeat the Formless)",
     "Luminarium subject type (conditional: if subjugation succeeds)",
     "+10% damage against extradimensional invaders (costs 2000 Astral Threads per faction)"],"choices":[]}]},
]
