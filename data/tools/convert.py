# -*- coding: utf-8 -*-
"""Normalise the Stellaris rift + archaeology datasets onto one schema (v2.1).

Reads the existing files only. Never hand-edits data: every string in the output
is copied verbatim from the source files, so v2.1 cannot drift from v2.0 / v1.0.
"""
import os, json, re, unicodedata

HOME = os.environ["HOME"]
DATA = HOME + "/mnt/Stellaris/data"
SCHEMA_ID = "stellaris-discovery/2.1"
VERSION = "2.1"
GENERATED = "2026-08-30"

def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t

RIFT_GROUPS = [("unique", "Unique rifts"), ("precursor", "Precursor rifts"), ("general", "General rifts")]

# Shared mechanics text for rifts, lifted from the rift document's own section 1
RIFT_MECHANICS = [
 "The rift must be inside your borders. You need the Rift Sphere rare technology plus a scientist and a science ship. Councillors cannot explore rifts and exploration cannot be stopped once started.",
 "Phases are 90 days. Roll = d10 + scientist Astral Rift Skill + clues - chapter difficulty.",
 "14+ completes the chapter (75 XP). 10-13 gives 2 clues (40 XP). 5-9 gives 1 clue (25 XP). 4 or less gives nothing (10 XP) and carries a 1.5% chance to fail the chapter (0.75% with the Riftworld origin).",
 "Spawning after the mid-game year: chance/100 = 2 x years_since_last_spawn x weight + eligible_systems/3. Weight is 1 base, x2 for the Riftworld origin, x2 for the Dimensional Worship civic, x10 if you began 'A Rift in Space' but lost your last rift. -25 flat once you have completed 5 rifts. There is a 10-year moratorium after each spawn.",
]

RIFT_ASSUMPTIONS = [
 "Chapter numbering on the wiki is inconsistent across rifts. Some use 1 / 2-A, some use combined ids like 3/4-A because the chapter count shifts with your route. Chapter ids here follow the wiki, not the game files.",
 "A handful of chapters have no wiki-documented title (The Vortex, Whiteout, parts of Tropical Habitat). Those titles are descriptive placeholders.",
 "Failure branches are only listed where the wiki documents one. Most chapters have no failure effect at all.",
 "Reward values are multipliers of your current empire output, so 'best reward' changes with game stage. Do not treat the clamps as flat numbers.",
 "Everything is wiki-sourced, not extracted from the game files. Spot-check the high-traffic rifts against your current patch: The Mechanism, Desert Ruins, The Garden, The Crystal Rift.",
 "The rift document's chapter column is headed 'Rewards on entering' while the wiki reads as on chapter completion. Resolve this before building anything that depends on payout timing.",
 "Astral Planes DLC is assumed throughout. Grand Archive specimen rewards are flagged per reward.",
]

def norm_codes(codes):
    if isinstance(codes, dict):
        return [{"code": k, "meaning": v} for k, v in codes.items()]
    return [{"code": c["code"], "meaning": c["meaning"]} for c in codes]

def build_rifts():
    src = json.load(open(f"{DATA}/astral_rifts.json"))
    labels = dict(RIFT_GROUPS)
    entities, seen = [], set()
    for r in src["rifts"]:
        sid = slug(r["name"])
        assert sid not in seen, f"duplicate rift slug {sid}"
        seen.add(sid)
        entities.append({
            "id": sid, "uid": f"rift:{sid}", "kind": "astral_rift", "name": r["name"],
            "group": r["class"], "group_label": labels[r["class"]],
            "dlc": "Astral Planes", "precursor": None, "system": None,
            "requirements": r.get("requirements"), "restrictions": r.get("restrictions"),
            "notes": r.get("notes"),
            "chapters": [{
                "id": c["id"], "index": i + 1, "title": c.get("title"),
                "rewards": c.get("rewards", []), "choices": c.get("choices", []),
            } for i, c in enumerate(r["chapters"])],
        })
    by_name = {e["name"]: e for e in entities}
    finder = []
    for cat, rows in src["reward_finder"].items():
        for row in rows:
            ent = by_name.get(row["rift"])
            finder.append({
                "category": cat, "reward": row["reward"],
                "entity": row["rift"], "entity_id": ent["uid"] if ent else None,
                "kind": "astral_rift",
                "group_label": ent["group_label"] if ent else None,
                "chapter": None, "path": row.get("path") or None,
            })
    return {
        "dataset": "stellaris_astral_rifts", "kind": "astral_rift", "schema": SCHEMA_ID,
        "version": VERSION, "generated": GENERATED, "source": src["source"],
        "notes": src.get("notes"),
        "coverage": {"entities": len(entities),
                     "chapters": sum(len(e["chapters"]) for e in entities),
                     "finder_rows": len(finder)},
        "mechanics": RIFT_MECHANICS,
        "reward_codes": norm_codes(src["reward_codes"]),
        "groups": [{"key": k, "label": l} for k, l in RIFT_GROUPS],
        "entities": entities, "reward_finder": finder,
        "assumptions": RIFT_ASSUMPTIONS,
    }

