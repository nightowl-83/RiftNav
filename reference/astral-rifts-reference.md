<!-- Imported from Google Docs 2026-09-20. Source doc retired.
     Original: https://docs.google.com/document/d/1X6nrrljs9muE4mI3vgIhdFXA96QRdZoteQOX_g260yQ/edit
     This is the human-readable reference the datasets were built from.
     For machine use load data/astral_rifts.v3.json instead - and note this
     document predates the 2026-09-19 audit, so it is missing the rift
     situations and the choice-line rewards. See docs/audits/. -->

# **Stellaris Astral Rifts — Complete Event, Requirement & Reward Reference**

**Source:** https://stellaris.paradoxwikis.com/Astral_rift and linked per-rift pages | **Captured:** 2026-08-20 | **Coverage:** 32 rifts (24 general, 6 unique, 2 precursor)

**How to read a path:** paths are written as *chapter* "*choice you click*" → *next chapter* "*choice*". A step marked **[fail]** is what happens when the dice roll fails that chapter. Difficulty numbers are subtracted from your roll (d10 + scientist Astral Rift Skill + clues), so a difficulty 6 choice is the one that stalls the longest.

## **1. How rift exploration works**

Rift must be inside your borders. Requires the Rift Sphere rare technology plus a scientist and science ship. Phases are 90 days. Roll = d10 + scientist Astral Rift Skill + clues - chapter difficulty. 14+ completes the chapter (75 XP), 10-13 gives 2 clues (40 XP), 5-9 gives 1 clue (25 XP), 4 or less gives nothing (10 XP) and has a 1.5% chance to fail the chapter (0.75% with the Riftworld origin). Councillors cannot explore rifts and exploration cannot be stopped.

**Spawning:** After the mid-game year, chance/100 = 2 x years_since_last_spawn x weight + eligible_systems/3. Weight is 1 base, x2 for Riftworld origin, x2 for the Dimensional Worship civic, x10 if you began 'A Rift in Space' but lost your last rift. -25 flat if you have already completed 5 rifts. 10-year moratorium after each spawn.

## **2. Reading the reward values**

The wiki writes most payouts as a multiplier of your empire's current output, clamped to a range. This document expands those codes; the raw codes are preserved in the JSON dataset.

|  |  |
| :-: | :-: |
| Code | Meaning |
| ast1 | Small astral threads (40 / 50 / 60) |
| ast2 | Medium astral threads (90 / 100 / 110) |
| ast3 | Large astral threads (140 / 150 / 160) |
| x\|mat1 | 6x of the named resource (100-1,000) |
| x\|mat3 | 18x of the named resource (250-5,000) |
| x\|mat5 | 48x of the named resource (700-30,000) |
| x\|rsh1 | 12x of the named resource (250-100,000) |
| x\|rsh3 | 24x of the named resource (500-1,000,000) |
| x\|rsh5 | 96x of the named resource (2,000-2,000,000) |
| x\|uni3 | 18x of the named resource (250-1,000,000) |
| x\|uni5 | 48x of the named resource (700-2,000,000) |

## **3. Reward finder — “I want X, what do I click?”**

### **Relics**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Advisor Core | The Advisor | 1 "Disable this thing." -\\\> 2/3 "Discharge an electromagnetic pulse." -\\\> 3/4-B "Attempt to recover its core." |
| Celestial Tear | Subnautical | 1 "Dive deeper." -\\\> 2 "Activate the engines." -\\\> 3-A "Interesting." -\\\> 4 "Try to communicate." -\\\> 5-A "Greetings." |
| Daedalus Seal | Dimensional Conflict | 1 "Study its composition." -\\\> 2-A "Fascinating." -\\\> 3 "Try to activate the dodecahedron." |
| Ever Spinning Top | The Vortex | 1 "Proceed further." -\\\> 2a "(continue)" -\\\> 3 "(continue)" -\\\> 4 "Flash lights." -\\\> 5a "(continue)" |
| Infinity Root | The Garden | thorns "Burn the weeds." -\\\> hollow "Burn it all." -\\\> creature "Burn the Creature." |
| Plasmic Core | The Fluid | 1 "Proceed forward at ease." -\\\> 2/3 "Follow the flow outward." -\\\> 3/4 "Use emergency gasses." |
| The Continuum — passive +5% Energy, Minerals, Food, Alloys, Consumer Goods and Research Speed; active grants a large lump of every resource | The Mechanism | 1 "(continue)" -\\\> 2 "Jam the gears." -\\\> 3 "(roll)" |
| Time Crystal | Desert Ruins | 1 "Fascinating." -\\\> 2 "Let's hope for the best." -\\\> 3 "Weren't they lost?" -\\\> 4-A "Press the blue button." -\\\> 5-A "Press the pentagon button." -\\\> 6-A "Press the button with six dots." |

### **Paragons & leaders**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Level 6 Commander with the Rift Warped trait (arrives after 1 year) | Dimensional Dump | 1 "Bring it aboard and give aid." -\\\> 2 "Attempt to negotiate." -\\\> 3-B "(continue)" |
| New scientist in 1 year with Society Focus + Increased Lifespan (if invited to your empire) | The Tower | 1 "Attempt to communicate with the creature." -\\\> 2a "Invite them aboard." |
| Option to recruit the paragon Oakenstalk | Siege on Paradise | 1 "Contact the planet's inhabitants." -\\\> baol-2 "Disclose what we know of the Baol. / We are explorers." -\\\> baol-3 "We will help however we can." -\\\> baol-4 "Genetically modify the Baol." |
| Plantoid leader | The Garden | thorns "Burn the weeds." -\\\> hollow "Burn it all." -\\\> creature "Burn the Creature." |
| Scientist becomes 5 years younger | The Microverse | 1 "(continue)" -\\\> 2 "(continue)" -\\\> 3 "Synchronize with the fleet." |

### **Edicts**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Astral Cloaking (+1 Cloaking Strength while active) | Siege on Paradise | 1 "Contact the planet's inhabitants." -\\\> baol-2 "Disclose what we know of the Baol. / We are explorers." -\\\> baol-3 "We will help however we can." -\\\> baol-4 "Deploy experimental planetary cloaking." |
| Automated Disinfection | Chemical Wasteland | 1 "Investigate the robots." -\\\> 2-A "Allow the drones to approach." -\\\> 3-A "Follow the drones." -\\\> 4-A "Explore the lab." -\\\> 5-A "Document and study the sanitary infrastructure." |
| Spontaneous Crystallization (converts 1% of minerals into rare crystals) | Entertainment Nexus | 1 "Continue investigations." -\\\> 2 "Very well." -\\\> 3 "A flippant use of impressive technology." -\\\> 4 "An interesting talent." -\\\> 5 "A rare specimen, indeed." -\\\> 6 "Visit the contortionist." -\\\> 7-C "Secure a tissue sample." |

### **Planetary decisions**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| 3 Fractal Seed planetary decisions | The Lattice | 1 "Explore further." -\\\> 2-A "Continue your investigations." -\\\> 3 "Can it be trusted?" -\\\> 4 "Unsettling..." -\\\> 5 "We are done here." |
| 9 Fractal Seed planetary decisions | The Lattice | 1 "Explore further." -\\\> 2-A "Continue your investigations." -\\\> 3 "Can it be trusted?" -\\\> 4 "Unsettling..." -\\\> 5 "Retrieve the globes." |
| Display Microplanet Husk decision | Tiny Planet | 1 "(continue)" -\\\> 2 "(continue)" -\\\> 3 "Establish contact." -\\\> 4 "Destroy the moon." -\\\> 5b "Put them out of their misery." |
| Incubate Wind Creatures (usable 3 times, +5 max generator districts each) | Windswept Planet | 1 "Rise above the storm." -\\\> 2a "(continue)" -\\\> 3a "(continue)" -\\\> 4a "Find a way to remove the fungus." |
| Intentional Tidal Locking planetary decision | Tiny Planet | 1 "(continue)" -\\\> 2 "(continue)" -\\\> 3 "Establish contact." -\\\> 4 "Attempt to fix the moon's orbit." -\\\> 5a "(continue)" |
| Rockworm Hive planetary decision | Rockworms | 1 "Continue surface observations." -\\\> 2 "Sample the microorganisms." -\\\> 3/4/5 "Set explosive charges." |

### **Leader traits**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Black Light Blinded | Bleached Planet | 1 "Explore the Terrain." -\\\> 2 "Retreat to the Rift Sphere." -\\\> 3-A "Fly towards the distant horizon." -\\\> 5-A "Continue your observations." |
| Psychic (if the leader has Latent Psionic) | Desert Ruins | 1 "Fascinating." -\\\> 2 "Let's hope for the best." -\\\> 3 "Weren't they lost?" -\\\> 4-A "Press the blue button." -\\\> 5-A "Press the pentagon button." -\\\> 6-A "Press the button with six dots." |
| Psychic + Planar Theorist + Riftwalker + Foreign Consciousness + Resilient on the scientist (upgraded versions if already Psychic) | Entangled Dark Matter | 1 "Approach the mass of dark matter." -\\\> 2/3-A "We are explorers. / We are strangers." -\\\> 3/4-A "Offer this scientist as a vessel. / Assimilate the entity." |
| Sanitary Drone Assistant | Chemical Wasteland | 1 "Explore the cave." -\\\> 2-B "Autopsy the avian corpse." -\\\> 3/4-A "What happened here?" -\\\> 5-B "Keep this drone as a personal research assistant." |
| Spark of Genius | Bleached Planet | 1 "Explore the Terrain." -\\\> 2 "Retreat to the Rift Sphere." -\\\> 3-A "Fly towards the distant horizon." -\\\> 5-A "Continue your observations." |

