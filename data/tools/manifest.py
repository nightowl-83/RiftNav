# -*- coding: utf-8 -*-
"""Build resources/image_manifest.json — a map from dataset rewards/entities to
the wiki image filenames that illustrate them. Filenames only; no image data."""
import os, json, re, unicodedata
HOME=os.environ["HOME"]; ROOT=HOME+"/mnt/Stellaris"
disc=json.load(open(f"{ROOT}/data/stellaris_discovery.v2.1.json"))
BASE="https://stellaris.paradoxwikis.com"

def wikify(fn):
    fn=fn.strip().replace(" ","_")
    return fn[0].upper()+fn[1:] if fn else fn

# --- site event art, as referenced on the Archaeological_site wiki page
SITE_ART = {
 "Ancient Capital Site":"Evt_overgrown_city.png","Ancient Facility":"Evt outpost.png",
 "Anomalous Cube":"Evt errant cube.png","Message in a Bottle":"Evt_frozen.png",
 "Message in the Canopy":"Evt_tropical_planet.png","Plentiful Fossils":"Evt_alien_wildlife.png",
 "Under the Ice":"Evt_frozen.png","Abandoned Observation Outpost":"Evt medieval_alien_civilization.png",
 "Ancient Robot World":"evt_ai_planet.png","Debris Belt":"evt_space_debris.png",
 "Desiccated":"evt_warm_barren.png","Moon Base":"Evt_barren_dig_site.png",
 "Abandoned Ecumenopolis":"Evt_overgrown_city.png","Never Forget":"evt_city_ruins.png",
 "One Last Hope":"evt_ocean.png","Ruined Star System":"evt_tomb_world.png",
 "Ruined World":"Evt_relic_world.png","The Crashed Ship":"evt_landing_ship_2.png",
 "The Signal":"evt_landing_ship.png","Tiyanki Grave Mound":"evt_gray_goo.png",
 "Vagrosian Ruins":"Evt city_ruins.png","From Gateway Sent":"evt_atmospheric_entry.png",
 "Homeworld Excavation":"evt_archaeological_dig.png","The Ruined Cradle":"Evt tomb_world.png",
 "Factory Setting":"Evt tomb_world.png","Copper and Chrome":"Evt tomb_world.png",
 "Dust Upon Dust":"Evt tomb_world.png","Point of Origin":"Evt tomb_world.png",
 "The Aftermath of Battle":"Evt_payback.png","Crashed Slaver Ship":"Evt_broken_shackles.png",
 "Quantum Catapult":"evt_slingshot_stars.png","Ancient Crater":"Evt riftworld archsite crater.png",
 "Derelict Safehouse":"Evt cold_barren.png","The Shrouded World":"Evt shrouded planet.png",
 "Grunur Ruins":"Evt baol 1.png","The Barren":"Evt warm barren planet.png",
 "The Shattered":"Evt asteroid field.png","The Silenced":"Evt baol 5.png",
 "Abandoned Colony Ruins":"Evt overgrown_city.png","Zroni Beacon":"Evt overgrown_city.png",
 "Zroni Shrine":"Evt overgrown_city.png","Zroni Research Station":"Evt baol 2.png",
 "Zroni Core World":"Evt baol 2.png","Zron":"Evt shrouded planet.png",
 "The Propaganda Station":"Evt_ruined_system.png",
 "Windswept Fates":"evt_cosmic_storms_windswept_fates.png",
 "Fleets of the Thrice Damned":"evt_cosmic_storms_fleets_of_the_thrice_damned.png",
 "Institute of Exalted Benevolence":"evt_habitat.png","Celebration":"evt_ancient_databank.png",
 "The Ancient Shelters":"evt_weather_manipulators.png",
 "Coordinates A: Colonized Planet":"evt_weather_manipulators.png",
 "Coordinates B: Industrial Planet":"evt_weather_manipulators.png",
 "Coordinates C: Barren Planet":"evt_weather_manipulators.png",
 "Origins of the Pervading":"evt_weather_manipulators.png","Before the Fall":"evt_weather_manipulators.png",
 "Ancient Battle Site":"Evt_landing_ship.png","Ancient Tomb":"Evt_excavation_team.png",
 "Any Other Rock":"Evt_warm_barren.png","Anyone Home?":"Evt_overgrown_city.png",
 "Asteroid Blast Door":"Evt_barren_dig_site.png","Beautiful Bubble":"Evt_big_landing_ship.png",
 "Beneath the Waves":"Evt_ship_in_orbit_2.png","City of Bones":"Evt_relic_world_street.png",
 "Crashed Starship":"Evt_crashed_station.png","Déjà Vu Dig":"Evt_archaeology_camp.png",
 "Dotted Archipelago":"Evt_ocean.png","Fossilized Remains":"Evt_archaeology_camp.png",
 "Frozen Complex":"Evt_frozen.png","Gas Giant Structure":"Evt_gas_giant_station.png",
 "Get Inside":"Evt_alien_ruins.png","Get to the Bottom":"Evt_ship_in_orbit.png",
 "Ix Belèn":"Evt_gas_giant_station.png","Hidden Worlds":"Evt_crashed_station.png",
 "Hole in the Ground":"Evt_big_landing_ship.png","Kleptomaniac Rats":"Evt_relic_world.png",
 "Message in the Dust":"Evt_ship_in_orbit.png","Moon Bump":"Evt_relic_world_street.png",
 "Mutant Fossils":"Evt_scanning_remains.png","Planetary Machinery":"evt_tomb_world.png",
 "Popular Rock":"Evt_ice_asteroids.png","Relic Rails":"Evt_archaeological_dig.png",
 "Robot Debris":"Evt_space_debris.png","Ruined Station":"Evt_space_debris.png",
 "Ruins":"Evt_dead_city.png","Seeds of Destruction":"Evt_frozen.png",
 "Strange Asteroid":"Evt_asteroid_field.png","Strange Flows":"Evt_glitchy_matrix.png",
 "Subterranean Hollows":"Evt_underground_civilization.png","Target from Orbit":"Evt_ship_in_orbit.png",
 "The Echoes Inside":"Evt_arid_planet.png","The Endless Expanse":"Evt_frozen.png",
 "The Grand Herald":"Evt_ancient_alien_temple.png","The Library":"Evt_archaeological_dig.png",
 "Too Angled":"Evt_ship_in_orbit.png","Trench World":"Evt_tundra_planet.png",
 "Weapons Cache":"Evt_tomb_world.png","Whispers in the Stone":"Evt_hidden_door.png",
 "The Sentinels":"Evt_huge_monument.png","The Broken Gates":"Evt baol 5.png",
 "Chthonic Siren":"evt_clocks.png","Green Skies":"evt_alien_planet.png",
 "Hold the Line":"evt_habitat.png","Repowered Complex":"evt_generator_powerup.png",
}
RIFT_ART = {
 "Ruined Planet":"Evt astral rift riftworld.png","Genesis":"Evt astral rift genesis 2.png",
 "Strange Station":"Evt space station.png","The Microverse":"Evt astral rift microverse.png",
 "Entertainment Nexus":"Evt astral rift interdimensional circus.png",
 "The Crystal Rift":"Evt astral rift crystal 1.png",
 "Psionic Stranger":"Evt astral rift psionic stranger.png",
 "Siege on Paradise":"Evt astral rift siege on paradise baol.png",
}
RELIC_ICON = {  # only relics that appear in the datasets
 "Celestial Tear":"R celestial tear.png","Daedalus Seal":"R daedalus seal.png",
 "Ever Spinning Top":"R ever spinning top.png","Infinity Root":"R infinity root.png",
 "Plasmic Core":"R plasmic core.png","The Continuum":"R continuum.png",
 "Time Crystal":"R time crystal.png","Crystal of Odryskia":"R odryskan crystal.png",
 "Blade of the Huntress":"R ancient sword.png","Head of Zarqlan":"R severed head.png",
 "Miniature Galaxy":"R galaxy.png","The Defragmentor":"R mechano calibrator.png",
 "Omnicodex":"R omnicodex.png","The Rubricator":"R rubricator.png",
 "Psionic Archive":"R zro crystal.png","The Disturbance Oppressor":"R weather manipulator.png",
 "The Tempest Invocator":"R the tempest invocator.png","Eternal Throne":"R eternal throne.png",
}
UNRESOLVED_RELICS = ["Advisor Core"]
SHARED = {"Astral threads":"Astral threads.png","Grand Archive":"Grand Archive.png",
          "Minor artifacts":"Minor artifacts.png"}
