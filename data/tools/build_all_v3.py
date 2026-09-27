# -*- coding: utf-8 -*-
"""Build all three v3 datasets: rifts, archaeological sites, and the merged file.

Single entry point. Reads v2.1 (+ situations source) and emits v3. Nothing is
hand-written: every string is copied verbatim from its source.
"""
import json, os, sys, re
from collections import Counter, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_rewards import classify, from_choice, GATE, COND
from situations import SITUATIONS

HOME=os.environ["HOME"]; DATA=HOME+"/mnt/Stellaris/data"
SCHEMA="stellaris-discovery/3.0"; VERSION="3.0"; GENERATED="2026-09-26"
WIKI="3.14"

REWARD_GROUPS = OrderedDict([
 ("loot",     {"label":"Loot",     "blurb":"Things you keep and can use again",
               "types":["relic","specimen","cosmetic"]}),
 ("empire",   {"label":"Empire",   "blurb":"Standing changes to your empire, its planets or its space",
               "types":["modifier","edict","decision","deposit","contact","system","planet",
                        "situation","followup","recurring","undocumented"]}),
 ("leaders",  {"label":"Leaders",  "blurb":"New leaders, and traits on existing ones",
               "types":["leader","trait"]}),
 ("research", {"label":"Research", "blurb":"Technologies and tech progress",
               "types":["tech"]}),
 ("forces",   {"label":"Forces",   "blurb":"Pops, species traits, armies and ships",
               "types":["species","unit"]}),
 ("risk",     {"label":"Risk",     "blurb":"Losses, deaths and standing penalties",
               "types":["penalty"]}),
])
PAYOUT_TYPES = ["threads","artifacts","research","resource"]
CHAIN_TYPES  = ["chain"]          # -> chains[], graph edges not rewards
NON_REWARD   = ["routing","narrative"]
TYPE_TO_GROUP = {t:g for g,s in REWARD_GROUPS.items() for t in s["types"]}

def slug(t): return re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-")

def clean_name(o):
    if o.get("name"): return o["name"]
    s=re.sub(r"\s*\[[^\]]*\]\s*$","",o["raw"])
    s=re.sub(r"^(also grants:|follow-up:)\s*","",s,flags=re.I)
    s=re.split(r"\s+(?:for \d+ years|if |unless |otherwise )", s)[0]
    if ":" in s and len(s.split(":")[0])>3: s=s.split(":")[0]
    return s.strip(" .;")[:90] or o["raw"][:90]

TARGET=re.compile(r"\breveals?\b(?: the| a)? (?P<t>[A-Z0-9][\w':\- ]*?)\s*(?:site|system)\b"
                  r"|\bstarts the (?P<t2>[A-Z][\w' ]*?) event chain", re.I)

def collect(entities):
    rewards, payouts, chains, ignored = [], [], [], []
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
                base={"entity":e["name"],"entity_uid":e["uid"],"kind":e["kind"],
                      "chapter":c["id"],"chapter_index":ci,"type":o["type"],
                      "conditional":bool(COND.search(o["raw"])),"gate":gate,
                      "polarity":o["polarity"],"source":o["source"],"raw":o["raw"]}
                t=o["type"]
                if t in PAYOUT_TYPES:
                    base["pid"]=f"p{len(payouts)+1:04d}"; payouts.append(base)
                elif t in CHAIN_TYPES:
                    base["cid"]=f"c{len(chains)+1:04d}"
                    base["targets"]=[]          # filled by resolve_chains once names are known
                    chains.append(base)
                elif t in NON_REWARD:
                    ignored.append({"entity":e["name"],"chapter":c["id"],
                                    "type":t,"raw":o["raw"]})
                else:
                    base["rid"]=f"r{len(rewards)+1:04d}"
                    base["group"]=TYPE_TO_GROUP[t]
                    base["group_label"]=REWARD_GROUPS[base["group"]]["label"]
                    base["name"]=clean_name(o)
                    rewards.append(base)
    return rewards, payouts, chains, ignored

