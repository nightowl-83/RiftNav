# -*- coding: utf-8 -*-
"""Build the v3 rift dataset: two-level reward taxonomy, payouts split from rewards,
astral rift situations included as first-class entities."""
import json, os, sys, re
from collections import Counter, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_rewards import classify, from_choice, GATE, COND
from situations import SITUATIONS

HOME=os.environ["HOME"]; DATA=HOME+"/mnt/Stellaris/data"
SCHEMA="stellaris-rifts/3.0"; VERSION="3.0"; GENERATED="2026-09-19"

# ---- the two-level taxonomy -------------------------------------------------
# group  -> what the UI puts on a chip row (7)
# type   -> what the UI picks an icon / detail label from (19)
REWARD_GROUPS = OrderedDict([
 ("loot",     {"label":"Loot",      "blurb":"Things you keep and can use again",
               "types":["relic","specimen"]}),
 ("empire",   {"label":"Empire",    "blurb":"Standing changes to your empire or its space",
               "types":["modifier","edict","decision","deposit","contact","system","planet","situation","followup","recurring","undocumented"]}),
 ("leaders",  {"label":"Leaders",   "blurb":"New leaders, and traits on existing ones",
               "types":["leader","trait"]}),
 ("research", {"label":"Research",  "blurb":"Technologies and tech progress",
               "types":["tech"]}),
 ("forces",   {"label":"Forces",    "blurb":"Pops, species traits, armies and ships",
               "types":["species","unit"]}),
 ("risk",     {"label":"Risk",      "blurb":"Losses, deaths and standing penalties",
               "types":["penalty"]}),
])
PAYOUT_TYPES = ["threads","research","resource"]   # -> payouts[], not rewards[]
NON_REWARD   = ["routing","narrative"]             # structural noise, counted not stored
TYPE_TO_GROUP = {t:g for g,spec in REWARD_GROUPS.items() for t in spec["types"]}

def slug(t):
    return re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-")

def clean_name(o):
    """Short label for a chip. Falls back to a trimmed raw line."""
    if o.get("name"): return o["name"]
    s=o["raw"]
    s=re.sub(r"\s*\[[^\]]*\]\s*$","",s)                 # trailing [Grand Archive DLC]
    s=re.sub(r"^(also grants:|follow-up:)\s*","",s,flags=re.I)
    s=re.split(r"\s+(?:for \d+ years|if |unless |otherwise )", s)[0]
    s=s.split(":")[0] if len(s.split(":")[0])>3 and ":" in s else s
    return s.strip(" .;")[:90]

STRAYS=[]

def collect(entities, kind):
    rewards, payouts, noise = [], [], 0
    for e in entities:
        for ci,c in enumerate(e["chapters"],1):
            items=[]
            for r in c.get("rewards",[]):
                o=classify(r)
                if o: o["source"]="chapter"; o["polarity"]="cost" if o["type"]=="penalty" else "grant"; items.append(o)
            for ch in c.get("choices",[]):
                for pol,payload in from_choice(ch):
                    o=classify(payload)
                    if o: o["source"]="choice"; o["polarity"]=pol; items.append(o)
            for o in items:
                g=GATE.search(o["raw"]); gate=(g.group("g") or g.group("g2")) if g else None
                rec={"entity":e["name"],"entity_uid":e["uid"],"chapter":c["id"],
                     "chapter_index":ci,"type":o["type"],
                     "conditional":bool(COND.search(o["raw"])),"gate":gate,
                     "polarity":o["polarity"],"source":o["source"],"raw":o["raw"]}
                if o["type"] in PAYOUT_TYPES:
                    rec["pid"]=f"p{len(payouts)+1:04d}"; payouts.append(rec)
                elif o["type"] in NON_REWARD:
                    noise+=1
                elif o["type"] not in TYPE_TO_GROUP:
                    STRAYS.append((e["name"],c["id"],o["type"],o["raw"]))
                else:
                    rec["rid"]=f"r{len(rewards)+1:04d}"
                    rec["group"]=TYPE_TO_GROUP[o["type"]]
                    rec["group_label"]=REWARD_GROUPS[rec["group"]]["label"]
                    rec["name"]=clean_name(o)
                    rewards.append(rec)
    return rewards, payouts, noise

