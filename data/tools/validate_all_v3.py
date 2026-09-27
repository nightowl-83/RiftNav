# -*- coding: utf-8 -*-
import json, os, re
from collections import Counter
from paths import DATA, UI
import relics as relic_catalogue
from reward_text import CODE_RX
L=lambda f: json.load(open(f"{DATA}/{f}"))
fails=[]
def check(label, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+label+(f"   {detail}" if detail and not cond else ""))
    if not cond: fails.append(label)

r21,a21 = L("astral_rifts.v2.1.json"), L("archaeological_sites.v2.1.json")
r3,a3,m3 = L("astral_rifts.v3.json"), L("archaeological_sites.v3.json"), L("stellaris_discovery.v3.json")
rl = L("relics.v3.json")
def js(fn):
    s=open(os.path.join(UI,fn)).read()
    return s, json.loads(s[s.index("{"):s.rindex("}")+1])
rift_src, RD = js("rift-data.js")
dig_src, DD = js("dig-data.js")

print("== 1. Nothing lost from v2.1 ==")
for old,new,label in ((r21,r3,"rift"),(a21,a3,"site")):
    oldstr=Counter(x for e in old["entities"] for c in e["chapters"] for x in c["rewards"])
    newraw=(Counter(x["raw"] for x in new["rewards"])+Counter(x["raw"] for x in new["payouts"])
            +Counter(x["raw"] for x in new["chains"])+Counter(x["raw"] for x in new["ignored_lines"]))
    corrected={l for c in new.get("corrections",[]) for l in c["removed_lines"]}
    lost=[s for s in oldstr if s not in newraw and s not in corrected]
    check(f"every v2.1 {label} reward string accounted for ({sum(oldstr.values())})", not lost, str(lost[:4]))
    check(f"{label}: dropped lines are recorded, not silently discarded",
          len(new["ignored_lines"])==new["coverage"]["structural_lines_ignored"])
    check(f"every v2.1 {label} entity present",
          {e["name"] for e in old["entities"]} <= {e["name"] for e in new["entities"]})

print("\n== 2. Coverage provable ==")
for d,n in ((r3,"rifts"),(a3,"sites"),(m3,"merged")):
    check(f"{n}: zero unclassified", d["coverage"]["unclassified"]==0)
    t2g={t:g["key"] for g in d["reward_groups"] for t in g["types"]}
    bad={x["type"] for x in d["rewards"] if x["type"] not in t2g}
    check(f"{n}: every reward type maps to a group", not bad, str(bad))
    check(f"{n}: group field agrees with the type map",
          all(t2g[x["type"]]==x["group"] for x in d["rewards"]))
    check(f"{n}: payout types are declared",
          {p["type"] for p in d["payouts"]} <= set(d["payout_types"]),
          str({p["type"] for p in d["payouts"]} - set(d["payout_types"])))

print("\n== 3. Ids and back-references ==")
for d,n in ((r3,"rifts"),(a3,"sites"),(m3,"merged")):
    rid={x["rid"] for x in d["rewards"]}; pid={x["pid"] for x in d["payouts"]}; cid={x["cid"] for x in d["chains"]}
    check(f"{n}: reward ids unique", len(rid)==len(d["rewards"]))
    check(f"{n}: payout ids unique", len(pid)==len(d["payouts"]))
    check(f"{n}: chain ids unique", len(cid)==len(d["chains"]))
    linked=sum(len(c["reward_ids"])+len(c["payout_ids"])+len(c["chain_ids"])
               for e in d["entities"] for c in e["chapters"])
    check(f"{n}: every object linked from exactly one chapter",
          linked==len(d["rewards"])+len(d["payouts"])+len(d["chains"]),
          f"linked={linked} objects={len(d['rewards'])+len(d['payouts'])+len(d['chains'])}")
    uids={e["uid"] for e in d["entities"]}
    check(f"{n}: every entity_uid resolves",
          all(x["entity_uid"] in uids for x in d["rewards"]+d["payouts"]+d["chains"]))

print("\n== 4. Merged file is exactly its parts ==")
for k in ("entities","chapters","rewards","payouts","chains","structural_lines_ignored"):
    check(f"merged {k} == rifts + sites",
          m3["coverage"][k]==r3["coverage"][k]+a3["coverage"][k],
          f"{m3['coverage'][k]} vs {r3['coverage'][k]}+{a3['coverage'][k]}")
check("merged uids unique across kinds",
      len({e["uid"] for e in m3["entities"]})==len(m3["entities"]))
check("merged covers both kinds", {e["kind"] for e in m3["entities"]} >=
      {"astral_rift","astral_rift_situation","archaeological_site"})

print("\n== 5. Chain graph ==")
names={e["name"] for e in m3["entities"]}
bad=[t for c in m3["chains"] for t in c["targets"] if t not in names]
check("every resolved chain target is a real entity", not bad, str(bad[:4]))
check("unresolved chains are typed, not silently empty",
      all(c["target_kind"]!="unknown" or c["targets"] for c in m3["chains"]))