TRAIT_ICON = {"Rift Warped":"Leader trait rift warped.png","Maimed":"Leader trait maimed.png",
              "Resilient":"Leader trait resilient.png","Psionic":"Leader trait psionic leader.png"}

by_name={e["name"]:e for e in disc["entities"]}
items=[]
def add(cat, subject, fname, uids, status="resolved", note=None):
    wf=wikify(fname) if fname else None
    items.append({"category":cat,"subject":subject,"wiki_file":wf,
                  "file_page":f"{BASE}/File:{wf}" if wf else None,
                  "local_name":(re.sub(r"[^a-z0-9]+","-",unicodedata.normalize("NFKD",subject)
                                .encode("ascii","ignore").decode().lower()).strip("-")
                                + os.path.splitext(wf)[1]) if wf else None,
                  "entity_uids":uids,"status":status,"note":note})

for name,fn in RIFT_ART.items():
    e=by_name.get(name); add("entity_art",name,fn,[e["uid"]] if e else [],
        "resolved" if e else "orphan", None if e else "name not in dataset")
for name,fn in SITE_ART.items():
    e=by_name.get(name); add("entity_art",name,fn,[e["uid"]] if e else [],
        "resolved" if e else "orphan", None if e else "name not in dataset")
for name,fn in RELIC_ICON.items():
    uids=[r["entity_id"] for r in disc["reward_finder"]
          if r["category"] in ("Relics","Situations","Situations & event chains")
          and name.lower() in r["reward"].lower() and r["entity_id"]]
    add("relic",name,fn,sorted(set(uids)))
