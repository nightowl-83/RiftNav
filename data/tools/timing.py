# -*- coding: utf-8 -*-
"""Derive the temporal shape of a reward.

Replaces the v3 `recurring` type, which special-cased one row (The Seal) and said
nothing about the other 28 rewards that carry a time dimension.

Canonical unit is DAYS. A Stellaris year is 360 days — confirmed by the relic
catalogue, whose only cooldown values (900 / 1800 / 3600) divide exactly by 360
(2.5y / 5y / 10y) and give fractions under 365.

`mode` is the dominant shape, for a chip or a label. The other fields are
independently nullable, so a reward that arrives late AND then lasts 10 years
carries both `delay_days` and `days`.
"""
import re

YEAR_DAYS = 360

MODES = ("cycle", "uses", "duration", "delayed", "while_active", "permanent", "instant")

_CYCLE   = re.compile(r"(?:recurring |repeats )?(?:every|each) (\d+) years?", re.I)
_USES    = re.compile(r"usable (\d+) times?|^(\d+) (?:Fractal Seed )?planetary decisions", re.I)
_ACTIVE  = re.compile(r"while active|while .{0,24}(?:present|on the council)", re.I)
_DURATION= re.compile(r"for (\d+)(?:-(\d+))? (years?|months?|days?)", re.I)
_DELAY_Y = re.compile(r"(?:returns?|arrives?|appears?|comes? back)(?:[^.]{0,40}?)\b(?:in|after) (?:about |~)?(\d+)(?:-(\d+))? years?"
                      r"|\b(?:after|in) (?:about |~)?(\d+)(?:-(\d+))? years?\b"
                      r"|(\d+)(?:-(\d+))? years? later", re.I)
_DELAY_M = re.compile(r"\b(?:within|after|in) (?:about |~)?(\d+)(?:-(\d+))? months?", re.I)
_DELAY_D = re.compile(r"\b(?:after|in) (?:about |~)?(\d+)(?:-(\d+))? days?", re.I)
_PERM    = re.compile(r"\bpermanent\b", re.I)

def _mid(a, b):
    """A range like '30-40 days' becomes its midpoint; the wiki states ranges, a UI needs a number."""
    a = int(a)
    return a if not b else (a + int(b)) // 2

def derive(raw, reward_type=None, relic=None):
    """raw: the reward line. relic: the matching relics.v3.json record, if any."""
    t = {"mode": "instant", "days": None, "years": None,
         "cycle_days": None, "cycle_years": None, "uses": None,
         "delay_days": None, "delay_years": None,
         "activation": None, "derived_from": "default", "match": None}

    def stamp(mode, match):
        t["mode"] = mode; t["match"] = match; t["derived_from"] = "text"

    # duration and delay are independent of the mode, so read them first
    m = _DURATION.search(raw)
    if m:
        n = _mid(m.group(1), m.group(2))
        unit = m.group(3).lower()
        per = YEAR_DAYS if unit.startswith("year") else 30 if unit.startswith("month") else 1
        t["days"] = n * per
        t["years"] = round(t["days"] / YEAR_DAYS, 2)

    for rx, unit in ((_DELAY_Y, YEAR_DAYS), (_DELAY_M, 30), (_DELAY_D, 1)):
        m = rx.search(raw)
        if m:
            g = [x for x in m.groups() if x is not None]
            t["delay_days"] = _mid(g[0], g[1] if len(g) > 1 else None) * unit
            t["delay_years"] = round(t["delay_days"] / YEAR_DAYS, 2)
            break

    # mode, in precedence order
    m = _CYCLE.search(raw)
    if m:
        t["cycle_years"] = int(m.group(1)); t["cycle_days"] = int(m.group(1)) * YEAR_DAYS
        stamp("cycle", m.group(0))
    elif (m := _USES.search(raw)):
        t["uses"] = int(next(g for g in m.groups() if g)); stamp("uses", m.group(0))
    elif t["days"] is not None:
        stamp("duration", _DURATION.search(raw).group(0))
    elif t["delay_days"] is not None:
        stamp("delayed", "delayed arrival")
    elif (m := _ACTIVE.search(raw)):
        # ranks below duration/delayed: "while on the council" is usually a sub-clause,
        # not the reward's dominant temporal shape
        stamp("while_active", m.group(0))
    elif (m := _PERM.search(raw)):
        stamp("permanent", m.group(0))

    # a relic is kept permanently; its triumph is what sits on a cooldown
    if relic:
        if t["mode"] == "instant":
            t["mode"] = "permanent"; t["derived_from"] = "relic_catalogue"; t["match"] = "relic is kept"
        cd = relic.get("triumph_cooldown_days")
        if relic.get("activatable") and cd:
            t["activation"] = {"cooldown_days": cd,
                               "cooldown_years": round(cd / YEAR_DAYS, 2),
                               "cost": relic.get("triumph_cost") or []}
            if t["derived_from"] == "default":
                t["derived_from"] = "relic_catalogue"
    return t