check("no entity unlocks itself",
      all(e["name"] not in e["unlocks"] for e in m3["entities"]))

print("\n== 6. UI-shape guarantees ==")
check("6 reward groups in every file", all(len(d["reward_groups"])==6 for d in (r3,a3,m3)))
check("no empty group in the merged file",
      all(any(x["group"]==g["key"] for x in m3["rewards"]) for g in m3["reward_groups"]))
check("every reward has a chip name", all(x.get("name") for x in m3["rewards"]))
check("chip names <= 90 chars", max(len(x["name"]) for x in m3["rewards"])<=90)
check("rewards are a minority of typed objects (payouts held separately)",
      len(m3["rewards"]) < len(m3["payouts"]))

print("\n== 7. Sourced corrections ==")
for c in a3.get("corrections",[]):
    check(f"correction on {c['entity']} ({c['op']}) cites a wiki revision and evidence hash",
          c.get("revid") and c.get("source","").startswith("https://") and len(c.get("evidence_sha256",""))==64)
acs=next(e for e in a3["entities"] if e["uid"]=="site:ancient-capital-site")
check("Ancient Capital Site has the wiki's five chapters", len(acs["chapters"])==5, str(len(acs["chapters"])))

print("\n== 8. Relic catalogue ==")
relic_catalogue.load_capture()                     # raises if the capture was edited by hand
check("relic capture matches its hash (not hand-edited)", True)
ids=[r["id"] for r in rl["relics"]]
check(f"relic ids unique ({len(ids)})", len(ids)==len(set(ids)))
check("merged file carries the same catalogue", [r["id"] for r in m3.get("relics",[])]==ids)
check("every relic has a passive effect and a category",
      all(r["passive"] and r["category"] for r in rl["relics"]))
catids=set(ids); exc={(x["entity_uid"],x["raw"]) for x in rl["link_exceptions"]}
for d,n in ((r3,"rifts"),(a3,"sites"),(m3,"merged")):
    rel=[x for x in d["rewards"] if x["type"]=="relic"]
    bad=[x["raw"] for x in rel if x.get("relic_id") not in catids and (x["entity_uid"],x["raw"]) not in exc]
    check(f"{n}: every relic reward links to the catalogue or is a documented exception ({len(rel)})",
          not bad, str(bad[:3]))
check("exceptions are documented", all(x["why"] for x in rl["link_exceptions"]))
check("rewarded_by points back at real rewards",
      all(any(x["rid"]==rid and x.get("relic_id")==r["id"] for x in m3["rewards"])
          for r in rl["relics"] for rid in r["rewarded_by"]))

print("\n== 9. UI data files are generated from v3 ==")
for src,fn in ((rift_src,"rift-data.js"),(dig_src,"dig-data.js")):
    check(f"{fn} carries the generated-file header", src.startswith("// GENERATED FILE - DO NOT EDIT BY HAND."))
check("rift-data.js: every v3 rift and situation present, in order",
      [x["name"] for x in RD["rifts"]]==[e["name"] for e in r3["entities"]])
check("rift-data.js: all 4 rift situations present",
      sum(1 for x in RD["rifts"] if x.get("kind")=="astral_rift_situation")==4)
check("rift-data.js counts match v3",
      RD["counts"]["entries"]==r3["coverage"]["entities"] and RD["counts"]["chapters"]==r3["coverage"]["chapters"]
      and RD["counts"]["rewards"]==r3["coverage"]["rewards"]==len(RD["rewards"]),
      str(RD["counts"]))
check("rift-data.js chapters == v3 chapters",
      sum(len(x["chapters"]) for x in RD["rifts"])==r3["coverage"]["chapters"])
check("rift-data.js: every v3 reward id present", sorted(x["rid"] for x in RD["rewards"])==sorted(x["rid"] for x in r3["rewards"]))
check("dig-data.js: every v3 site present, in order", [x["name"] for x in DD["sites"]]==[e["name"] for e in a3["entities"]])
check("dig-data.js counts match v3",
      DD["counts"]["sites"]==a3["coverage"]["entities"] and DD["counts"]["phases"]==a3["coverage"]["chapters"]
      and DD["counts"]["rewards"]==a3["coverage"]["rewards"]==len(DD["rewards"]), str(DD["counts"]))
check("dig-data.js phases == v3 chapters", sum(len(x["chapters"]) for x in DD["sites"])==a3["coverage"]["chapters"])
LEGACY={"rift":["name","group","req","restrict","notes","chapters"],"rch":["id","title","rewards","choices","ends"],
        "rrow":["name","rift","path","cat"],"site":["id","name","group","groupLabel","dlc","precursor","system","req","restrict","notes","chapters"],
        "sch":["id","rewards"],"drow":["cat","name","site","siteId","chapter","groupLabel"]}