### **Empire modifiers**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| \\+10% Physics research for 10 years | Whiteout | 1 "Maximize propulsion." -\\\> 2a "(continue)" -\\\> 3 "Take a sample." -\\\> 4a "(continue)" |
| \\+50% Governing Ethics Attraction for 10 years | Strange Station | 1 "Study their people." -\\\> 2-A "Excellent." -\\\> 3 "Welcome friendship between our empires." |
| A Star is Born: +10% Physics research for 10 years | The Microverse | 1 "(continue)" -\\\> 2 "(continue)" -\\\> 3 "Repolarize the hull." -\\\> 4-B "Approach the closest star system." -\\\> 5-A "There may never be another chance." |
| Astral Shield Experimentation: +5% Shield HP, +5% Shield Hardening | Siege on Paradise | 1 "Contact the planet's inhabitants." -\\\> baol-2 "Disclose what we know of the Baol. / We are explorers." -\\\> baol-3 "We will help however we can." -\\\> baol-4 "Generate an astral shield." |
| Black Curtain + astral threads: +25% Astral Rift Exploration Speed, -50% Astral Rift Fail Probability | Ruined Planet | Chapter 4-A "Offer astral threads." (-100 threads) -\\\> chapter 5-A -\\\> chapter 7 |
| Black Curtain + resources: +0.5 basic resource from the matching job category | Ruined Planet | Chapter 4-A "Offer resources." (-1000 basic resource) -\\\> chapter 5-A -\\\> chapter 7 |
| Black Curtain base: +5% Pop Growth Speed and +5% Habitability | Ruined Planet | Chapter 2 "Visit the Black Curtain." -\\\> reach chapter 7 by any route |
| Chapter 5 astral threads: +5% Sublight Speed | Ruined Planet | Chapter 5-A "Offer astral threads." (-100 threads) -\\\> chapter 6 -\\\> chapter 7 |
| Chapter 5 energy: +5% Ship Build Speed | Ruined Planet | Chapter 5-A "Offer energy." (-1000 energy) -\\\> chapter 6 -\\\> chapter 7 |
| Colonization Drones (+25% colony development speed, +25% clear blocker speed) | Chemical Wasteland | 1 "Explore the cave." -\\\> 2-B "Autopsy the avian corpse." -\\\> 3/4-A "What happened here?" -\\\> 5-B "Repurpose the drone's technology." |
| Extra Dimensional Spores: +25% Exotic Gases | Windswept Planet | 1 "Shelter in the cave below." -\\\> 2b "(continue)" -\\\> 3b "(continue)" -\\\> 4b "Protect the ecosystem against the wind." |
| Foreign Consciousness (+5% research) for Gestalt empires | Entangled Dark Matter | 1 "Approach the mass of dark matter." -\\\> 2/3-A "We are explorers. / We are strangers." -\\\> 3/4-A "Offer this scientist as a vessel. / Assimilate the entity." |
| Formula Pink: +20 opinion from non-robotic/lithoid/toxoid empires, +10% army health, -50% morale damage | Tropical Habitat | 1 "(continue)" -\\\> 2 "Examine the fauna." -\\\> 3a "Find the source of this gas." -\\\> 4 "Explore the chasm directly." -\\\> 5b "Extract the mouth." -\\\> 6b "Analyze the severed organ." |
| Fractured Ambassadors (Gestalt Consciousness only) | Strange Station | 1 "Study their people." -\\\> 2-A "Excellent." -\\\> 3 "Welcome friendship between our empires." |
| Genesis Insight (Gestalt Consciousness only) | Genesis | 1 "Arm them with might." -\\\> 2 "Diligence." -\\\> 3 "Preserve the old ways." |
| Grunur Weapons Interface: +10% Ship Fire Rate | Siege on Paradise | 1 "Contact the orbiting fleet." -\\\> grunur-2 "Let us see where this leads... / The Grunur are dangerous. Be cautious." -\\\> grunur-3 "We are explorers, and we have seen your future." -\\\> grunur-4-known "Share rare military technology with the Grunur." -\\\> grunur-sharing "A worthy exchange." |
| Procedural Space (+1 district, +1 branch office) | The Corridors | 1 "Break through the floor." -\\\> 2-A "Fascinating." -\\\> 3 "Hack it." |
| Reconverted Leader (+1 envoy) if you convert the scientist to an envoy in the follow-up event | Windswept Planet | 1 "Rise above the storm." -\\\> 2a "(continue)" -\\\> 3a "(continue)" -\\\> 4a "Investigate the fungus." -\\\> 5a "(continue)" -\\\> 6 "Negotiate a compromise." |
| Revolutionary Medi-Gel (+25% Medical Worker output) for organic non-Gestalts; otherwise a random Biology (Farming) technology | Entertainment Nexus | 1 "Continue investigations." -\\\> 2 "Very well." -\\\> 3 "A flippant use of impressive technology." -\\\> 4 "An interesting talent." -\\\> 5 "A rare specimen, indeed." -\\\> 6 "Visit the cyborg." -\\\> 7-B "Secure a tissue sample." |
| Rift Fluid Samples (10 years) | The Fluid | 1 "Proceed forward at ease." -\\\> 2/3 "Follow the flow outward." -\\\> 3/4 "Use emergency gasses." \\[fail\\] |
| Rift Fluid Samples (10 years, or 5 if you cut the rig loose) | The Fluid | 1 "Proceed forward at ease." -\\\> 2/3 "Follow the flow outward." -\\\> 3/4 "Pull anchor. Return immediately." |
| Starlight Vanguard + alloys: +10% Armor HP, +10% Armor Hardening | Ruined Planet | Chapter 4-B "Offer alloys." (-100 alloys) -\\\> chapter 5-A -\\\> chapter 7 |
| Starlight Vanguard + astral threads: +10% Shield HP, +10% Shield Hardening | Ruined Planet | Chapter 4-B "Offer astral threads." (-100 threads) -\\\> chapter 5-A -\\\> chapter 7 |
| Starlight Vanguard base: +10% Kinetic Weapon Damage | Ruined Planet | Chapter 2 "Visit the Starlight Vanguard." -\\\> reach chapter 7 by any route |

### **Specimens (Grand Archive)**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Repurposed Cleaning Drone (+25% Planetary Build Speed) | Chemical Wasteland | 1 "Explore the cave." -\\\> 2-B "Autopsy the avian corpse." -\\\> 3/4-A "What happened here?" -\\\> 5-B "Repurpose the drone's technology." |

### **Unlocks**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Flamestorm Troopers | Siege on Paradise | 1 "Contact the orbiting fleet." -\\\> grunur-2 "Let us see where this leads... / The Grunur are dangerous. Be cautious." -\\\> grunur-3 "We are explorers, and we have seen your future." -\\\> grunur-4-known "Share Baol research data with the Grunur." -\\\> grunur-witness "Watch the extermination." |
| Warpling Armies | Abandoned Complex | 1 "Open an egg." -\\\> 2-B "Inject the liquid into the egg." -\\\> 3-B "Inject astral thread." |

### **Technologies**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Next-tier Quantum Firewalls / Quantum Hacking, else a random Computing tech | Chemical Wasteland | 1 "Explore the cave." -\\\> 2-B "Autopsy the avian corpse." -\\\> 3/4-A "What happened here?" -\\\> 5-B "Engineer a virus to disable the sanitation network." |
| Random Society technology (if you confiscate their documents instead) | The Tower | 1 "Attempt to communicate with the creature." -\\\> 2a "Invite them aboard." |
| Wormhole Stabilization if researchable, otherwise 50% progress toward a random Particles technology | Entertainment Nexus | 1 "Continue investigations." -\\\> 2 "Very well." -\\\> 3 "A flippant use of impressive technology." -\\\> 4 "An interesting talent." -\\\> 5 "A rare specimen, indeed." -\\\> 6 "Visit the acrobats." -\\\> 7-A "Tip energy credits." |

### **Species & pops**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| 3 Baol pops (Gaia preference; Venerable, Agrarian, Communal, Delicious, Slow Breeders; Pacifist ethic) | Siege on Paradise | 1 "Contact the planet's inhabitants." -\\\> baol-2 "Disclose what we know of the Baol. / We are explorers." -\\\> baol-3 "We will help however we can." -\\\> baol-4 "Preserve the seedlings." |
| One pop of the new species on a random colony, with the three traits you picked and that colony's climate preference | Genesis | 1 "Arm them with might." -\\\> 2 "Diligence." -\\\> 3 "Preserve the old ways." |

### **Rift deposits**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| \\+10 Physics on the rift | Bleached Planet | 1 "Explore the Terrain." -\\\> 2 "Retreat to the Rift Sphere." -\\\> 3-A "Wait alongside the creatures." -\\\> 5-B "Retreat." |
| \\+10 Society on the rift | Tiny Planet | 1 "(continue)" -\\\> 2 "(continue)" -\\\> 3 "Observe passively." |
| \\+10 Society on the rift | Windswept Planet | 1 "Rise above the storm." -\\\> 2a "(continue)" -\\\> 3a "(continue)" -\\\> 4a "Investigate the fungus." -\\\> 5a "(continue)" -\\\> 6 "Negotiate a compromise." |
| \\+10 Unity and +10 Physics on the rift | The Crystal Rift | 1 "Utilize A.I. to check for hidden patterns." -\\\> 3-B "Preserve the particles." -\\\> 4 "Preserve physics data." -\\\> 5 "Seal it\\\! Quickly\\\!" |
| \\+15 Society on the rift for 10 years | Tiny Planet | 1 "(continue)" -\\\> 2 "(continue)" -\\\> 3 "Establish contact." -\\\> 4 "Destroy the moon." -\\\> 5b "Deploy remote research devices." |
| \\+25 Physics and +25 Engineering on the rift for 10 years | Entangled Dark Matter | 1 "Approach the mass of dark matter." -\\\> 2/3-A "We are explorers. / We are strangers." -\\\> 3/4-A "Deny the proposal. / Deny assimilation." -\\\> 4/5-B "Preserve the captive for study." |
| \\+25 Society research on the rift | Siege on Paradise | 1 "Contact the planet's inhabitants." -\\\> baol-2 "Disclose what we know of the Baol. / We are explorers." -\\\> baol-3 "It is not our place to interfere." -\\\> baol-not-our-fight "Prepare observation satellites." |

### **Diplomacy**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Permanent communications with the Mirror Empire | Strange Station | 1 "Study their people." -\\\> 2-A "Excellent." -\\\> 3 "Welcome friendship between our empires." |

### **Situations**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| The Seal — clearing the Aberrants can yield a legendary paragon, a Luminarium subject, or the Eternal Throne relic | The Crystal Rift | 1 "Utilize A.I. to check for hidden patterns." -\\\> 3-B "Preserve the particles." -\\\> 4 "Preserve physics data." -\\\> 5 "We've opened a doorway." |

### **Systems**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| Azilash: neutral Formless starbase, 8 hostile Aberrant fleets, deposits of 1 astral thread / 10 rare crystals / 10 physics | The Crystal Rift | 1 "Utilize A.I. to check for hidden patterns." -\\\> 3-B "Preserve the particles." -\\\> 4 "Preserve physics data." -\\\> 5 "We've opened a doorway." |

### **Warnings**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| If the Aberrants destroy the Formless first, Azilash goes nova and is lost | The Crystal Rift | 1 "Utilize A.I. to check for hidden patterns." -\\\> 3-B "Preserve the particles." -\\\> 4 "Preserve physics data." -\\\> 5 "We've opened a doorway." |

### **Other**

|  |  |  |
| :-: | :-: | :-: |
| Reward | Rift | Path to it |
| \\+20 Adaptive Evolution and Lithoid DNA if Evolutionary Predators | Rockworms | 1 "Continue surface observations." -\\\> 2 "Sample the microorganisms." -\\\> 3/4/5 "Set explosive charges." |

## **4. Unique rifts**

### **Ruined Planet**

**Requirements:** Astral Planes DLC; Riftworld origin — this rift is always present in the home system of a Riftworld empire and cannot appear anywhere else

**Restrictions:** Genocidal empires cannot visit the Black Curtain

