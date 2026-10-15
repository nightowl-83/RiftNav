# -*- coding: utf-8 -*-
"""Diff a fresh relic capture against the committed one.

Run this AFTER re-capturing with capture/capture_relics.js. It compares only the five
fields the dataset actually consumes, because everything else on the Relics page
(score, source wording, DLC icons) churns on ordinary wiki edits and would bury the signal.

The baseline is read from git, not from disk, so saving a new capture over
relics.wiki.json cannot destroy the thing you are comparing against.

    python3 data/tools/diff_relic_capture.py
"""
import json, subprocess, sys, os
from paths import DATA

CAPTURE = os.path.join(DATA, "tools", "capture", "relics.wiki.json")
REL = "data/tools/capture/relics.wiki.json"
FIELDS = ["passive", "triumph", "triumph_cost", "triumph_cooldown_days", "activatable"]

def baseline():
    repo = os.path.dirname(DATA)
    try:
        out = subprocess.run(["git", "-C", repo, "show", f"HEAD:{REL}"],
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        sys.exit(f"Cannot read {REL} from git HEAD. Is it committed?")
    return json.loads(out)

def main():
    old, new = baseline(), json.load(open(CAPTURE))
    print("=== provenance ===")
    for k in ("revid", "wiki_version", "wikitext_sha256", "captured"):
        o, n = old.get(k), new.get(k)
        print(f"  {k:16} {str(o)[:20]:22} -> {str(n)[:20]:22} {'(changed)' if o != n else ''}")
    if old.get("wikitext_sha256") == new.get("wikitext_sha256"):
        print("\nThe page wikitext is byte-identical. Nothing to review.")
        return 0

    o = {r["name"]: r for r in old["relics"]}
    n = {r["name"]: r for r in new["relics"]}
    added, removed = sorted(set(n) - set(o)), sorted(set(o) - set(n))
    print(f"\n=== relics: {len(o)} -> {len(n)} ===")
    if added:   print("  added  :", ", ".join(added))
    if removed: print("  removed:", ", ".join(removed))

    changed, cooldown_changed = [], []
    for name in sorted(set(o) & set(n)):
        for f in FIELDS:
            if o[name].get(f) != n[name].get(f):
                changed.append((name, f, o[name].get(f), n[name].get(f)))
                if f == "triumph_cooldown_days":
                    cooldown_changed.append(name)

    print(f"\n=== consumed-field changes: {len(changed)} ===")
    for name, f, a, b in changed:
        print(f"  {name[:30]:32} {f}")
        print(f"      was: {str(a)[:92]}")
        print(f"      now: {str(b)[:92]}")

    print("\n=== verdict ===")
    if not changed and not added and not removed:
        print("  Page edited, but no field this dataset consumes changed. Re-pin the revid in")
        print("  data/sources.json and move on - no data correction needed.")
    else:
        print(f"  {len(changed)} field change(s) across {len({c[0] for c in changed})} relic(s).")
        if cooldown_changed:
            print(f"  COOLDOWNS CHANGED on: {', '.join(cooldown_changed)}")
            print("  -> timing.activation is derived from these. Rebuild and re-check the 22")
            print("     activation rewards: python3 data/tools/build_all_v3.py && validate_all_v3.py")
        else:
            print("  No cooldown changed, so timing.activation is unaffected.")
        print("  -> rebuild, then update data/sources.json (verified_revid + status).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