has=lambda rows,keys: all(all(k in r for k in keys) for r in rows)
check("UI contract: every field the UI already reads is still present",
      has(RD["rifts"],LEGACY["rift"]) and has([c for x in RD["rifts"] for c in x["chapters"]],LEGACY["rch"])
      and has(RD["rewards"],LEGACY["rrow"]) and has(DD["sites"],LEGACY["site"])
      and has([c for x in DD["sites"] for c in x["chapters"]],LEGACY["sch"]) and has(DD["rewards"],LEGACY["drow"])
      and all(k in DD for k in ("sites","rewards","mechanics","groups")))

RAWKEYS={"raw","rawChoices","meta"}   # verbatim source lines and provenance are not player text
def strings(o, key=None):
    if key in RAWKEYS: return
    if isinstance(o,str): yield o
    elif isinstance(o,list):
        for v in o: yield from strings(v, key)
    elif isinstance(o,dict):
        for k,v in o.items(): yield from strings(v, k)
ui_text=list(strings(RD))+list(strings(DD))
codes=[t for t in ui_text if CODE_RX.search(t)]
print(f"  untranslated reward codes left in UI text: {len(codes)}")
for t in codes[:20]: print("     ", t[:110])
check("no untranslated reward codes in the UI files", not codes)
tildes=[t for t in ui_text if re.search(r"\d\s*~\s*\d",t)]
check("no tilde ranges in the UI files (min–max instead)", not tildes, str(tildes[:3]))
PLACEHOLDER=re.compile(r"\(final chapter|payout is the .* again|placeholder|\bTODO\b|\bTBD\b",re.I)
ph=[t for t in ui_text if PLACEHOLDER.search(t)]+[x["raw"] for d in (r3,a3) for x in d["rewards"]+d["payouts"] if PLACEHOLDER.search(x["raw"])]
check("no placeholder text in the UI files or the v3 rewards", not ph, str(ph[:3]))
check("the 6x glossary entry is in dig mechanics", any('"6x"' in m for m in DD["mechanics"]))
groups=[g for x in RD["rifts"] for c in x["chapters"] for g in c["rewardChoices"]]+\
       [g for x in DD["sites"] for c in x["chapters"] for g in c["choices"]]
check(f"every choice / random / either group has >= 2 options ({len(groups)} groups)",
      all(len(g["options"])>=2 for g in groups))
check("choice groups are typed", all(g["kind"] in ("choice","random","either") for g in groups))
gi=[(c,i) for x in DD["sites"] for c in x["chapters"] for i in c["guaranteed"]]
def covers(c, key):
    grouped={o["line"] for g in c[key] for o in g["options"]}
    return not (grouped & set(c["guaranteed"])) and grouped | set(c["guaranteed"]) == set(range(len(c["raw"])))
check("dig chapters: every line is either guaranteed or in exactly one option group",
      all(covers(c,"choices") for x in DD["sites"] for c in x["chapters"]))
check("rift chapters: every line is either guaranteed or in exactly one option group",
      all(covers(c,"rewardChoices") for x in RD["rifts"] for c in x["chapters"]))
bad_paths=[]
for row in RD["rewards"]:
    rift=next(x for x in RD["rifts"] if x["name"]==row["rift"])
    ids={c["id"]:c for c in rift["chapters"]}
    for seg in [s_.strip() for s_ in row["path"].split("->")]:
        m=re.match(r'^(\S+)(?:\s+"([^"]*)")?(?:\s+.*)?$',seg)   # trailing prose is allowed, as in the UI
        ch=ids.get(m.group(1)) if m else None
        if not ch or (m.group(2) and m.group(2) not in [c["text"] for c in ch["choices"]]):
            bad_paths.append((row["rift"],row["path"])); break
check(f"every rift reward path resolves to real chapters and choices ({len(RD['rewards'])})",
      not bad_paths, str(bad_paths[:3]))
rows_all=RD["rewards"]+DD["rewards"]
bad_short=[(x.get("short"),x["name"]) for x in rows_all if not x.get("short") or len(x["short"])>60]
check(f"every rift and dig reward has a short name of 1-60 characters ({len(rows_all)})", not bad_short, str(bad_short[:3]))
opts=[o for x in RD["rifts"] for c in x["chapters"] for g in c["rewardChoices"] for o in g["options"]]+\
     [o for x in DD["sites"] for c in x["chapters"] for g in c["choices"] for o in g["options"]]
check(f"every choice option has a short label of 1-60 characters ({len(opts)})",
      all(o.get("short") and len(o["short"])<=60 for o in opts))
rrows=[x for x in RD["rewards"]+DD["rewards"] if x["type"]=="relic"]
check(f"every UI relic reward carries relic details or a documented note ({len(rrows)})",
      all(x.get("relic") or x.get("relicNote") for x in rrows))

print(f"\n{'ALL CHECKS PASSED' if not fails else str(len(fails))+' FAILED: '+str(fails)}")