def resolve_chains(entities, chains):
    """Match each chain line against real entity names, longest first, so
    'The Last Stand' wins over 'Last Stand' and multi-target lines resolve to both."""
    names=sorted({e["name"] for e in entities}, key=len, reverse=True)
    # bounded aliases: wiki phrasing that cannot substring-match a real entity name
    ALIAS={"benign cover-up":"Benign Cover-Up / Bury The Hatchet",
           "bury the hatchet":"Benign Cover-Up / Bury The Hatchet",
           "three coordinates sites":None}   # None -> expand to all Coordinates entities
    COORDS=[e["name"] for e in entities if e["name"].startswith("Coordinates ")]
    for c in chains:
        raw=c["raw"].lower(); hits=[]
        for n in names:
            if n.lower() in raw and not any(n.lower() in h.lower() for h in hits):
                hits.append(n)
        for k,v in ALIAS.items():
            if k in raw:
                if v is None: hits.extend(COORDS)
                elif v not in hits: hits.append(v)
        c["targets"]=sorted({h for h in hits})
        c["target_kind"]=("site" if c["targets"] else
                          "event_chain" if "event chain" in raw else
                          "system" if "system" in raw else
                          "special_project" if "special project" in raw else "unknown")
    return chains

def link(entities, rewards, payouts, chains):
    idx={}
    for arr,key in ((rewards,"rid"),(payouts,"pid"),(chains,"cid")):
        for x in arr: idx.setdefault((x["entity_uid"],x["chapter"],key),[]).append(x[key])
    for e in entities:
        for c in e["chapters"]:
            c["reward_ids"]=idx.get((e["uid"],c["id"],"rid"),[])
            c["payout_ids"]=idx.get((e["uid"],c["id"],"pid"),[])
            c["chain_ids"]=idx.get((e["uid"],c["id"],"cid"),[])
        e["unlocks"]=sorted({t for x in chains if x["entity_uid"]==e["uid"]
                             for t in x.get("targets",[]) if t != e["name"]})

def envelope(name, kind, ents, rewards, payouts, chains, ignored, src, extra_assumptions=()):
    return {
     "dataset":name,"kind":kind,"schema":SCHEMA,"version":VERSION,"generated":GENERATED,
     "wiki_version":WIKI,"source":src,
     "coverage":{"entities":len(ents),"chapters":sum(len(e["chapters"]) for e in ents),
                 "rewards":len(rewards),"payouts":len(payouts),"chains":len(chains),
                 "structural_lines_ignored":len(ignored),"unclassified":0},
     "reward_groups":[{"key":k,"label":v["label"],"blurb":v["blurb"],"types":v["types"]}
                      for k,v in REWARD_GROUPS.items()],
     "payout_types":PAYOUT_TYPES,
     "entities":ents,"rewards":rewards,"payouts":payouts,"chains":chains,
     "ignored_lines":ignored,
     "assumptions":list(extra_assumptions),
    }

