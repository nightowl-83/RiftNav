# -*- coding: utf-8 -*-
"""Player-facing text for reward lines: expand wiki reward codes and group choice lines.

Reward values are multipliers of current output with a min-max clamp, never single numbers,
so the expansion always keeps both: "art1 minor artifacts" becomes
"6x minor artifacts (50 / 150 / 250 by game stage)" and "mat2 Society research" becomes
"12x Society research (150–2,000)". The raw line is always kept alongside by the callers.
"""
import re

CODE = r"(?:x\|)?(?:art|mat|rsh|res|uni|inf|ast)\d"
CODE_RX = re.compile(r"\b" + CODE + r"\b")

# Codes the data uses that neither input table carries. Sourced from the wiki's Template:Reward,
# expanded on 2026-09-26 ({{reward|x|inf4}} -> "24x ... output (150~300)").
SUPPLEMENTARY_CODES = [
    {"code": "inf4", "meaning": "24x Influence (150~300)",
     "source": "https://stellaris.paradoxwikis.com/Template:Reward"},
]

# Nouns a code can be followed by, longest first so "Society research" wins over "Society".
NOUNS = ["minor artifacts", "astral threads", "society research", "engineering research",
         "physics research", "exotic gases", "consumer goods", "enclave resources", "living metal",
         "unity", "influence", "minerals", "alloys", "society", "engineering", "physics", "research"]
FIELDS = {"society", "engineering", "physics"}


def _range(s):
    return re.sub(r"(\d)\s*~\s*(\d)", "\\1–\\2", s)


def parse_meaning(meaning):
    """'6x of the named resource (100~1,000)' -> {mult:'6x', noun:None, clamp:'100–1,000'}."""
    s = _range(meaning.strip())
    mult = None
    m = re.match(r"^(\d+x)\s+(.*)$", s)
    if m:
        mult, s = m.group(1), m.group(2)
    clamp = None
    m = re.match(r"^(.*?),\s*clamped to (.*)$", s) or re.match(r"^(.*?)\s*\((.*)\)$", s)
    if m:
        s, clamp = m.group(1).strip(), m.group(2).strip()
    noun = None if s.startswith("of the named") else s
    return {"mult": mult, "noun": noun, "clamp": clamp}


def code_table(*tables):
    """Merge reward_codes tables (earlier tables win) into {code: parsed meaning}."""
    out = {}
    for table in tables:
        for row in table:
            for code in re.split(r"\s*/\s*", row["code"]):
                code = code.replace("x|", "")
                if code not in out:
                    out[code] = dict(parse_meaning(row["meaning"]), meaning=row["meaning"])
    return out


class Translator:
    def __init__(self, table):
        self.table = table
        nouns = "|".join(re.escape(n) for n in NOUNS)
        # "inf4-scale Influence" is the same payout as "inf4 Influence"
        self.rx = re.compile(r"\b(?P<codes>" + CODE + r"(?:/" + CODE + r")*)\b(?:-scale)?(?:\s+(?P<noun>" + nouns + r")\b)?",
                             re.I)

    def _one(self, m):
        codes = [c.lower().replace("x|", "") for c in m.group("codes").split("/")]
        if any(c not in self.table for c in codes):
            return m.group(0)                      # unknown code: left as-is, the validator reports it
        noun = m.group("noun")
        ents = [self.table[c] for c in codes]
        fixed = ents[0]["noun"]
        if fixed:                                   # the code names its own resource: art, uni, inf, ast
            text = fixed
            if noun and noun.lower() not in fixed.lower():
                text += " " + noun                  # a following noun that isn't the same thing stays
        else:
            if noun:
                text = noun + (" research" if noun.lower() in FIELDS else "")
            else:
                text = "research" if codes[0][:3] in ("rsh", "res") else "of the named resource"
        mults = [e["mult"] for e in ents if e["mult"]]
        clamps = [e["clamp"] for e in ents if e["clamp"]]
        head = (" or ".join(mults) + " " if mults else "") + text
        if fixed and not mults:                     # "Small astral threads" reads better lower-cased mid-line
            head = head[0].lower() + head[1:] if m.start() else head
        return head + (" (" + " or ".join(clamps) + ")" if clamps else "")

    def text(self, line):
        """Plain wording for one line. Codes -> multiplier + clamp, 'a~b' ranges -> 'a–b'."""
        return _range(self.rx.sub(self._one, line))

    @staticmethod
    def leftover(text):
        return CODE_RX.findall(text)