**Notes:** Chapter 7 stacks modifiers from your chapter 4 and chapter 5 choices. Completing it also triggers Formless contact one year later, which hints at The Crystal Rift requirements.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Ruined Planet | — | "Search for remaining survivors." (diff 0) → 2 |
| **2**Opposing Factions | — | "Visit the Black Curtain." (diff 0) → 3 *\\[not Genocidal\\]* *(sets you on the 4-A branch)*"Visit the Starlight Vanguard." (diff 0) → 3 *(sets you on the 4-B branch)* |
| **3**Lost Ancestors | — | "We were engineered?" (diff 0) → 4-A *(goes to 4-A or 4-B depending on your chapter 2 choice)* |
| **4-A**The Black Curtain | — | "Offer resources." (diff 3) → 5-A *cost: -1000 food / minerals / energy* *(grants +0.5 basic resource per job at chapter 7)*"Offer astral threads." (diff 5) → 5-A *cost: -100 Astral Threads* *(grants +25% rift exploration speed and -50% rift fail chance at chapter 7)*"These efforts are hopeless. Let us visit the militants." (diff 1) → 4-B *\\[only if 4-B not yet visited\\]*"This is a lost cause. Return to the new world." (diff 1) → 5-B *\\[only if 4-B already visited\\]* |
| **4-B**The Starlight Vanguard | — | "Offer alloys." (diff 3) → 5-A *cost: -100 Alloys* *(grants +10% armor HP and hardening at chapter 7)*"Offer astral threads." (diff 5) → 5-A *cost: -100 Astral Threads* *(grants +10% shield HP and hardening at chapter 7)*"This war is hopeless. Visit the preservationists." (diff 1) → 4-A *\\[not Genocidal; only if 4-A not yet visited\\]*"This is a lost cause. Return to the new world." (diff 1) → 5-B *\\[Genocidal, or 4-A already visited\\]* |
| **5-A**World Council | — | "Offer astral threads." (diff 3) → 6-A / on failure → 6-B *cost: -100 Astral Threads* *(adds +5% Sublight Speed at chapter 7)*"Offer energy." (diff 3) → 6-A / on failure → 6-B *cost: -1000 Energy* *(adds +5% Ship Build Speed at chapter 7)*"Offer nothing." (diff 6) → 6-A / on failure → 6-B *(no chapter 5 modifier)* |
| **5-B**Abandoning our Ancestors | Large astral threads (140 / 150 / 160)Small Unity*Follow-up: Formless contact one year later hinting at The Crystal Rift.* | *Ends the rift.* |
| **6-A**Celebration | — | "Recruit scientist." (diff 0) → 7 *also grants: Level 3 Scientist with Rift Warped*"Recruit commander." (diff 0) → 7 *also grants: Level 3 Commander with Rift Warped*"Recruit official." (diff 0) → 7 *also grants: Level 3 Official with Rift Warped* |
| **6-B**Devastation | — | "Take as many back as we can." (diff 0) → 7 *also grants: Unity*"Accept the noble's offer." (diff 0) → 7 *also grants: Energy and an aged Official immune to negative traits*"Preserve the library." (diff 0) → 7 *\\[not Genocidal\\]* *also grants: Research and Unity*"Claim their knowledge." (diff 0) → 7 *\\[Genocidal\\]* *also grants: Research and Unity* |
| **7**Spirit of our Ancestors | —*Follow-up: Formless contact one year later hinting at The Crystal Rift.***Black Curtain base: +5% Pop Growth Speed and +5% Habitability****Starlight Vanguard base: +10% Kinetic Weapon Damage****Black Curtain + astral threads: +25% Astral Rift Exploration Speed, -50% Astral Rift Fail Probability****Starlight Vanguard + astral threads: +10% Shield HP, +10% Shield Hardening****Black Curtain + resources: +0.5 basic resource from the matching job category****Starlight Vanguard + alloys: +10% Armor HP, +10% Armor Hardening****Chapter 5 astral threads: +5% Sublight Speed****Chapter 5 energy: +5% Ship Build Speed** | *Ends the rift.* |

### **Genesis**

**Requirements:** Astral Planes DLC; One unique spawn per galaxy; Empire must have at least one colony (the new pop needs somewhere to land)

**Notes:** Every choice is a species-trait pick. The E.M.P. option in chapter 1 is an instant exit that trades the new species for a large alloy payout.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Genesis | Small astral threads (40 / 50 / 60) | "Arm them with might." (diff 3) → 2 *(species gains Strong)*"Plant the seeds of knowledge." (diff 3) → 2 *(species gains Natural Intellectuals)*"We play no games. Activate an E.M.P." (diff 3) → END *(ends the rift immediately)* *also grants: Large astral threads (140 / 150 / 160); 48x Alloys output (700-30,000)* |
| **2**Fruit of Knowledge | Small astral threads (40 / 50 / 60) | "Diligence." (diff 3) → 3 *(species gains Proles)*"Intuition." (diff 3) → 3 *(species gains Ingenious)* |
| **3**To The Stars | Small astral threads (40 / 50 / 60) | "Preserve the old ways." (diff 3) → 4 *(species gains Conservative)*"Challenge every frontier." (diff 3) → 4 *(species gains Starborn)* |
| **4**New Life | Large astral threads (140 / 150 / 160)24x Society research output (500-1,000,000) — Gestalt ConsciousnessGenesis Core specimen \\[Grand Archive DLC\\]**One pop of the new species on a random colony, with the three traits you picked and that colony's climate preference****Genesis Insight (Gestalt Consciousness only)** | *Ends the rift.* |

### **Strange Station**

**Requirements:** Astral Planes DLC; One unique spawn per game

**Restrictions:** Cannot spawn for empires with the Riftworld origin

**Notes:** The Mirror Empire is a permanent contact with mirrored ethics and a standing +150 opinion. It refuses all trades if you are Xenophobic.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Through the Mirror | Small astral threads (40 / 50 / 60) | "Study their people." (diff 2) → 2-A"Study their fleets." (diff 2) → 2-B |
| **2-A**Studying Their People | Small astral threads (40 / 50 / 60) | "Excellent." (diff 1) → 3 *also grants: Moderate Society research (moderate Unity for Gestalts)* |
| **2-B**Studying Their Fleets | Small astral threads (40 / 50 / 60) | "Excellent." (diff 1) → 3 *also grants: Moderate Engineering research (moderate Unity for Gestalts)* |
| **3**Diplomatic Opportunity | Small astral threads (40 / 50 / 60) | "Welcome friendship between our empires." (diff 3) → 4-A"Spurn their offer." (diff 1) → 4-B |
| **4-A**New Friendship | Large Society researchInterdimensional Treaty specimen \\[Grand Archive DLC\\]**+50% Governing Ethics Attraction for 10 years****Permanent communications with the Mirror Empire****Fractured Ambassadors (Gestalt Consciousness only)** | *Ends the rift.* |
| **4-B**Offer Spurned | Medium astral threads (90 / 100 / 110)Large UnityInterdimensional Treaty specimen \\[Grand Archive DLC\\] | *Ends the rift.* |

### **The Microverse**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Notes:** Physics-focused rift. 4-A is the biggest single research payout in the pool but gives no astral threads and cuts the rift short.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Acceleration | 100 Dark Matter | "(continue)" (diff 0) → 2 |
| **2**Shrinking Space | Small astral threads (40 / 50 / 60) | "(continue)" (diff 0) → 3 |
| **3**Temporal Leak | 24x Physics research output (500-1,000,000) | "Synchronize with the fleet." (diff 3) → 4-A"Repolarize the hull." (diff 6) → 4-B *cost: -10 Astral Threads* |
| **4-A**Emergency | 96x Physics research output (2,000-2,000,000)**Scientist becomes 5 years younger** | *Ends the rift.* |
| **4-B**Unbirthing | 24x Physics research output (500-1,000,000) | "Approach the closest star system." (diff 3) → 5-A"Observe from the edge of the universe." (diff 6) → 5-B |
| **5-A**Stardust | Medium astral threads (90 / 100 / 110) | "There may never be another chance." (diff 0) → 6 |
| **5-B**End of the Beginning (Cosmic Horizon) | Small astral threads (40 / 50 / 60)48x Physics research output (1,000-1,000,000) | *Ends the rift.* |
| **6**End of the Beginning (Star) | Small astral threads (40 / 50 / 60)**A Star is Born: +10% Physics research for 10 years** | *Ends the rift.* |

### **Entertainment Nexus**

**Requirements:** Astral Planes DLC; Once per empire per game; Starts from the 'Bright Object Detected' anomaly and costs Energy to investigate

**Notes:** Chapters 1-5 are on rails. Chapter 6 picks the performer, chapter 7 picks tissue sample vs. payment — those two choices alone decide which of the six endings you get.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Come One, Come All | Small astral threads (40 / 50 / 60) | "Continue investigations." (diff 0) → 2 |
| **2**Anticipation | Small astral threads (40 / 50 / 60) | "Very well." (diff 0) → 3 |
| **3**The Vaulting Vulpines | Small astral threads (40 / 50 / 60) | "A flippant use of impressive technology." (diff 0) → 4 |
| **4**The Jaws of Life | Small astral threads (40 / 50 / 60) | "An interesting talent." (diff 0) → 5 |
| **5**The Final Act | Rare Crystals | "A rare specimen, indeed." (diff 0) → 6 |
| **6**After the Show | Small astral threads (40 / 50 / 60) | "Visit the acrobats." (diff 2) → 7-A"Visit the cyborg." (diff 3) → 7-B"Visit the contortionist." (diff 3) → 7-C |
| **7-A**Meet the Acrobats | Small astral threads (40 / 50 / 60) | "Secure a tissue sample." (diff 4) → 8-A"Tip energy credits." (diff 2) → 8-B *cost: -1000 Energy* |
| **7-B**Meet the Cyborg Maw | Small astral threads (40 / 50 / 60) | "Secure a tissue sample." (diff 5) → 8-C"Offer a snack." (diff 2) → 8-D *cost: -1000 Food* |
| **7-C**Meet the Contortionist | Small astral threads (40 / 50 / 60) | "Secure a tissue sample." (diff 6) → 8-E"Tip energy credits." (diff 2) → 8-F *cost: -1000 Energy* |
| **8-A**Extra-Dimensional Genetics | Large astral threads (140 / 150 / 160)Random Biology (Genetics) technologySociety researchWormhole Fur specimen \\[Grand Archive DLC\\] | *Ends the rift.* |
| **8-B**Micro-Wormholes | Large astral threads (140 / 150 / 160)**Wormhole Stabilization if researchable, otherwise 50% progress toward a random Particles technology** | *Ends the rift.* |
| **8-C**Unorthodox Sample Collection | Large astral threads (140 / 150 / 160)Mutative Digestive Fluids specimen \\[Grand Archive DLC\\]**Revolutionary Medi-Gel (+25% Medical Worker output) for organic non-Gestalts; otherwise a random Biology (Farming) technology** | *Ends the rift.* |
| **8-D**Extensive Life Support | Large astral threads (140 / 150 / 160)10% progress toward a random Robotics technology | *Ends the rift.* |
| **8-E**Biological Crystallization | Large astral threads (140 / 150 / 160)Extreme Contortionist DNA specimen \\[Grand Archive DLC\\]**Spontaneous Crystallization (converts 1% of minerals into rare crystals)** | *Ends the rift.* |
| **8-F**Quantum Mineralization | Large astral threads (140 / 150 / 160)Physics research | *Ends the rift.* |

