# -*- coding: utf-8 -*-
import json, os
from collections import Counter
DATA=os.environ["HOME"]+"/mnt/Stellaris/data"
L=lambda f: json.load(open(f"{DATA}/{f}"))
fails=[]
def check(label, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+label+(f"   {detail}" if detail and not cond else ""))
    if not cond: fails.append(label)

r21,a21 = L("astral_rifts.v2.1.json"), L("archaeological_sites.v2.1.json")
r3,a3,m3 = L("astral_rifts.v3.json"), L("archaeological_sites.v3.json"), L("stellaris_discovery.v3.json")

print("== 1. Nothing lost from v2.1 ==")
for old,new,label in ((r21,r3,"rift"),(a21,a3,"site")):
    oldstr=Counter(x for e in old["entities"] for c in e["chapters"] for x in c["rewards"])
    newraw=(Counter(x["raw"] for x in new["rewards"])+Counter(x["raw"] for x in new["payouts"])
            +Counter(x["raw"] for x in new["chains"])+Counter(x["raw"] for x in new["ignored_lines"]))
    lost=[s for s in oldstr if s not in newraw]
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

print(f"\n{'ALL CHECKS PASSED' if not fails else str(len(fails))+' FAILED: '+str(fails)}")
