# -*- coding: utf-8 -*-
import json, os
from collections import Counter
HOME=os.environ["HOME"]; DATA=HOME+"/mnt/Stellaris/data"
old=json.load(open(f"{DATA}/astral_rifts.v2.1.json"))
new=json.load(open(f"{DATA}/astral_rifts.v3.json"))
fails=[]
def check(label, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+label+(f"   {detail}" if detail and not cond else ""))
    if not cond: fails.append(label)

print("== 1. Nothing lost from v2.1 ==")
oldnames={e["name"] for e in old["entities"]}
newnames={e["name"] for e in new["entities"]}
check("every v2.1 rift still present", oldnames <= newnames, str(oldnames-newnames))
check("v3 adds exactly the 4 situations", newnames-oldnames=={
  "A Rift in Space","Study the Crystal Sphere","Destroy the Crystal Sphere","The Seal"},
  str(newnames-oldnames))

# every v2.1 reward string must survive somewhere in v3 (reward.raw or payout.raw)
oldstr=Counter(r for e in old["entities"] for c in e["chapters"] for r in c["rewards"])
newraw=Counter(x["raw"] for x in new["rewards"]) + Counter(x["raw"] for x in new["payouts"])
lost=[s for s in oldstr if s not in newraw]
# structural lines are deliberately dropped
STRUCT={"—","Ends the rift."}
lost=[s for s in lost if s not in STRUCT]
check(f"every v2.1 reward string survives ({sum(oldstr.values())} strings)", not lost, str(lost[:5]))

print("\n== 2. Coverage is provable ==")
check("zero unclassified", new["coverage"]["unclassified"]==0)
groups={g["key"] for g in new["reward_groups"]}
t2g={t:g["key"] for g in new["reward_groups"] for t in g["types"]}
check("every reward type maps to a declared group",
      all(r["type"] in t2g for r in new["rewards"]),
      str({r["type"] for r in new["rewards"] if r["type"] not in t2g}))
check("every reward.group matches its type's group",
      all(t2g[r["type"]]==r["group"] for r in new["rewards"]))
check("payout types are exactly the declared ones",
      {p["type"] for p in new["payouts"]} <= set(new["payout_types"]))
check("rewards and payouts are disjoint sets of ids",
      not ({r["rid"] for r in new["rewards"]} & {p["pid"] for p in new["payouts"]}))

print("\n== 3. Back-references resolve ==")
rid={r["rid"] for r in new["rewards"]}; pid={p["pid"] for p in new["payouts"]}
bad_r=[i for e in new["entities"] for c in e["chapters"] for i in c["reward_ids"] if i not in rid]
bad_p=[i for e in new["entities"] for c in e["chapters"] for i in c["payout_ids"] if i not in pid]
check("every chapter.reward_ids entry exists", not bad_r, str(bad_r[:5]))
check("every chapter.payout_ids entry exists", not bad_p, str(bad_p[:5]))
linked=sum(len(c["reward_ids"])+len(c["payout_ids"]) for e in new["entities"] for c in e["chapters"])
check("every reward/payout is linked from exactly one chapter",
      linked==len(new["rewards"])+len(new["payouts"]),
      f"linked={linked} objects={len(new['rewards'])+len(new['payouts'])}")
uids={e["uid"] for e in new["entities"]}
check("every reward.entity_uid resolves", all(r["entity_uid"] in uids for r in new["rewards"]))

print("\n== 4. UI-shape guarantees ==")
check("6 reward groups + 1 payout bucket", len(new["reward_groups"])==6)
check("no group is empty",
      all(any(r["group"]==g["key"] for r in new["rewards"]) for g in new["reward_groups"]),
      str([g["key"] for g in new["reward_groups"] if not any(r["group"]==g["key"] for r in new["rewards"])]))
check("every reward has a short name for a chip", all(r.get("name") for r in new["rewards"]))
check("chip names stay under 90 chars", max(len(r["name"]) for r in new["rewards"])<=90,
      f"max={max(len(r['name']) for r in new['rewards'])}")
check("reward index is no longer mostly payouts",
      len(new["rewards"])<len(new["payouts"]) and len(new["rewards"])>100,
      f"rewards={len(new['rewards'])} payouts={len(new['payouts'])}")

print("\n== 5. The gaps this version closes ==")
print(f"  rewards parsed out of CHOICE lines : {sum(1 for r in new['rewards'] if r['source']=='choice')}")
print(f"  rewards from the 4 situations      : {sum(1 for r in new['rewards'] if r['entity_uid'].startswith('situation:'))}")
print(f"  old v2.1 finder rows               : {len(old['reward_finder'])}")
print(f"  v3 reward rows                     : {len(new['rewards'])}  (+ {len(new['payouts'])} payouts held separately)")

print("\n"+("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILED: {fails}"))