### **The Crystal Rift**

**Requirements:** Astral Planes DLC; Rift Sphere technology; Completed 5 or more astral rifts; Completed more astral rifts than any other empire (ties favour the player / Riftworld origins); Complete the 'Study the Crystal Sphere' situation; An eligible system that is not Sol and contains no wormhole or shroud tunnel

**Restrictions:** Spawns exactly once per game, galaxy-wide

**Notes:** The endgame rift. Sealing it (chapter 6) needs Wormhole Stabilization and costs 500 astral threads; leaving it open spawns the Strange Wormhole to Azilash and the The Seal situation, which is where the paragon / Luminarium / Eternal Throne rewards come from.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Understanding | Small astral threads (40 / 50 / 60) | "Utilize A.I. to check for hidden patterns." (diff 2) → 3-B *(skips chapter 2 and locks out the 3-A ending)*"E.M.P. the anchor cord." (diff 6) → 2 *cost: -1000 Energy* |
| **2**Taking Control | 24x Physics research output (500-1,000,000)Large astral threads (140 / 150 / 160) | "Provide A.I. assistance." (diff 6) → 3-B"Get out\\\! We've only stunned it." (diff 1) → 3-A |
| **3-A**Escape | Large astral threads (140 / 150 / 160)96x Unity output (2,000-2,000,000) | *Ends the rift.* |
| **3-B**Home | Medium astral threads (90 / 100 / 110) | "Preserve the particles." (diff 3) → 4 *also grants: 25% progress toward a random Particles technology*"Preserve field manipulation data." (diff 1) → 4 *also grants: 25% progress toward a random Field Manipulation technology* |
| **4**Ascendance | — | "Preserve physics data." (diff 3) → 5 *also grants: 24x Physics research output (500-1,000,000)*"Preserve society data." (diff 3) → 5 *also grants: 24x Society research output (500-1,000,000)* |
| **5**Shatter | — | "We've opened a doorway." (diff 0) → wormhole"Seal it\\\! Quickly\\\!" (diff 3) → 6 *cost: -500 Astral Threads* *\\[Wormhole Stabilization technology\\]* |
| **6**The Seal | —**+10 Unity and +10 Physics on the rift** | *Ends the rift.* |
| **wormhole**Strange Wormhole (opens the Azilash endgame) | —**Azilash: neutral Formless starbase, 8 hostile Aberrant fleets, deposits of 1 astral thread / 10 rare crystals / 10 physics****The Seal — clearing the Aberrants can yield a legendary paragon, a Luminarium subject, or the Eternal Throne relic****If the Aberrants destroy the Formless first, Azilash goes nova and is lost** | *Ends the rift.* |

## **5. Precursor rifts**

### **Psionic Stranger**

**Requirements:** Astral Planes DLC; Ancient Relics DLC (precursor rift); Tied to the Zroni precursor

**Restrictions:** Fanatic Spiritualists who have not discovered the Zroni cannot pick 'It is a doomed endeavor'; Fanatic Materialists in the same situation cannot pick 'This time, it may be different'