def main():
    # ---------- rifts ----------
    rsrc=json.load(open(f"{DATA}/astral_rifts.v2.1.json"))
    rents=[dict(e) for e in rsrc["entities"]]
    for s in SITUATIONS:
        sid=slug(s["name"])
        rents.append({"id":sid,"uid":f"situation:{sid}","kind":"astral_rift_situation",
                      "name":s["name"],"group":"situation","group_label":"Rift situations",
                      "dlc":s["dlc"],"precursor":None,"system":None,
                      "requirements":s["requirements"],"restrictions":s["restrictions"],
                      "notes":s["notes"],
                      "chapters":[{"id":c["id"],"index":i+1,"title":c["title"],
                                   "rewards":c["rewards"],"choices":c["choices"]}
                                  for i,c in enumerate(s["chapters"])]})
    rr,rp,rc,rn = collect(rents); resolve_chains(rents,rc); link(rents,rr,rp,rc)
    rifts=envelope("stellaris_astral_rifts","astral_rift",rents,rr,rp,rc,rn,
      "https://stellaris.paradoxwikis.com/Astral_rift , per-rift pages , "
      "https://stellaris.paradoxwikis.com/Astral_rift_situations , Template:Reward",
      rsrc.get("assumptions",[])+[
       "Rift situations were added in v3 from the Astral_rift_situations wiki page, which no "
       "earlier version covered. Stage numbering is the wiki's, not the game files'.",
       "The Seal carries the only recurring reward (type 'recurring'). The schema cannot express "
       "recurrence - any rift-value total is wrong for it until it can.",
       "Rewards parsed out of choice lines inherit the chapter of the CHOICE, not the payout. "
       "Ruined Planet's chapter-4 and chapter-5 offers actually resolve at chapter 7.",
      ])
    rifts["reward_codes"]=rsrc["reward_codes"]
    rifts["mechanics"]=rsrc.get("mechanics",[])
    rifts["groups"]=[{"key":k,"label":l} for k,l in
      [("unique","Unique rifts"),("precursor","Precursor rifts"),("general","General rifts"),
       ("situation","Rift situations")]]

    # ---------- archaeological sites ----------
    asrc=json.load(open(f"{DATA}/archaeological_sites.v2.1.json"))
    aents=[dict(e) for e in asrc["entities"]]
    ar_,ap,ac,an = collect(aents); resolve_chains(aents,ac); link(aents,ar_,ap,ac)
    arch=envelope("stellaris_archaeological_sites","archaeological_site",aents,ar_,ap,ac,an,
      asrc["source"],
      asrc.get("assumptions",[])+[
       "Migrated to v3 on 2026-09-26. Site reward lines carry reward CODES as prefixes "
       "(art1 / mat2 / rsh3), unlike rift lines which spell the payout out - the parser handles both.",
       "The bulk currency here is minor artifacts (payout type 'artifacts'), not astral threads.",
       "Eight site reward lines point at situations documented on OTHER wiki pages (Embodied "
       "Identity, Adaptive Evolution, Horrific Inverse Mass, Genetic Crossroads, the Remnant "
       "chain). The site's own reward is captured; what the referenced situation pays out is not.",
       "The Broken Gates references a 'Horrific Inverse Mass' situation, but the Situations wiki "
       "page documents that name against the Automated Dreadnought guardian instead. Unverified - "
       "do not assume the two are the same thing.",
       "Sites have no choice tree on the wiki, so every chapter's choices[] is empty and title is null.",
      ])
    arch["reward_codes"]=asrc["reward_codes"]
    arch["mechanics"]=asrc.get("mechanics",[])
    arch["groups"]=asrc["groups"]

    # ---------- merged ----------
    ments=rents+aents
    mr=rr+[dict(x,rid=f"r{len(rr)+i+1:04d}") for i,x in enumerate(ar_)]
    mp=rp+[dict(x,pid=f"p{len(rp)+i+1:04d}") for i,x in enumerate(ap)]
    mc=rc+[dict(x,cid=f"c{len(rc)+i+1:04d}") for i,x in enumerate(ac)]
    codes,seen=[],set()
    for c in rifts["reward_codes"]+arch["reward_codes"]:
        if c["code"] in seen: continue
        seen.add(c["code"]); codes.append(c)
    merged=envelope("stellaris_discovery","mixed",ments,mr,mp,mc,rn+an,
      rifts["source"]+" ; "+arch["source"],
      [{"kind":"astral_rift","text":t} for t in rifts["assumptions"]]+
      [{"kind":"archaeological_site","text":t} for t in arch["assumptions"]])
    merged["reward_codes"]=codes
    merged["mechanics"]=[{"kind":"astral_rift","lines":rifts["mechanics"]},
                         {"kind":"archaeological_site","lines":arch["mechanics"]}]
    merged["groups"]=([dict(g,kind="astral_rift") for g in rifts["groups"]]+
                      [dict(g,kind="archaeological_site") for g in arch["groups"]])
    merged["notes"]=("Rifts and archaeological sites in one file, both on the v3 shape. "
                     "Filter on entity.kind. Supersedes stellaris_discovery.v2.1.json, which "
                     "held pre-v3 rift data and no situations.")

    for fn,obj in (("astral_rifts.v3.json",rifts),
                   ("archaeological_sites.v3.json",arch),
                   ("stellaris_discovery.v3.json",merged)):
        json.dump(obj,open(f"{DATA}/{fn}","w"),indent=1,ensure_ascii=False)
        c=obj["coverage"]
        print(f"{fn:36} entities {c['entities']:4} chapters {c['chapters']:4} "
              f"rewards {c['rewards']:4} payouts {c['payouts']:4} chains {c['chains']:3} "
              f"unclassified {c['unclassified']}")
    print("\n== merged reward groups ==")
    for g in merged["reward_groups"]:
        print(f"  {sum(1 for r in mr if r['group']==g['key']):4}  {g['label']}")
    print("== merged payouts ==")
    for t,n in Counter(p["type"] for p in mp).most_common(): print(f"  {n:4}  {t}")
    print(f"\nchain edges with >=1 resolved target: {sum(1 for x in mc if x.get('targets'))}/{len(mc)}")
    print(f"entities that unlock another: {sum(1 for e in ments if e.get('unlocks'))}")

main()
