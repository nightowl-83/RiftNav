# -*- coding: utf-8 -*-
"""The relic catalogue, from the wiki's Relics page, and the links from relic rewards to it.

Input is data/tools/capture/relics.wiki.json, produced by capture/capture_relics.js from one
wiki revision. The build checks the capture's hash before using it, so a hand-edited capture
fails loudly instead of flowing into the dataset.
"""
import hashlib, json, os, re
from collections import Counter
from paths import TOOLS

CAPTURE = os.path.join(TOOLS, "capture", "relics.wiki.json")
CAPTURE_META = ("captured", "captured_with", "capture_sha256")

# Relic rewards that name nothing on the Relics page. Listed, never guessed.
LINK_EXCEPTIONS = {
    ("rift:the-advisor", "Advisor Core"):
        "The Relics page (revision 119679) has no 'Advisor Core' entry. The Advisor rift's "
        "reward line names it, but there is no catalogue record to link it to.",
}


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def canonical_sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode()).hexdigest()


def load_capture():
    cap = json.load(open(CAPTURE))
    body = {k: v for k, v in cap.items() if k not in CAPTURE_META}
    got = canonical_sha(body)
    if got != cap["capture_sha256"]:
        raise SystemExit(f"relics.wiki.json does not match its capture hash ({got}). "
                         "Re-run capture/capture_relics.js rather than editing the file.")
    return cap


def build(cap, translate):
    """Catalogue entries, one per relic (upgradeable relics: one per stage)."""
    names = Counter(r["name"] for r in cap["relics"])
    out = []
    for r in cap["relics"]:
        rid = slug(r["name"]) if names[r["name"]] == 1 else f"{slug(r['name'])}-{r['stage']}"
        out.append({
            "id": rid, "uid": f"relic:{rid}", "name": r["name"],
            "category": r["category"], "category_key": slug(r["category"]),
            "subsection": r["subsection"], "stage": r.get("stage"),
            "passive": [translate(x) for x in r["passive"]],
            "triumph": [translate(x) for x in r["triumph"]],
            "triumph_cost": r["triumph_cost"],
            "triumph_cooldown_days": r["triumph_cooldown_days"],
            "activatable": r["activatable"],
            "source": r["source"], "source_kind": r["source_kind"],
            "score": r["score"], "dlc": r["dlc"], "dlc_codes": r["dlc_codes"],
            "raw": {"passive": r["passive"], "triumph": r["triumph"]},
            "rewarded_by": [],
        })
    return out


def _variants(name):
    v = [name]
    if name.lower().startswith("the "):
        v.append(name[4:])                      # "Omnicodex relic" -> The Omnicodex
    return v


def link(rewards, catalogue):
    """Set relic_id on every type=='relic' reward whose raw line names exactly one catalogue
    relic (whole words, longest names first). Returns (unmatched, ambiguous) for reporting;
    unmatched rewards on LINK_EXCEPTIONS carry relic_link_exception instead."""
    # upgradeable relics share a name across stages; a reward that names one links its final stage
    by_name = {}
    for r in catalogue:
        for v in _variants(r["name"]):
            prev = by_name.get(v.lower())
            if prev is None or (r.get("stage") or 0) > (prev.get("stage") or 0):
                by_name[v.lower()] = r
    keys = sorted(by_name, key=len, reverse=True)
    unmatched, ambiguous = [], []
    for x in rewards:
        if x["type"] != "relic":
            continue
        raw, hits = x["raw"].lower(), []
        for k in keys:
            if re.search(r"(?<![\w'])" + re.escape(k) + r"(?![\w'])", raw):
                if not any(k in h for h in hits):
                    hits.append(k)
        ids = sorted({by_name[h]["id"] for h in hits})
        if len(ids) == 1:
            x["relic_id"] = ids[0]
        elif not ids:
            why = LINK_EXCEPTIONS.get((x["entity_uid"], x["raw"]))
            x["relic_id"] = None
            if why:
                x["relic_link_exception"] = why
            else:
                unmatched.append(x)
        else:
            x["relic_id"] = None
            ambiguous.append((x, ids))
    return unmatched, ambiguous