ASSUMPTIONS = [
 "Reward timing is derived from the wiki's own wording, not the game files. `timing.match` "
 "records the substring each mode came from so any row can be checked by hand.",
 "A Stellaris year is treated as 360 days. The relic catalogue's cooldowns (900/1800/3600) "
 "divide exactly by 360 and not by 365, which is the evidence for it.",
 "`timing.mode` is the dominant shape only. `days`, `delay_days`, `uses` and `activation` are "
 "independent — a reward that arrives in 5 years and then lasts 10 carries both.",
 "`mode: instant` is the default, not a finding. It means no time dimension was stated, which "
 "for most rewards means permanent-on-acquisition; it is not evidence of a one-off effect.",
 "Stated ranges ('returns in 30-40 days') are reduced to their midpoint. The range survives "
 "in `raw`.",
 "Relic timing comes from the relic catalogue, which was captured from a wiki page tagged game "
 "version 4.5, while the rift and site data is documented against 3.14. Cooldowns and triumph "
 "costs may not match the version the rest of the dataset describes.",
]

if __name__ == "__main__":
    CASES = [
     ("Recurring every 10 years, choose one: 16 extradimensional cruisers", "cycle", 3600),
     ("Incubate Wind Creatures (usable 3 times, +5 max generator districts each)", "uses", None),
     ("Astral Cloaking (+1 Cloaking Strength while active)", "while_active", None),
     ("A Star is Born: +10% Physics research for 10 years", "duration", None),
     ("Scientist disappears and returns in 5 years with Rift Warped", "delayed", None),
     ("Home Cooking permanent empire modifier (+10% Food from jobs)", "permanent", None),
     ("Celestial Tear", "instant", None),
     ("The scientist goes missing for 30-40 days", "duration", None),
    ]
    ok = True
    for raw, want, cyc in CASES:
        got = derive(raw)
        bad = got["mode"] != want or (cyc and got["cycle_days"] != cyc)
        ok &= not bad
        print(f"  {'ok  ' if not bad else 'FAIL'} {want:13} <- {raw[:58]}")
        if bad: print(f"        got {got['mode']}, cycle={got['cycle_days']}")
    # delayed + duration co-existing
    d = derive("Follow-up: after 1 year the scientist returns with Paranoia, a year later Obelisk's Curse for 6 years")
    print(f"  {'ok  ' if d['delay_days'] and d['days'] else 'FAIL'} delay+duration coexist: "
          f"delay={d['delay_days']}d days={d['days']}d mode={d['mode']}")
    r = derive("Eternal Throne relic", relic={"activatable":True,"triumph_cooldown_days":3600,
                                              "triumph_cost":[{"amount":3000,"resource":"unity"}]})
    print(f"  {'ok  ' if r['mode']=='permanent' and r['activation']['cooldown_years']==10 else 'FAIL'} "
          f"relic: mode={r['mode']} cooldown={r['activation']['cooldown_years']}y")
    print("\n" + ("SELF-TEST PASSED" if ok else "SELF-TEST FAILED"))