**Notes:** Leads to an alternate universe where the Zroni are still alive. The real payout is the follow-up event 3-5 years after completion.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Psionic Stranger | Small astral threads (40 / 50 / 60) | "Find this being." (diff 0) → 2 |
| **2**The Far-Seer | Small astral threads (40 / 50 / 60) | "Listen to the Far-Seer's words." (diff 0) → 3 |
| **3**The Far-Seer's Burden | Small astral threads (40 / 50 / 60) | "Reveal the fate of the Zroni. / We can only offer our perspective." (diff 6) → 4-A"It is not our place to intervene. / Such spiritual pursuits are trivial." (diff 1) → 4-B |
| **4-B**Leaving it to Fate | Small astral threads (40 / 50 / 60) | "Explore the mineral cache." (diff 0) → 5-B |
| **5-B**Opportunity Strikes | MineralsRare CrystalsLarge astral threads (140 / 150 / 160) | *Ends the rift.* |
| **4-A**Portents of Doom / Certain Fate / Our Perspective | Small astral threads (40 / 50 / 60) | "It is a doomed endeavor. / Advise against interfering with the Shroud." (diff 0) → 5-A *\\[not Fanatic Spiritualist without Zroni discovered\\]* *(sets up the 'A Message from Beyond' follow-up)*"This time, it may be different. / Encourage the Far-Seer to breach the Shroud." (diff 0) → 5-A *\\[not Fanatic Materialist without Zroni discovered\\]* *(sets up the 'The Shroud's Promise' follow-up)* |
| **5-A**Prophetic Advice | 75% progress toward a random Psionics technology (Energy instead for Gestalt and Materialist / Fanatic Materialist empires)*Follow-up: 3-5 years later: 'A Message from Beyond' (75% progress toward a random Particles technology + large astral threads) if you advised against breaching the Shroud; or 'The Shroud's Promise' (Zroni Insight Storm Safeguard — space storm effects halved, +5% Particles research, Energy, Rare Crystals and large astral threads) if you encouraged it.* | *Ends the rift.* |

### **Siege on Paradise**

**Requirements:** Astral Planes DLC; Ancient Relics DLC (precursor rift); Tied to the Baol precursor

**Restrictions:** The Grunur branch changes shape depending on whether you have discovered the Baol precursor

**Notes:** Two mutually exclusive halves: side with the Baol on the planet, or side with the Grunur fleet in orbit. Every ending gives large astral threads.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Siege on Paradise | Small astral threads (40 / 50 / 60) | "Contact the planet's inhabitants." (diff 3) → baol-2"Contact the orbiting fleet." (diff 3) → grunur-2 |
| **baol-2**Meeting the Baol / Plantoid Encounter | Small astral threads (40 / 50 / 60) | "Disclose what we know of the Baol. / We are explorers." (diff 0) → baol-3 |
| **baol-3**Impending Doom / A Request for Aid | Small astral threads (40 / 50 / 60) | "We will help however we can." (diff 3) → baol-4"It is not our place to interfere." (diff 1) → baol-not-our-fight |
| **baol-not-our-fight**Not Our Fight | Small astral threads (40 / 50 / 60) | "Prepare observation satellites." (diff 0) → baol-ashes |
| **baol-ashes**Ashes to Ashes | —*Follow-up: 2-4 years later the 'Dust to Dust' event gives Society and Engineering research and removes the deposit.***+25 Society research on the rift** | *Ends the rift.* |
| **baol-4**Saving the Baol / Considering Options | Small astral threads (40 / 50 / 60) | "Genetically modify the Baol." (diff 6) → baol-genetic *\\[Gene Tailoring technology\\]*"Deploy experimental planetary cloaking." (diff 6) → baol-cloak *cost: -50 Astral Threads* *\\[Basic Cloaking Fields technology\\]*"Generate an astral shield." (diff 6) → baol-shield *cost: -100 Astral Threads* *\\[unavailable if you have both Gene Tailoring and Basic Cloaking Fields\\]*"Preserve the seedlings." (diff 2) → baol-life |
| **baol-genetic**Genetic Reinforcement | Large astral threads (140 / 150 / 160)**Option to recruit the paragon Oakenstalk** | *Ends the rift.* |
| **baol-cloak**Under the Radar | Large astral threads (140 / 150 / 160)**Astral Cloaking (+1 Cloaking Strength while active)** | *Ends the rift.* |
| **baol-shield**Astral Shield | Large astral threads (140 / 150 / 160)**Astral Shield Experimentation: +5% Shield HP, +5% Shield Hardening** | *Ends the rift.* |
| **baol-life**Life Finds a Way | Large astral threads (140 / 150 / 160)**3 Baol pops (Gaia preference; Venerable, Agrarian, Communal, Delicious, Slow Breeders; Pacifist ethic)** | *Ends the rift.* |
| **grunur-2**Flagship Escort | Small astral threads (40 / 50 / 60) | "Let us see where this leads... / The Grunur are dangerous. Be cautious." (diff 0) → grunur-3 |
| **grunur-3**A Unique Conversation | Small astral threads (40 / 50 / 60) | "We are explorers, and we have seen your future." (diff 0) → grunur-4-known *\\[Baol precursor discovered\\]*"We are explorers." (diff 0) → grunur-4-unknown *\\[Baol precursor not discovered\\]* |
| **grunur-4-known**The Infamous Grunur (Baol precursor discovered) | Small astral threads (40 / 50 / 60) | "Share rare military technology with the Grunur." (diff 6) → grunur-sharing *\\[a rare technology such as Artificial Dragonscales, Dark Matter Propulsion or Jump Drive\\]*"Share Baol research data with the Grunur." (diff 4) → grunur-witness"Refuse to co-operate." (diff 2) → grunur-end |
| **grunur-4-unknown**A Meek Introduction (Baol precursor not discovered) | Small astral threads (40 / 50 / 60) | "Respond with bravado. Do not be intimidated." (diff 1) → grunur-stand"Attempt to reason with them." (diff 1) → grunur-punish |
| **grunur-sharing**Sharing of Knowledge | 25% progress toward a random Military Theory technology | "A worthy exchange." (diff 0) → grunur-weapons |
| **grunur-witness**Bearing Witness | Small astral threads (40 / 50 / 60) | "Watch the extermination." (diff 4) → grunur-burn"Refuse." (diff 1) → grunur-end |
| **grunur-stand**Taking a Stand | Small astral threads (40 / 50 / 60) | "Press the crystal. Order the launch." (diff 4) → grunur-burn"Refuse." (diff 1) → grunur-end |
| **grunur-punish**Punishment | Small astral threads (40 / 50 / 60) | "Remain strong. We will find a way to recover you." (diff 0) → grunur-end |
| **grunur-weapons**Grunur Weapons Interface | Large astral threads (140 / 150 / 160)**Grunur Weapons Interface: +10% Ship Fire Rate** | *Ends the rift.* |
| **grunur-burn**Watching a World Burn | Large astral threads (140 / 150 / 160)24x Society research output (500-1,000,000)**Flamestorm Troopers** | *Ends the rift.* |
| **grunur-end**Expedition's End | Large astral threads (140 / 150 / 160)24x Engineering research output (500-1,000,000)*Scientist is lost for 5-7 years**Follow-up: The leader returns with Rift Warped and gains Expertise: Propulsion I (or Expertise: Voidcraft I if they already have it).* | *Ends the rift.* |

## **6. General rifts**

### **Abandoned Complex**

**Requirements:** Astral Planes DLC; Rift Sphere technology; Rift inside empire borders; Scientist + science ship assigned

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Abandoned Facility | Small astral threads (40 / 50 / 60) | "Search for the caretakers." (diff 2) → 2-A"Open an egg." (diff 4) → 2-B |
| **2-A**The Caretakers | Small astral threads (40 / 50 / 60) | "Open an egg." (diff 4) → 2-B"Return with the remains." (diff 2) → 3-A |
| **2-B**Quantum Parasites | Small astral threads (40 / 50 / 60) | "Inject the liquid into the egg." (diff 3) → 3-B / on failure → 4-B"Euthanize the remaining creatures." (diff 3) → 3-C |
| **3-A**Return With the Remains | Large astral threads (140 / 150 / 160) | *Ends the rift.* |
| **3-B**Metabolization | 12x Society research output (250-100,000) | "Do not intervene." (diff 1) → 4-B"Inject astral thread." (diff 5) → 4-A |
| **3-C**Euthanized | Large astral threads (140 / 150 / 160)48x Physics research output (1,000-1,000,000)Reptilian DNA if Evolutionary Predators is active | *Ends the rift.* |
| **4-A**Biological Weapon | Large astral threads (140 / 150 / 160)**Warpling Armies** | *Ends the rift.* |
| **4-B**Biological Instability | Large astral threads (140 / 150 / 160)24x Physics research output (500-1,000,000)*Scientist dies within 1 month* | *Ends the rift.* |

### **Bleached Planet**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Ashen Environment | Small astral threads (40 / 50 / 60) | "Explore the Terrain." (diff 3) → 2 |
| **2**Bleached Landscape | 24x Society research output (500-1,000,000) | "Retreat to the Rift Sphere." (diff 2) → 3-A"Prepare for contact." (diff 2) → 3-B |
| **3-A**Rock Creatures (from above) | Small astral threads (40 / 50 / 60) | "Fly towards the distant horizon." (diff 3) → 5-A *(forces the 6-A ending)*"Wait alongside the creatures." (diff 1) → 5-B |
| **3-B**Rock Creatures | 18x Society research output (350-100,000) | "Examine a rock creature." (diff 5) → 4"Wait alongside the creatures." (diff 1) → 5-B |
| **4**Bio-Geology | 25% progress toward a random Biology technology | "Retreat to the Rift Sphere." (diff 1) → 5-B |
| **5-A**Darkest Dawn | Small astral threads (40 / 50 / 60) | "Continue your observations." (diff 1) → 6-A"Turn away\\\!" (diff 1) → 6-A |
| **5-B**Darkest Before the Dawn | Small astral threads (40 / 50 / 60) | "Observe the dark star." (diff 3) → 6-A"Retreat." (diff 1) → 6-B |
| **6-A**Black Light Blinded | Large astral threads (140 / 150 / 160)**Spark of Genius****Black Light Blinded** | *Ends the rift.* |
| **6-B**Further Observations | Large astral threads (140 / 150 / 160)**+10 Physics on the rift** | *Ends the rift.* |

### **Chemical Wasteland**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Chemically Cleansed | Small astral threads (40 / 50 / 60) | "Investigate the robots." (diff 4) → 2-A *(locks you into endings 6-A / 6-B / 6-C)*"Explore the cave." (diff 4) → 2-B *(locks you into endings 6-D / 6-E / 6-F)* |
| **2-A**Drone Encounter | 18x Engineering research output (350-100,000) | "Allow the drones to approach." (diff 2) → 3-A *(prevents ending 6-C)*"Disable them." (diff 6) → 3-B |
| **2-B**Signs of Life | Small astral threads (40 / 50 / 60) | "Autopsy the avian corpse." (diff 5) → 3/4-A"Reactivate the drone." (diff 5) → 3/4-B |
| **3-A**Clean Shot | Small astral threads (40 / 50 / 60) | "Follow the drones." (diff 2) → 4-A |
| **3-B**Disabled Drones | Small astral threads (40 / 50 / 60) | "Trace the distress signal." (diff 5) → 4-A"Flee before potential reinforcements arrive." (diff 2) → 6-C |
| **3/4-A**Avian Autopsy | 25% progress toward a random Biology technology | "Reactivate the drone." (diff 4) → 3/4-B *\\[only if 3/4-B not yet done\\]*"What happened here?" (diff 6) → 5-B *\\[both branches done; not Evolutionary Predators\\]*"Retrieve the avian specimen." (diff 6) → 5-B *\\[both branches done; Evolutionary Predators\\]* *also grants: Avian DNA + 10 Adaptive Evolution* |
| **3/4-B**Drone Repaired | 18x Engineering research output (350-100,000) | "Examine the avian corpse." (diff 4) → 3/4-A *\\[only if 3/4-A not yet done\\]*"What happened here?" (diff 6) → 5-B *\\[both branches done; not Evolutionary Predators\\]*"Retrieve the avian specimen." (diff 6) → 5-B *\\[both branches done; Evolutionary Predators\\]* *also grants: Avian DNA + 10 Adaptive Evolution* |
| **4-A**Signs of the Makers | Small astral threads (40 / 50 / 60) | "Explore the lab." (diff 4) → 5-A |
| **5-A**Scrubbed History | 25% progress toward a random Computing technology | "Document and study the sanitary infrastructure." (diff 2) → 6-A *\\[Biological or Lithoid; not Wilderness\\]*"Shut down the Facility." (diff 5) → 6-B *\\[Biological or Lithoid\\]*"Fascinating." (diff 5) → 6-B *\\[not Biological or Lithoid\\]* |
| **5-B**Hygienic Hypothesis | 18x Society research output (350-100,000) | "Repurpose the drone's technology." (diff 4) → 6-D"Engineer a virus to disable the sanitation network." (diff 6) → 6-E"Keep this drone as a personal research assistant." (diff 3) → 6-F *\\[not Gestalt Consciousness\\]* |
| **6-A**Automated Disinfection | Large astral threads (140 / 150 / 160)24x Society research output (500-1,000,000) — Gestalt Consciousness**Automated Disinfection** | *Ends the rift.* |
| **6-B**Shut Down the Facility | Large astral threads (140 / 150 / 160)24x Energy output (350-10,000)48x Energy output (700-30,000) — Barbaric Despoilers or Genocidal (replaces the smaller energy reward) | *Ends the rift.* |
| **6-C**A Clean Escape | Large astral threads (140 / 150 / 160)18x Alloys output (250-5,000) | *Ends the rift.* |
| **6-D**Repurposing the Drone | Large astral threads (140 / 150 / 160)**Colonization Drones (+25% colony development speed, +25% clear blocker speed)****Repurposed Cleaning Drone (+25% Planetary Build Speed)** | *Ends the rift.* |
| **6-E**Viral Irony | Large astral threads (140 / 150 / 160)**Next-tier Quantum Firewalls / Quantum Hacking, else a random Computing tech** | *Ends the rift.* |
| **6-F**Never Alone with a Drone | Large astral threads (140 / 150 / 160)**Sanitary Drone Assistant** | *Ends the rift.* |

### **Desert Ruins**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Notes:** A button-puzzle rift. Every wrong button adds +1 to a hidden 'time' counter; 3 or more wrong answers sends you to the bad ending (7-B). Toxoid species are immune to the triangle-button penalty and Aquatic/Waterproof species are immune to the four-dot flood penalty.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Strange Console | Small astral threads (40 / 50 / 60) | "Fascinating." (diff 1) → 2 |
| **2**Lost Contact | Small astral threads (40 / 50 / 60) | "Let's hope for the best." (diff 1) → 3 |
| **3**Outer Ruins | Small astral threads (40 / 50 / 60) | "Weren't they lost?" (diff 1) → 4-A |
| **4-A**A Choice | Small astral threads (40 / 50 / 60) | "Press the blue button." (diff 3) → 5-A *(CORRECT)*"Press the green button." (diff 3) → 4-B *(WRONG, +1 time)* |
| **4-B**The Wrong Button | Small astral threads (40 / 50 / 60) | "Green was the wrong choice..." (diff 1) → 4-C |
| **4-C**The Blue Button | — | "Press the blue button." (diff 1) → 5-A |
| **5-A**The Second Chamber | Small astral threads (40 / 50 / 60) | "Press the pentagon button." (diff 3) → 6-A *(CORRECT)*"Press the triangle button." (diff 3) → 5-B *(WRONG, +1 time unless Toxoid)* |
| **5-B**Wrong Button | Small astral threads (40 / 50 / 60) | "Unfortunate." (diff 1) → 5-C *\\[not Toxoid\\]*"Fortunate." (diff 1) → 6-A *\\[Toxoid\\]* |
| **5-C**The Second Chamber | Small astral threads (40 / 50 / 60) | "Press the pentagon button." (diff 3) → 6-A |
| **6-A**The Third Chamber | Small astral threads (40 / 50 / 60) | "Press the button with six dots." (diff 3) → 7-A *(CORRECT)*"Press the button with four dots." (diff 3) → 6-B *(WRONG, +1 time unless Aquatic/Waterproof)* |
| **6-B**Flood | — | "Fortunate." (diff 1) → 7-A *\\[Aquatic or Waterproof\\]*"Unfortunate." (diff 3) → 6-C *\\[not Aquatic/Waterproof; fewer than 3 wrong buttons so far\\]*"Unfortunate." (diff 3) → 7-B *\\[not Aquatic/Waterproof; 3 or more wrong buttons — you run out of time\\]* |
| **6-C**The Third Chamber | Small astral threads (40 / 50 / 60) | "Press the button with six dots." (diff 3) → 7-A |
| **7-A**Time Crystal | Astral threads scaled to how few mistakes you made (roughly 50 / 100 / 150)**Time Crystal****Psychic (if the leader has Latent Psionic)** | *Ends the rift.* |
| **7-B**Trapped in Time | Large astral threads (140 / 150 / 160)*Scientist dies* | *Ends the rift.* |

### **Dimensional Conflict**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**An Ancient Battle | Small astral threads (40 / 50 / 60) | "Study its composition." (diff 2) → 2-A"Let's get in there." (diff 3) → 2-B |
| **2-A**Exotic Armor | 6x Alloys output (100-1,000)Leviathan Scale specimen \\[Grand Archive DLC\\] | "Fascinating." (diff 1) → 3 |
| **2-B**Uncharted Body | 25% progress toward a random Biology technology | "Fascinating." (diff 1) → 3 |
| **3**A Dozen Faces | Medium astral threads (90 / 100 / 110) | "Try to activate the dodecahedron." (diff 6) → 4-A"Strip it for parts." (diff 2) → 4-B |
| **4-A**Activation | No astral threads**Daedalus Seal** | *Ends the rift.* |
| **4-B**Disassembly | Large astral threads (140 / 150 / 160)24x Dark Matter output (350-10,000) | *Ends the rift.* |

### **Dimensional Dump**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** Some options are closed to Barbaric Despoilers and Genocidal empires

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Floating Body | Small astral threads (40 / 50 / 60) | "Bring it aboard and give aid." (diff 3) → 2 *\\[not Barbaric Despoilers; not Genocidal\\]*"Bring it aboard and recover its gear." (diff 3) → 2 *(adds an engineering payout to ending 3-A)* |
| **2**Floating Body | Small astral threads (40 / 50 / 60) | "Dispatch the individual." (diff 6) → 3-A *(can fail if you chose 'give aid' in chapter 1)*"Attempt to negotiate." (diff 3) → 3-B *\\[not Barbaric Despoilers; not Genocidal\\]* |
| **3-A**Floating Body (dispatched) | Medium astral threads (90 / 100 / 110)24x Minerals output (350-10,000)24x Alloys output (350-10,000)96x Engineering research output (2,000-2,000,000) — only if you chose 'recover its gear' in chapter 1*On failure: scientist is killed; you still get large astral threads and alloys* | *Ends the rift.* |
| **3-B**De-escalation | Small astral threads (40 / 50 / 60) | "(continue)" (diff 1) → 4 |
| **4**Lost Junker | Large astral threads (140 / 150 / 160)24x Society research output (500-1,000,000)**Level 6 Commander with the Rift Warped trait (arrives after 1 year)** | *Ends the rift.* |

### **Entangled Dark Matter**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** The 'offer the scientist as a vessel' path is closed to Egalitarian empires

**Notes:** Chapter numbering shifts by one depending on whether you took the shortcut in chapter 1, hence the 'x/y' node ids.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Strange Mesh | 6x Dark Matter output (100-1,000) | "Examine the mesh." (diff 2) → 2"Approach the mass of dark matter." (diff 2) → 2/3-A |
| **2**Limited Current | 18x Engineering research output (350-100,000) | "Remove the device." (diff 4) → 3-A"Investigate the captive mass." (diff 2) → 2/3-A |
| **2/3-A**Telepathic Communication / Communications Established | Small astral threads (40 / 50 / 60) | "We are explorers. / We are strangers." (diff 1) → 3/4-A |
| **3-A**Unlimited Current | Large astral threads (140 / 150 / 160)48x Dark Matter output (700-30,000) | *Ends the rift.* |
| **3/4-A**An Ominous Proposal | Small astral threads (40 / 50 / 60) | "Offer this scientist as a vessel. / Assimilate the entity." (diff 3) → 4/5-A *\\[not Egalitarian; difficulty 2 and cannot fail if the scientist is Psychic\\]*"Deny the proposal. / Deny assimilation." (diff 2) → 4/5-B |
| **4/5-A**Absorbed Consciousness | Large astral threads (140 / 150 / 160)*On failure (Unfortunate Complications): you get large astral threads and dark matter instead of the traits***Psychic + Planar Theorist + Riftwalker + Foreign Consciousness + Resilient on the scientist (upgraded versions if already Psychic)****Foreign Consciousness (+5% research) for Gestalt empires** | *Ends the rift.* |
| **4/5-B**A Prisoner's Plea | Small astral threads (40 / 50 / 60) | "Euthanize the ethereal creature." (diff 2) → 5/6-A *\\[not Barbaric Despoilers; not Genocidal\\]*"Kill it." (diff 2) → 5/6-A *\\[Barbaric Despoilers or Genocidal\\]*"Preserve the captive for study." (diff 3) → 5/6-B |
| **5/6-A**Compassion / Extermination | Large astral threads (140 / 150 / 160)48x Dark Matter output (700-30,000) | *Ends the rift.* |
| **5/6-B**Life in a Cage | Large astral threads (140 / 150 / 160)**+25 Physics and +25 Engineering on the rift for 10 years** | *Ends the rift.* |

### **Hatching Ground**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Giant Eggs | Small astral threads (40 / 50 / 60) | "Fascinating." (diff 2) → 2 |
| **2**Star Drinkers | Small astral threads (40 / 50 / 60) | "Get closer." (diff 6) → 3-A"Maintain a safe distance." (diff 2) → 3-B |
| **3-A**Friendly Hatchlings | Small astral threads (40 / 50 / 60) | "They are comparable to our ships\\\!" (diff 2) → 4-A *also grants: 48x Society research (organic shipset) or 48x Engineering research (mechanical shipset)*"Neither Avian nor Arthropoid. Very peculiar." (diff 2) → END *(ends the rift early)* *also grants: Medium DNA reward; 48x Engineering research output (1,000-1,000,000)* |
| **3-B**Solar Sailing | Small astral threads (40 / 50 / 60)Lonely Planet empire modifier: +15% Propulsion for 15 years | "Impressive." (diff 2) → 4-B |
| **4-A**Astral Spawning | Large astral threads (140 / 150 / 160)18x Unity output (250-1,000,000) | *Ends the rift.* |
| **4-B**Astral Migration | Large astral threads (140 / 150 / 160)18x Unity output (250-1,000,000) | *Ends the rift.* |

### **Lone Object**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Floating Mystery | Small astral threads (40 / 50 / 60) | "Attempt to translate the glyphs." (diff 4) → 2"Scan its entire perimeter." (diff 2) → 2/3 |
| **2**Millions of Glyphs | 18x Society research output (350-100,000) | "Scan its entire perimeter." (diff 2) → 2/3"Blast it open." (diff 6) → 3/4/5-success / on failure → 3/4/5-fail |
| **2/3**An Ancient Seal | Small astral threads (40 / 50 / 60) | "Send a drone through the crack." (diff 2) → 3/4"Blast it open." (diff 6) → 3/4/5-success / on failure → 3/4/5-fail |
| **3/4**Clouded Passageways | Medium astral threads (90 / 100 / 110) | "Take samples and return." (diff 1) → END *(safe exit, ends the rift)*"Engage destructive exploration." (diff 6) → 3/4/5-success / on failure → 3/4/5-fail *also grants: Large astral threads (140 / 150 / 160)* |
| **3/4/5-success**Tomb Raiding (success) | 12x Minerals output (150-2,000)6x Alloys output (100-1,000)500 Rare Crystals12x Unity output (150-100,000)Medium astral threads (90 / 100 / 110)Random Psionics technology if the leader is Psychic | *Ends the rift.* |
| **3/4/5-fail**Grave Guardians (failure) | —*Spawns a hostile fleet of 10-30 Crystalline entity ships (scales toward endgame)* | *Ends the rift.* |

### **Rockworms**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** The explosive-charge option needs Exotic Gas Refining or 100 stored Exotic Gases

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Endless Rock | Small astral threads (40 / 50 / 60) | "Continue surface observations." (diff 2) → 2"Explore the tunnels." (diff 5) → 2/3 |
| **2**Sky Plankton | 15% progress toward a random Biology technology | "Sample the microorganisms." (diff 2) → 3/4/5"Explore the worms' tunnels." (diff 5) → 2/3 *(can fail)* |
| **2/3**Tunnels | Small astral threads (40 / 50 / 60) | "Harvest the eggs." (diff 5) → 3/4/5"Proceed onward." (diff 2) → 3/4 |
| **3/4**The Nursery | Small astral threads (40 / 50 / 60) | "Capture a live specimen." (diff 5) → 3/4/5"We've pushed our luck..." (diff 1) → END *(safe exit, ends the rift)* *also grants: 6x Unity output (100-100,000); 15% Biology tech progress; +20 Adaptive Evolution and Lithoid DNA if Evolutionary Predators* |
| **3/4/5**Swallowed | Small astral threads (40 / 50 / 60) | "Pull emergency anchor." (diff 1) → 4/5/6-A"Set explosive charges." (diff 2) → 4/5/6-B / on failure → 4/5/6-B-fail *cost: -100 Exotic Gases* *\\[Exotic Gas Refining or stored Exotic Gases\\]* |
| **4/5/6-A**Pulled Free | Large astral threads (140 / 150 / 160) | *Ends the rift.* |
| **4/5/6-B**Rupture (success) | Large astral threads (140 / 150 / 160)**Rockworm Hive planetary decision****+20 Adaptive Evolution and Lithoid DNA if Evolutionary Predators** | *Ends the rift.* |
| **4/5/6-B-fail**Digested (failure) | Small astral threads (40 / 50 / 60)15% progress toward a random Biology technology*Scientist dies and returns a year later with the Partially Digested trait* | *Ends the rift.* |

### **Subnautical**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** The communication branch is closed to Barbaric Despoilers and Genocidal empires

**Notes:** All three endings give the Celestial Tear; the only difference is how much Society research comes with it. 6-C is the best payout.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Submerged | Small astral threads (40 / 50 / 60) | "Dive deeper." (diff 1) → 2"Head to the surface." (diff 1) → 2 |
| **2**Unexpected Results | Small astral threads (40 / 50 / 60) | "Activate the engines." (diff 2) → 3-A"Don pressure suits. We swim." (diff 5) → 3-B *\\[difficulty drops to 2 if Aquatic or Waterproof\\]* |
| **3-A**A Planet-Sized Bubble | Small astral threads (40 / 50 / 60) | "Interesting." (diff 1) → 4 |
| **3-B**We Swim | Medium astral threads (90 / 100 / 110) | "Fascinating." (diff 1) → 4 |
| **4**Planetoid Bubbles | Small astral threads (40 / 50 / 60)18x Physics research output (350-100,000) | "Try to communicate." (diff 6) → 5-A"Approach the object." (diff 2) → 5-B |
| **5-A**Communication | Small astral threads (40 / 50 / 60) | "Greetings." (diff 1) → 6-A"What are you?" (diff 3) → 6-B"Do you need help?" (diff 6) → 6-C |
| **5-B**The Approach | Small astral threads (40 / 50 / 60)18x Physics research output (350-100,000) | "Get closer..." (diff 3) → 6-A |
| **6-A**Awakening | Small astral threads (40 / 50 / 60)24x Society research output (500-1,000,000)**Celestial Tear** | *Ends the rift.* |
| **6-B**Awakening | Small astral threads (40 / 50 / 60)48x Society research output (1,000-1,000,000)**Celestial Tear** | *Ends the rift.* |
| **6-C**Awakening | Small astral threads (40 / 50 / 60)96x Society research output (2,000-2,000,000)**Celestial Tear** | *Ends the rift.* |

### **The Advisor**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**A Familiar Place | Small astral threads (40 / 50 / 60) | "Ask for assistance." (diff 1) → 2"Disable this thing." (diff 3) → 2/3 |
| **2**Assisting the Assistant | Small astral threads (40 / 50 / 60) | "Ask for FURTHER assistance." (diff 1) → 3/4-A"Disable this thing." (diff 3) → 2/3 |
| **2/3**Unable to Disable | Small astral threads (40 / 50 / 60) | "Placate the machine." (diff 1) → 3/4-A"Discharge an electromagnetic pulse." (diff 6) → 3/4-B |
| **3/4-A**Further 'Assistance' | —*Scientist disappears and returns in 5 years with Rift Warped plus a random trait* | *Ends the rift.* |
| **3/4-B**Electromagnetic Pulse | 24x Engineering research output (500-1,000,000) | "Attempt to recover its core." (diff 6) → 4/5-A"Destroy the machine completely." (diff 2) → 4/5-B |
| **4/5-A**Scrapping the Machine | Large astral threads (140 / 150 / 160)18x Alloys output (250-5,000)20% progress toward a random Computing technology**Advisor Core** | *Ends the rift.* |
| **4/5-B**Good Riddance | 24x Engineering research output (500-1,000,000) | *Ends the rift.* |

### **The Corridors**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Corridors | Small astral threads (40 / 50 / 60) | "Break through the floor." (diff 4) → 2-A"Open the walls." (diff 2) → 2-B |
| **2-A**Impossible "Glass" | Small astral threads (40 / 50 / 60) | "Fascinating." (diff 1) → 3 |
| **2-B**Regeneration | 18x Physics research output (350-100,000) | "Fascinating." (diff 1) → 3 |
| **3**The Terminal | — | "Hack it." (diff 6) → 4-A / on failure → 4-A-fail"Strip it for parts." (diff 2) → 4-B |
| **4-A**A Formula (success) | —**Procedural Space (+1 district, +1 branch office)** | *Ends the rift.* |
| **4-A-fail**Entombed (failure) | —*Scientist returns in 5 years with Rift Warped plus a random trait* | *Ends the rift.* |
| **4-B**Astral Computer | Large astral threads (140 / 150 / 160) | *Ends the rift.* |

### **The Fluid**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** Emergency-gas options need Exotic Gas Refining or stored Exotic Gases

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**The Fluid | Small astral threads (40 / 50 / 60) | "Deploy sample collection rig." (diff 5) → 2"Proceed forward at ease." (diff 2) → 2/3 |
| **2**Snagged | Small astral threads (40 / 50 / 60) | "Cut it loose. The risk isn't worth it." (diff 2) → 2/3 *(shortens the Rift Fluid Samples modifier to 5 years)*"Use emergency gasses." (diff 2) → 2/3 *cost: -50 Exotic Gases* *\\[Exotic Gas Refining or stored Exotic Gases\\]* |
| **2/3**The Chamber | Small astral threads (40 / 50 / 60)Dimensional Endothelial Lining specimen \\[Grand Archive DLC\\] | "Follow the flow outward." (diff 2) → 3/4 *also grants: +200 Exotic Gases if you spent gases earlier*"Explore the crystalline orifice." (diff 5) → 3/4 *also grants: +200 Rare Crystals if you spent gases earlier* |
| **3/4**The Blob | Small astral threads (40 / 50 / 60) | "Pull anchor. Return immediately." (diff 1) → 4/5-A"Use emergency gasses." (diff 6) → 4/5-B / on failure → 4/5-B-fail *cost: -100 Exotic Gases* *\\[Exotic Gas Refining or stored Exotic Gases\\]* |
| **4/5-A**Extraction | Large astral threads (140 / 150 / 160)**Rift Fluid Samples (10 years, or 5 if you cut the rig loose)** | *Ends the rift.* |
| **4/5-B**Dissolution (success) | Large astral threads (140 / 150 / 160)**Plasmic Core** | *Ends the rift.* |
| **4/5-B-fail**Dissolved (failure) | Large astral threads (140 / 150 / 160)*Scientist and science ship are destroyed***Rift Fluid Samples (10 years)** | *Ends the rift.* |

### **The Garden**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Notes:** Nodes are named rather than numbered on the wiki. The Infinity Root relic is the prize; getting it requires burning the creature (or surviving three rounds of study).

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **thorns**Thorns | Small astral threads (40 / 50 / 60) | "Burn the weeds." (diff 2) → hollow"Extract the fruit." (diff 5) → hollow / on failure → entangled |
| **entangled**Entangled | Small astral threads (40 / 50 / 60) | "Burn the entangling vines." (diff 5) → hollow / on failure → conflagration"Pull anchor. Escape." (diff 1) → escape |
| **conflagration**Conflagration | Large astral threads (140 / 150 / 160) | *Ends the rift.* |
| **hollow**The Hollow | 25% progress toward a random Biology technology if nothing was burnt, otherwise small astral threads | "Burn it all." (diff 2) → creature"Study this place." (diff 4) → creature *also grants: Symbiotic Fruit specimen \\[Grand Archive DLC\\]* |
| **creature**A Creature | Small astral threads (40 / 50 / 60) | "Burn the Creature." (diff 6) → infinity\\_root / on failure → plant\\_material *\\[difficulty drops to 1 if you successfully studied the Hollow\\]*"Continue Studies." (diff 5) → continued\\_studies *\\[only after a successful 'Study this place'\\]*"Escape." (diff 2) → escape"Do nothing." (diff 1) → plant\\_material *\\[only if you chose 'Burn it all'\\]* |
| **continued\\_studies**Continued Studies | Small astral threads (40 / 50 / 60) | "Continued Studies." (diff 5) → continued\\_studies\\_2 / on failure → noticed |
| **continued\\_studies\\_2**Continued Studies (second round) | Small astral threads (40 / 50 / 60) | "Continued Studies." (diff 5) → infinity\\_root / on failure → noticed |
| **noticed**Noticed | Small astral threads (40 / 50 / 60) | "Escape." (diff 3) → escape"Burn the Creature." (diff 6) → infinity\\_root / on failure → plant\\_material |
| **infinity\\_root**Infinity Root | —**Infinity Root****Plantoid leader** | *Ends the rift.* |
| **plant\\_material**Plant Material | Medium astral threads (90 / 100 / 110)25% progress toward a random Biology technology*Scientist dies and returns as a plantoid in 5 years* | *Ends the rift.* |
| **escape**Escape | Large astral threads (140 / 150 / 160)25% progress toward a random Biology technology | *Ends the rift.* |

### **The Lattice**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Strange Geometry | Small astral threads (40 / 50 / 60) | "Explore further." (diff 3) → 2-A"Stay put. Study the surroundings." (diff 2) → 2-B |
| **2-A**Multi-Dimensional Patterns | Small astral threads (40 / 50 / 60) | "Continue your investigations." (diff 1) → 3 |
| **2-B**Multi-Dimensional Analysis | Small astral threads (40 / 50 / 60) | "Study further." (diff 1) → 3 |
| **3**Message in a Bottle | Small astral threads (40 / 50 / 60) | "Can it be trusted?" (diff 1) → 4 |
| **4**Time Traveling | Small astral threads (40 / 50 / 60) | "Unsettling..." (diff 3) → 5 |
| **5**Fractal Seeds | — | "Retrieve the globes." (diff 6) → 6-A"We are done here." (diff 2) → 6-B |
| **6-A**Dimensional Containers | Large astral threads (140 / 150 / 160)**9 Fractal Seed planetary decisions** | *Ends the rift.* |
| **6-B**Close Encounters | Large astral threads (140 / 150 / 160)**3 Fractal Seed planetary decisions** | *Ends the rift.* |

### **The Mechanism**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Notes:** Shortest path to a relic in the whole general pool: two choices. Jamming the gears has a 1.5% failure chance per roll.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Gears and Pinions | Small astral threads (40 / 50 / 60) | "(continue)" (diff 1) → 2 |
| **2**Dimensional Machine | 18x Engineering research output (350-100,000) | "Interfering would be irresponsible." (diff 1) → 4a"Jam the gears." (diff 6) → 3 |
| **3**Jammed | Medium astral threads (90 / 100 / 110) | "(roll)" → 4c / on failure → 4b *(1.5% failure chance per roll)* |
| **4a**If It Ain't Broke... | 96x Engineering research output (2,000-2,000,000)Large astral threads (140 / 150 / 160) | *Ends the rift.* |
| **4b**Shatter | 96x Engineering research output (2,000-2,000,000)Large astral threads (140 / 150 / 160)*Scientist ages 20 years* | *Ends the rift.* |
| **4c**Success | —**The Continuum — passive +5% Energy, Minerals, Food, Alloys, Consumer Goods and Research Speed; active grants a large lump of every resource** | *Ends the rift.* |

### **The Tower**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** Homicidal (genocidal) and Barbaric Despoiler empires get the 'Kill it' branch instead of the diplomatic ones

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**The Tower | Small astral threads (40 / 50 / 60) | "Attempt to communicate with the creature." (diff 5) → 2a *\\[not Homicidal; not Barbaric Despoilers\\]*"Observe the creature and report back." (diff 1) → 2b"Kill it." (diff 5) → 3 *\\[Homicidal or Barbaric Despoilers\\]* |
| **2a**Binary Communication | 18x Society research output (350-100,000) | "Invite them aboard." (diff 6) → 4a"Offer something in return." (diff 2) → 4b *cost: -100 Alloys*"Leave the site." (diff 0) → 4c |
| **2b**A Long Awaited Welcome | Small astral threads (40 / 50 / 60) | "Invite them aboard." (diff 6) → 4a *\\[not Homicidal; not Barbaric Despoilers\\]*"Offer something in return." (diff 2) → 4b *cost: -100 Alloys* *\\[not Homicidal; not Barbaric Despoilers\\]*"Leave the site." (diff 0) → 4c"Kill the creature." (diff 5) → 3 *\\[Homicidal or Barbaric Despoilers\\]* |
| **3**Fish in a Barrel | 48x Unity output (1,000-1,000,000) | "(continue)" (diff 0) → 4c |
| **4a**Playing Host | —**New scientist in 1 year with Society Focus + Increased Lifespan (if invited to your empire)****Random Society technology (if you confiscate their documents instead)** | *Ends the rift.* |
| **4b**Reciprocity | 48x Unity output (1,000-1,000,000) | *Ends the rift.* |
| **4c**Prophecy Rejected | Large astral threads (140 / 150 / 160) | *Ends the rift.* |

### **The Vortex**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Notes:** The Ever Spinning Top relic is the guaranteed ending as long as you do not blow up the sample in chapter 2. The wiki does not name every node — some titles below are descriptive.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**The Vortex | Small astral threads (40 / 50 / 60) | "Proceed further." (diff 2) → 2a"Expose sample to flame." (diff 6) → 2b / on failure → 2c |
| **2a**Proceeding | Small astral threads (40 / 50 / 60) | "(continue)" → 3 |
| **2b**Flame Test (success) | Engineering researchVortex Fuel: +10% Energy for 10 years | "(continue)" → 3 |
| **2c**Flame Test (failure) | Exotic GasesLarge astral threads (140 / 150 / 160)*Scientist dies* | *Ends the rift.* |
| **3**Descent | Physics researchSmall astral threads (40 / 50 / 60) | "(continue)" → 4 |
| **4**Contact | Small astral threads (40 / 50 / 60) | "Flash lights." (diff 6) → 5a"Observe." (diff 2) → 5b |
| **5a**Flashing Lights | Medium astral threads (90 / 100 / 110) | "(continue)" → 6 |
| **5b**Observation | Physics research | "(continue)" → 6 |
| **6**The Top | —**Ever Spinning Top** | *Ends the rift.* |

### **Tiny Planet**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** Homicidal and Barbaric Despoiler empires get replacement options; 'Destroy the moon' is closed to Pacifist Xenophiles

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**It's a Small World | 12x Physics research output (250-100,000) | "(continue)" → 2 |
| **2**Lunar Impact | Small astral threads (40 / 50 / 60) | "(continue)" → 3 |
| **3**A Small Problem | 18x Society research output (350-100,000) | "Establish contact." (diff 6) → 4 *\\[not Homicidal; not Barbaric Despoilers\\]*"Demand ransom." (diff 6) → 4 *\\[Barbaric Despoilers\\]*"Inform them that their doom has come." (diff 6) → 4 *\\[Homicidal\\]*"Observe passively." (diff 3) → observed *\\[not Homicidal; not Barbaric Despoilers\\]*"Watch the destruction unfold." (diff 3) → observed *\\[Homicidal or Barbaric Despoilers\\]* |
| **4**Communications Established | Small astral threads (40 / 50 / 60) | "Attempt to fix the moon's orbit." (diff 6) → 5a *\\[not Homicidal; not Barbaric Despoilers\\]*"Destroy the moon." (diff 3) → 5b *\\[not Pacifist Xenophile\\]*"Cut communications. Observe passively." (diff 1) → observed *\\[not Homicidal; not Barbaric Despoilers\\]*"Cut communications. Watch the destruction unfold." (diff 1) → observed *\\[Homicidal or Barbaric Despoilers\\]* |
| **5a**Back in Orbit | 24x Physics research output (500-1,000,000) | "(continue)" → tidal |
| **5b**No More Moon | 12x Physics research output (250-100,000)5 Minerals24x Unity output — Homicidal or Barbaric DespoilersMini Moon Dust specimen \\[Grand Archive DLC\\] | "Put them out of their misery." (diff 1) → shallow"Deploy remote research devices." (diff 3) → model |
| **observed**Observed From Afar | Large astral threads (140 / 150 / 160)12x Society research output (250-100,000)24x Unity output — Homicidal or Barbaric Despoilers**+10 Society on the rift** | *Ends the rift.* |
| **tidal**Tidal Locking Breakthrough | Large astral threads (140 / 150 / 160)12x Unity output (250-100,000)**Intentional Tidal Locking planetary decision** | *Ends the rift.* |
| **shallow**Shallow Impact | Large astral threads (140 / 150 / 160)**Display Microplanet Husk decision** | *Ends the rift.* |
| **model**Model Planet | Large astral threads (140 / 150 / 160)12x Society research output (250-100,000)**+15 Society on the rift for 10 years** | *Ends the rift.* |

### **Tropical Habitat**

**Requirements:** Astral Planes DLC; Rift Sphere technology

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Tropical Habitat | Small astral threads (40 / 50 / 60) | "(continue)" → 2 |
| **2**Rough Landing | Small astral threads (40 / 50 / 60) | "Examine the fauna." (diff 2) → 3a"Sample the pink gas." (diff 2) → 3b |
| **3a**Fauna Study | Exotic Gases if Robotic/Lithoid/Toxoid, otherwise Society research | "Find the source of this gas." (diff 2) → 4 |
| **3b**Atmospheric Analysis | Exotic GasesSmall astral threads (40 / 50 / 60) | "Don respiratory gear and proceed." (diff 5) → 4 |
| **4**Yawning Chasm | Exotic GasesSmall astral threads (40 / 50 / 60) | "Use caution. Excavate around the chasm." (diff 5) → 5a"Explore the chasm directly." (diff 2) → 5b |
| **5a**Excavating the Chasm | 5000 Minerals1000 Exotic Gases | "Study the soil samples." (diff 2) → 6a |
| **5b**Exploring the Chasm | Small astral threads (40 / 50 / 60) | "Extract the mouth." (diff 6) → 6b / on failure → 6c"Harvest soil from the deepest walls." (diff 3) → 6d |
| **6a**Geological Marvel | Large astral threads (140 / 150 / 160)Random Biology (Farming) technology | *Ends the rift.* |
| **6b**Extraction (success) | Small astral threads (40 / 50 / 60) | "Analyze the severed organ." → 7 |
| **6c**Traumatic Extraction (failure) | Small astral threads (40 / 50 / 60)*Scientist gains the Maimed trait unless robotic* | "Analyze the severed organ." → 7 |
| **6d**Deep Soil Harvest | Large astral threads (140 / 150 / 160)Random Biology (Farming) technologySociety research | *Ends the rift.* |
| **7**Planetary Dissection | Large astral threads (140 / 150 / 160)**Formula Pink: +20 opinion from non-robotic/lithoid/toxoid empires, +10% army health, -50% morale damage** | *Ends the rift.* |

### **Volcanic Plane**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Notes:** Destroying the obelisk triggers a follow-up event \~6 years later demanding one pop per year for six years.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Fiery Landscape | Small astral threads (40 / 50 / 60) | "Explore the surroundings." (diff 2) → 2a"Fly toward the obelisk." (diff 5) → 2b |
| **2a**Pursued | Small astral threads (40 / 50 / 60) | "Hide in the lava." (diff 6) → 3"Pull the emergency anchor." (diff 1) → 5a |
| **2b**Captured | — | "Attempt to escape." (diff 6) → 3 *cost: -100 Astral Threads*"Pull the emergency anchor." (diff 1) → 5a |
| **3**The Black Obelisk | Medium astral threads (90 / 100 / 110) | "Decipher the runes." (diff 2) → 4"Destroy the obelisk." (diff 6) → 5b / on failure → 5c *cost: -100 Exotic Gases* *(1.5% failure chance)* |
| **4**Names | Small astral threads (40 / 50 / 60) | "Destroy this infernal device." (diff 6) → 5b / on failure → 5c *(1.5% failure chance)*"Pull the emergency anchor." (diff 1) → 5a |
| **5a**Retrieval | Medium astral threads (90 / 100 / 110) | *Ends the rift.* |
| **5b**Shattered Obelisk | 12x Minerals output (150-2,000)12x Alloys output (150-2,000)12x Unity output (150-2,000)Large astral threads (140 / 150 / 160)Obsidian Obelisk Fragment specimen \\[Grand Archive DLC\\]*Follow-up: about 6 years later the obelisk demands 1 pop per year for 6 years. Accept → Restoring the Balance (+10% Energy for 6 years). Refuse → Obelisk's Curse (-6% happiness for 6 years; +6 deviancy for gestalts).* | *Ends the rift.* |
| **5c**Failure | Large astral threads (140 / 150 / 160)*Scientist is lost**Follow-up: after 1 year the scientist returns with Paranoia + Traumatized; a year later they gain Obelisk's Curse (+10% Energy, but sacrifices 1 pop per year while on the council).* | *Ends the rift.* |

### **Whiteout**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Notes:** Linear rift — every path reaches the same ending; choices only change the intermediate research payouts.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Whiteout | Small astral threads (40 / 50 / 60) | "Maximize propulsion." (diff 2) → 2a"Release a drone." (diff 5) → 2b |
| **2a**Maximized Propulsion | Small astral threads (40 / 50 / 60) | "(continue)" → 3 |
| **2b**Drone Released | Physics research | "(continue)" → 3 |
| **3**The Sphere | Medium astral threads (90 / 100 / 110) | "Take a sample." (diff 6) → 4a"Trace a map." (diff 3) → 4b |
| **4a**Sample Taken | Rare Crystals | "(continue)" → 5 |
| **4b**Map Traced | Society research | "(continue)" → 5 |
| **5**The Writer | Large astral threads (140 / 150 / 160)The Writer's Sphere specimen \\[Grand Archive DLC\\]**+10% Physics research for 10 years** | *Ends the rift.* |

### **Windswept Planet**

**Requirements:** Astral Planes DLC; Rift Sphere technology

**Restrictions:** 'Negotiate a compromise' is closed to genocidal empires; 'Eradicate both species' is genocidal-only

**Notes:** Two mirrored paths converge on the same four endings. The compromise ending is the richest and can also convert your scientist into an envoy.

|  |  |  |
| :-: | :-: | :-: |
| Chapter | Rewards on entering | Choices (difficulty → next chapter) |
| **1**Windswept Planet | 6x Exotic Gases output (100-1,000) | "Rise above the storm." (diff 2) → 2a"Shelter in the cave below." (diff 2) → 2b |
| **2a**Beyond the Stratosphere | Small astral threads (40 / 50 / 60) | "(continue)" → 3a |
| **3a**Living Wind | Small astral threads (40 / 50 / 60) | "(continue)" → 4a |
| **4a**Fungal Threat | Small astral threads (40 / 50 / 60) | "Find a way to remove the fungus." (diff 6) → cutting\\_winds *cost: -25 Alloys*"Investigate the fungus." (diff 3) → 5a |
| **5a**Fungal Transmission | Small astral threads (40 / 50 / 60) | "(continue)" → 6 |
| **2b**Fungal Cavern | Small astral threads (40 / 50 / 60) | "(continue)" → 3b |
| **3b**Among the Fungus | Small astral threads (40 / 50 / 60) | "(continue)" → 4b |
| **4b**Carnivorous Winds | Small astral threads (40 / 50 / 60) | "Protect the ecosystem against the wind." (diff 6) → fungal\\_bloom *cost: -50 Minerals*"Study the wind." (diff 3) → 5b |
| **5b**Current Events | Small astral threads (40 / 50 / 60) | "(continue)" → 6 |
| **6**The Case for the Fungus / The Case for the Wind | Small astral threads (40 / 50 / 60) | "Fortify the wind." (diff 3) → cutting\\_winds *cost: -25 Alloys*"Nourish the fungus." (diff 3) → fungal\\_bloom *cost: -50 Minerals*"Negotiate a compromise." (diff 6) → compromise *\\[not genocidal\\]*"Eradicate both species." (diff 6) → eradication *\\[genocidal\\]* |
| **cutting\\_winds**Cutting Winds | —**Incubate Wind Creatures (usable 3 times, +5 max generator districts each)** | *Ends the rift.* |
| **fungal\\_bloom**Fungal Bloom | Extradimensional Fungus specimen \\[Grand Archive DLC\\]**Extra Dimensional Spores: +25% Exotic Gases** | *Ends the rift.* |
| **compromise**A Difficult Compromise | 18x Exotic Gases output (250-5,000)18x Energy output (250-5,000)18x Unity output (250-1,000,000) — GestaltLarge astral threads (140 / 150 / 160)**+10 Society on the rift****Reconverted Leader (+1 envoy) if you convert the scientist to an envoy in the follow-up event** | *Ends the rift.* |
| **eradication**Biological Eradication | 48x Food output (700-30,000)18x Unity output (250-1,000,000) | *Ends the rift.* |

## **7. Assumptions to pressure-test before you build on this**

  - Chapter numbering on the wiki is inconsistent across rifts (some use 1 / 2-A, some use combined ids like 3/4-A because the chapter count shifts with your route). Node ids here follow the wiki, not the game files.
  - A handful of nodes have no wiki-documented title (The Vortex, Whiteout, parts of Tropical Habitat). Those titles are descriptive placeholders.
  - Failure branches are only listed where the wiki documents one. Most chapters have no failure effect at all.
  - Reward values are multipliers of your current empire output, so "best reward" changes with game stage. Do not treat the ranges as flat numbers.
  - Everything here is wiki-sourced, not extracted from the game files. Before shipping a tool on it, spot-check the highest-traffic rifts (The Mechanism, Desert Ruins, The Garden, The Crystal Rift) against the current patch.
  - Astral Planes DLC is assumed throughout. Grand Archive specimen rewards are flagged per reward.