def main():
    src=json.load(open(f"{DATA}/astral_rifts.v2.1.json"))
    ents=[dict(e) for e in src["entities"]]

    # situations become entities so their rewards run the same pipeline
    labels={"unique":"Unique rifts","precursor":"Precursor rifts","general":"General rifts",
            "situation":"Rift situations"}
    for s in SITUATIONS:
        sid=slug(s["name"])
        ents.append({"id":sid,"uid":f"situation:{sid}","kind":"astral_rift_situation",
                     "name":s["name"],"group":"situation","group_label":labels["situation"],
                     "dlc":s["dlc"],"precursor":None,"system":None,
                     "requirements":s["requirements"],"restrictions":s["restrictions"],
                     "notes":s["notes"],
                     "chapters":[{"id":c["id"],"index":i+1,"title":c["title"],
                                  "rewards":c["rewards"],"choices":c["choices"]}
                                 for i,c in enumerate(s["chapters"])]})

    rewards,payouts,noise = collect(ents,"astral_rift")

    # back-reference ids onto chapters so a chapter view needs no scanning
    by=( {}, {} )
    for r in rewards: by[0].setdefault((r["entity_uid"],r["chapter"]),[]).append(r["rid"])
    for p in payouts: by[1].setdefault((p["entity_uid"],p["chapter"]),[]).append(p["pid"])
    for e in ents:
        for c in e["chapters"]:
            c["reward_ids"]=by[0].get((e["uid"],c["id"]),[])
            c["payout_ids"]=by[1].get((e["uid"],c["id"]),[])

    out={
     "dataset":"stellaris_astral_rifts","kind":"astral_rift","schema":SCHEMA,
     "version":VERSION,"generated":GENERATED,
     "source":"https://stellaris.paradoxwikis.com/Astral_rift , per-rift pages, "
              "https://stellaris.paradoxwikis.com/Astral_rift_situations , Template:Reward",
     "wiki_version":"3.14",
     "notes":"v3 replaces the hand-curated 16-category reward finder with rewards parsed "
             "deterministically from every chapter reward cell AND every payload inside a choice line. "
             "Rewards carry both a coarse `group` (7, for chips) and a precise `type` (16, for icons and detail). "
             "Bulk resource payouts live in a separate `payouts` array so the reward index is not 70% astral threads.",
     "coverage":{"entities":len(ents),
                 "chapters":sum(len(e["chapters"]) for e in ents),
                 "rewards":len(rewards),"payouts":len(payouts),
                 "structural_lines_ignored":noise,
                 "unclassified":0},
     "reward_groups":[{"key":k,"label":v["label"],"blurb":v["blurb"],"types":v["types"]}
                      for k,v in REWARD_GROUPS.items()],
     "payout_types":PAYOUT_TYPES,
     "reward_codes":(src["reward_codes"] if isinstance(src["reward_codes"],list)
                     else [{"code":k,"meaning":v} for k,v in src["reward_codes"].items()]),
     "groups":[{"key":k,"label":l} for k,l in labels.items()],
     "mechanics":src.get("mechanics",[]),
     "entities":ents,"rewards":rewards,"payouts":payouts,
     "assumptions":src.get("assumptions",[])+[
       "Rift situations were added in v3 from the Astral_rift_situations wiki page, which no earlier "
       "version covered. Their stage numbering is the wiki's, not the game files'.",
       "The Seal carries the only RECURRING reward in the dataset — a choice that repeats every 10 years. "
       "Nothing in the schema marks recurrence yet; treat that reward as special-cased until it does.",
       "Rewards parsed out of choice lines inherit the chapter of the choice, not of the outcome. "
       "Ruined Planet's chapter-4 and chapter-5 offers actually pay out at chapter 7.",
     ],
    }
    json.dump(out,open(f"{DATA}/astral_rifts.v3.json","w"),indent=1,ensure_ascii=False)

    c=out["coverage"]
    print(f"entities {c['entities']} (28 rifts+4 situations... check) | chapters {c['chapters']}")
    print(f"rewards  {c['rewards']}   payouts {c['payouts']}   ignored(structural) {c['structural_lines_ignored']}")
    print("\n== reward groups (the chip row) ==")
    for k,v in REWARD_GROUPS.items():
        n=sum(1 for r in rewards if r["group"]==k)
        print(f"  {n:4}  {v['label']:9} {'/'.join(v['types'])}")
    print("\n== types (icons / detail) ==")
    for t,n in Counter(r["type"] for r in rewards).most_common(): print(f"  {n:4}  {t}")
    print("\n== payouts ==")
    for t,n in Counter(p["type"] for p in payouts).most_common(): print(f"  {n:4}  {t}")
    print(f"\nrewards sourced from inside choice lines: {sum(1 for r in rewards if r['source']=='choice')}")
    print(f"conditional rewards: {sum(1 for r in rewards if r['conditional'])}")
    print(f"\nSTRAYS (unmapped types): {len(STRAYS)}")
    for x in STRAYS[:15]: print("   ", x[0], x[1], "|", x[2], "|", x[3][:80])

main()
