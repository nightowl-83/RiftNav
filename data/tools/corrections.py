# -*- coding: utf-8 -*-
"""Sourced corrections to the v2.1 build inputs.

The v2.1 files are never hand-edited. When the wiki shows an input line is wrong, the fix goes
here with the page, revision and the exact wikitext it rests on, and the build applies it. Every
line a correction removes is recorded in the output's corrections[], so the validator can still
prove nothing was silently lost.
"""

CORRECTIONS = [
 {
  "entity_uid": "site:ancient-capital-site",
  "source": "https://stellaris.paradoxwikis.com/Archaeological_site",
  "revid": 118610,
  "checked": "2026-09-26",
  # sha256 of the site's table row in that revision; the row lists five numbered chapters
  "evidence_sha256": "c762b3383f954bec0e3a99a600456f8082a2a337a4132bad8ccb6ffbae24fc28",
  "why": "The wiki lists five chapters for Ancient Capital Site. The input's chapter 6 was a "
         "placeholder ('see wiki, payout is the art/soc pair again'), not a captured chapter, and "
         "the Skrand Sharpbeak experience line sits under chapter 2 on the wiki, not chapter 3.",
  "ops": [
   {"op": "drop_chapter", "chapter": "6"},
   {"op": "move_line", "from": "3", "to": "2",
    "line": "Skrand Sharpbeak, if you have him, gains 800 experience"},
  ],
 },
]


def apply(entities):
    """Apply CORRECTIONS in place. Returns the audit records for the dataset's corrections[]."""
    by_uid = {e["uid"]: e for e in entities}
    records = []
    for c in CORRECTIONS:
        e = by_uid[c["entity_uid"]]
        for op in c["ops"]:
            chs = {ch["id"]: ch for ch in e["chapters"]}
            if op["op"] == "drop_chapter":
                gone = chs[op["chapter"]]
                e["chapters"] = [ch for ch in e["chapters"] if ch["id"] != op["chapter"]]
                removed = list(gone["rewards"]) + list(gone.get("choices", []))
            elif op["op"] == "move_line":
                src, dst = chs[op["from"]], chs[op["to"]]
                src["rewards"] = [l for l in src["rewards"] if l != op["line"]]
                dst["rewards"] = list(dst["rewards"]) + [op["line"]]
                removed = []
            else:
                raise ValueError(op)
            records.append({"entity": e["name"], "entity_uid": e["uid"], **op,
                            "removed_lines": removed, "source": c["source"], "revid": c["revid"],
                            "checked": c["checked"], "evidence_sha256": c["evidence_sha256"],
                            "why": c["why"]})
        for i, ch in enumerate(sorted(e["chapters"], key=lambda x: x["index"]), 1):
            ch["index"] = i
    return records