def build_sites():
    src = json.load(open(f"{DATA}/archaeological_sites.json"))
    labels = {g["key"]: g["label"] for g in src["groups"]}
    entities, seen = [], set()
    for s in src["sites"]:
        sid = slug(s["name"])
        assert sid not in seen, f"duplicate site slug {sid}"
        seen.add(sid)
        req = s.get("requirements") or ""
        m = re.match(r"^([A-Z][A-Za-z' ]+) system\b", req)
        entities.append({
            "id": sid, "uid": f"site:{sid}", "kind": "archaeological_site", "name": s["name"],
            "group": s["group"], "group_label": labels[s["group"]],
            "dlc": s.get("dlc"), "precursor": s.get("precursor"),
            "system": m.group(1) if m else None,
            "requirements": s.get("requirements"), "restrictions": None,
            "notes": s.get("notes"),
            "chapters": [{
                "id": str(c["n"]), "index": i + 1, "title": None,
                "rewards": c.get("rewards", []), "choices": [],
            } for i, c in enumerate(s["chapters"])],
        })
    by_name = {e["name"]: e for e in entities}
    finder = []
    for cat, rows in src["reward_finder"].items():
        for row in rows:
            ent = by_name.get(row["site"])
            finder.append({
                "category": cat, "reward": row["reward"],
                "entity": row["site"], "entity_id": ent["uid"] if ent else None,
                "kind": "archaeological_site",
                "group_label": row.get("group") or (ent["group_label"] if ent else None),
                "chapter": str(row["chapter"]) if row.get("chapter") is not None else None,
                "path": None,
            })
    return {
        "dataset": "stellaris_archaeological_sites", "kind": "archaeological_site",
        "schema": SCHEMA_ID, "version": VERSION, "generated": GENERATED,
        "source": src["source"], "notes": None,
        "coverage": {"entities": len(entities),
                     "chapters": sum(len(e["chapters"]) for e in entities),
                     "finder_rows": len(finder)},
        "mechanics": src["mechanics"],
        "reward_codes": norm_codes(src["reward_codes"]),
        "groups": src["groups"],
        "entities": entities, "reward_finder": finder,
        "assumptions": src["assumptions"],
    }

def build_merged(a, b):
    codes, seen = [], set()
    for c in a["reward_codes"] + b["reward_codes"]:
        if c["code"] in seen: continue
        seen.add(c["code"]); codes.append(c)
    return {
        "dataset": "stellaris_discovery", "kind": "mixed", "schema": SCHEMA_ID,
        "version": VERSION, "generated": GENERATED,
        "source": f"{a['source']} ; {b['source']}",
        "notes": "Astral rifts and archaeological sites in one file. Filter on entity.kind. "
                 "Reward codes are merged; where both datasets define a code the rift definition wins "
                 "(they agree except that art* codes appear only in the archaeology set).",
        "coverage": {"entities": len(a["entities"]) + len(b["entities"]),
                     "chapters": a["coverage"]["chapters"] + b["coverage"]["chapters"],
                     "finder_rows": a["coverage"]["finder_rows"] + b["coverage"]["finder_rows"]},
        "mechanics": [{"kind": "astral_rift", "lines": a["mechanics"]},
                      {"kind": "archaeological_site", "lines": b["mechanics"]}],
        "reward_codes": codes,
        "groups": ([dict(g, kind="astral_rift") for g in a["groups"]] +
                   [dict(g, kind="archaeological_site") for g in b["groups"]]),
        "entities": a["entities"] + b["entities"],
        "reward_finder": a["reward_finder"] + b["reward_finder"],
        "assumptions": ([{"kind": "astral_rift", "text": t} for t in a["assumptions"]] +
                        [{"kind": "archaeological_site", "text": t} for t in b["assumptions"]]),
    }

rifts, sites = build_rifts(), build_sites()
merged = build_merged(rifts, sites)
for name, obj in (("astral_rifts.v2.1.json", rifts),
                  ("archaeological_sites.v2.1.json", sites),
                  ("stellaris_discovery.v2.1.json", merged)):
    json.dump(obj, open(f"{DATA}/{name}", "w"), indent=1, ensure_ascii=False)
    print(f"{name:34} entities={obj['coverage']['entities']:4} "
          f"chapters={obj['coverage']['chapters']:4} finder={obj['coverage']['finder_rows']:4}")
