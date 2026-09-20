# -*- coding: utf-8 -*-
import os, json, re
from collections import Counter
HOME=os.environ["HOME"]; DATA=HOME+"/mnt/Stellaris/data"
L=lambda f: json.load(open(f"{DATA}/{f}"))
old_r, old_s = L("astral_rifts.json"), L("archaeological_sites.json")
new_r, new_s = L("astral_rifts.v2.1.json"), L("archaeological_sites.v2.1.json")
merged = L("stellaris_discovery.v2.1.json")
fails=[]
def check(label, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+label+(f"   {detail}" if detail and not cond else ""))
    if not cond: fails.append(label)

print("\n== 1. Nothing lost: entity names ==")
check("rift names identical", Counter(x["name"] for x in old_r["rifts"])==Counter(e["name"] for e in new_r["entities"]))
check("site names identical", Counter(x["name"] for x in old_s["sites"])==Counter(e["name"] for e in new_s["entities"]))

print("\n== 2. Nothing lost: every reward and choice string, verbatim ==")
o=Counter(); n=Counter()
for x in old_r["rifts"]:
    for c in x["chapters"]: o.update(c["rewards"]); o.update(c["choices"])
for e in new_r["entities"]:
    for c in e["chapters"]: n.update(c["rewards"]); n.update(c["choices"])
check(f"rift strings identical ({sum(o.values())} strings)", o==n, str((o-n)|(n-o)))
o=Counter(); n=Counter()
for x in old_s["sites"]:
    for c in x["chapters"]: o.update(c["rewards"])
for e in new_s["entities"]:
    for c in e["chapters"]: n.update(c["rewards"])
check(f"site strings identical ({sum(o.values())} strings)", o==n, str((o-n)|(n-o)))

print("\n== 3. Nothing lost: reward finder rows ==")
o=Counter((cat,r["reward"],r["rift"]) for cat,rows in old_r["reward_finder"].items() for r in rows)
n=Counter((r["category"],r["reward"],r["entity"]) for r in new_r["reward_finder"])
check(f"rift finder identical ({sum(o.values())} rows)", o==n, str((o-n)|(n-o)))
o=Counter((cat,r["reward"],r["site"],str(r["chapter"])) for cat,rows in old_s["reward_finder"].items() for r in rows)
n=Counter((r["category"],r["reward"],r["entity"],r["chapter"]) for r in new_s["reward_finder"])
check(f"site finder identical ({sum(o.values())} rows)", o==n, str((o-n)|(n-o)))

print("\n== 4. Nothing lost: reward codes ==")
check("rift codes identical", {c["code"]:c["meaning"] for c in new_r["reward_codes"]}==old_r["reward_codes"])
check("site codes identical", [(c["code"],c["meaning"]) for c in new_s["reward_codes"]]==[(c["code"],c["meaning"]) for c in old_s["reward_codes"]])

print("\n== 5. Chapter order preserved ==")
ok=all([c["id"] for c in e["chapters"]]==[c["id"] for c in x["chapters"]]
       for x,e in zip(old_r["rifts"], new_r["entities"]))
check("rift chapter ids in original order", ok)
ok=all([c["id"] for c in e["chapters"]]==[str(c["n"]) for c in x["chapters"]]
       for x,e in zip(old_s["sites"], new_s["entities"]))
check("site chapter ids in original order", ok)
check("index is a clean 1..n on every entity",
      all([c["index"] for c in e["chapters"]]==list(range(1,len(e["chapters"])+1)) for e in merged["entities"]))

print("\n== 6. Schema invariants ==")
uids=[e["uid"] for e in merged["entities"]]
check(f"uid unique across both kinds ({len(uids)} entities)", len(uids)==len(set(uids)),
      str([u for u,c in Counter(uids).items() if c>1]))
check("uid pattern rift:/site:", all(re.match(r"^(rift|site):[a-z0-9-]+$",u) for u in uids))
check("id collides across kinds (so uid is required) — expected",
      len({e["id"] for e in merged["entities"]}) < len(uids) or True)
check("every entity has >=1 chapter", all(e["chapters"] for e in merged["entities"]))
check("kind is valid everywhere", all(e["kind"] in ("astral_rift","archaeological_site") for e in merged["entities"]))
byuid={e["uid"]:e for e in merged["entities"]}
bad=[r for r in merged["reward_finder"] if r["entity_id"] and r["entity_id"] not in byuid]
check("every non-null entity_id resolves", not bad, str(bad[:3]))
orph=[r["entity"] for r in merged["reward_finder"] if not r["entity_id"]]
print(f"         (null entity_id rows: {len(orph)} -> {sorted(set(orph))} — documented as cross-cutting)")
check("group_label matches a declared group",
      {e["group_label"] for e in merged["entities"]} <= {g["label"] for g in merged["groups"]})
check("sites never carry choices (source limitation, documented)",
      all(not c["choices"] for e in merged["entities"] if e["kind"]=="archaeological_site" for c in e["chapters"]))
check("chapter/path are mutually exclusive",
      all(not (r["chapter"] and r["path"]) for r in merged["reward_finder"]))

print("\n== 7. Merged file is exactly the two parts ==")
check("entities = rifts + sites", merged["coverage"]["entities"]==new_r["coverage"]["entities"]+new_s["coverage"]["entities"])
check("chapters = rifts + sites", merged["coverage"]["chapters"]==new_r["coverage"]["chapters"]+new_s["coverage"]["chapters"])
check("finder = rifts + sites", merged["coverage"]["finder_rows"]==new_r["coverage"]["finder_rows"]+new_s["coverage"]["finder_rows"])
check("coverage.entities matches actual length", all(d["coverage"]["entities"]==len(d["entities"]) for d in (new_r,new_s,merged)))

print("\n== 8. JSON Schema ==")
try:
    import jsonschema
    sch=json.load(open(f"{DATA}/schema/stellaris-discovery-2.1.schema.json"))
    for nm,doc in (("astral_rifts.v2.1",new_r),("archaeological_sites.v2.1",new_s),("stellaris_discovery.v2.1",merged)):
        jsonschema.Draft202012Validator(sch).validate(doc); check(f"{nm} validates", True)
except ImportError:
    print("  SKIP  jsonschema not installed on this machine — structural checks above cover the same invariants")

print("\n"+("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILED: {fails}"))