# ---------- choice / random / either groups (audit D2) ----------------------------------

HEAD = re.compile(r"^(?P<kw>choice of one|choice of|choice|random)\b\s*(?:-\s*(?P<label>[^:]+?)\s*:)?\s*:?\s*(?P<rest>.*)$", re.I)
OR = re.compile(r"^or\b\s*(?:(?P<label>[a-z][\w ,'-]{2,40}?):\s+)?(?P<rest>.*)$", re.I)
ROUTING = re.compile(r"^choice that sets a flag", re.I)


def _split_top(s, sep):
    """Split on sep only outside parentheses and brackets."""
    out, depth, cur, i = [], 0, "", 0
    while i < len(s):
        ch = s[i]
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if depth == 0 and s.startswith(sep, i):
            out.append(cur); cur = ""; i += len(sep); continue
        cur += ch; i += 1
    out.append(cur)
    return [x.strip(" ,.") for x in out if x.strip(" ,.")]


def _inline_options(rest):
    parts = _split_top(rest, ", or ")
    if len(parts) > 1:
        head = _split_top(parts[0], ", ")
        return head + parts[1:]
    return _split_top(rest, " or ")


def group_lines(lines):
    """Split a chapter's reward lines into guaranteed lines and option groups.

    Returns (guaranteed_idx, groups) where groups are
    [{kind: 'choice'|'random'|'either', options: [{label, idx}]}] and idx points into `lines`.
      choice  - "Choice: …" / "Choice of …" (+ "OR …" lines): the player picks
      random  - "Random: …" + "OR …" lines: the game picks
      either  - "OR …" with no header: the wiki doesn't say who picks
    A lone "Choice: A, or B" line is split at its top-level ", or" / " or ".
    """
    guaranteed, groups, cur = [], [], None
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        h, o = HEAD.match(line), OR.match(line)
        if h and not ROUTING.match(line):
            kw = h.group("kw").lower()
            cur = {"kind": "random" if kw == "random" else "choice", "options": [],
                   "_inline": h.group("rest"), "_label": h.group("label"), "_head": i}
            cur["options"].append({"label": h.group("label"), "idx": i, "text": h.group("rest")})
            groups.append(cur)
            if kw == "choice of one":                   # the options are this line and every line after it
                for j in range(i + 1, len(lines)):
                    cur["options"].append({"label": None, "idx": j, "text": lines[j].strip()})
                i = len(lines); continue
        elif o:
            if cur is None:                             # bare OR: the previous line is the first option
                prev = guaranteed.pop() if guaranteed else None
                cur = {"kind": "either", "options": []}
                if prev is not None:
                    cur["options"].append({"label": None, "idx": prev, "text": lines[prev].strip()})
                groups.append(cur)
            cur["options"].append({"label": o.group("label"), "idx": i, "text": o.group("rest")})
        else:
            cur = None
            guaranteed.append(i)
        i += 1
    kept = []
    for g in groups:                                    # a header line with no OR lines: split inline
        if len(g["options"]) == 1 and g["kind"] != "either":
            only = g["options"][0]
            parts = _inline_options(only["text"])
            g["options"] = [{"label": only["label"], "idx": only["idx"], "text": p} for p in parts]
        for k in ("_inline", "_label", "_head"):
            g.pop(k, None)
        if g["kind"] == "random" and len(g["options"]) < 2:
            # "Random: Biology (Genetics) technology" is one random tech, not a set of outcomes
            guaranteed.append(g["options"][0]["idx"])
            continue
        kept.append(g)
    return sorted(guaranteed), kept