for name in UNRESOLVED_RELICS:
    uids=[r["entity_id"] for r in disc["reward_finder"] if name.lower() in r["reward"].lower() and r["entity_id"]]
    add("relic",name,None,sorted(set(uids)),"unresolved",
        "Not found in the wiki's Relics table under this name. Verify before assuming an icon exists.")
for name,fn in TRAIT_ICON.items(): add("leader_trait",name,fn,[])
for name,fn in SHARED.items():
    add("resource_icon",name,fn,[],"needs_verification","Filename inferred from wiki usage; confirm the File: page exists before download.")

spec=sorted({r["reward"] for r in disc["reward_finder"] if r["category"]=="Specimens (Grand Archive)"})
add("specimen","(63 specimen icons)",None,[],"unresolved",
    f"{len(spec)} specimen reward rows reference Grand Archive specimens, but the rift and site pages link them as anchors on the Collection page rather than as File: refs. Their icons need a separate pass over Collection.")

resolved=[i for i in items if i["status"]=="resolved"]
manifest={"dataset":"stellaris_image_manifest","version":"1.0","generated":"2026-08-30",
 "schema_note":"Filenames and wiki page URLs only. No image data is included or redistributed here.",
 "source":f"{BASE}/Archaeological_site , {BASE}/Astral_rift , {BASE}/Relics",
 "licensing":"These files are Paradox Interactive game assets hosted on the community wiki for documentation. "
             "The wiki's TEXT is openly licensed; the extracted art is not. Fine for a local prototype; "
             "get a deliberate answer before putting them behind a public URL.",
 "counts":{"total":len(items),"resolved":len(resolved),
           "needs_verification":sum(1 for i in items if i["status"]=="needs_verification"),
           "unresolved":sum(1 for i in items if i["status"]=="unresolved"),
           "unique_files":len({i["wiki_file"] for i in resolved}),
           "entities_with_art":len({u for i in items if i["category"]=="entity_art" for u in i["entity_uids"]}),
           "entities_total":len(disc["entities"])},
 "items":items}
json.dump(manifest,open(f"{ROOT}/resources/image_manifest.json","w"),indent=1,ensure_ascii=False)
c=manifest["counts"]
print(f"manifest rows {c['total']} | resolved {c['resolved']} | verify {c['needs_verification']} | unresolved {c['unresolved']}")
print(f"unique files to download: {c['unique_files']}")
print(f"entity art coverage: {c['entities_with_art']}/{c['entities_total']} entities")
missing=[e["name"] for e in disc["entities"] if not any(u==e["uid"] for i in items if i["category"]=="entity_art" for u in i["entity_uids"])]
print(f"entities with NO art mapped ({len(missing)}): {', '.join(missing[:8])}{' …' if len(missing)>8 else ''}")
