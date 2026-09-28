# -*- coding: utf-8 -*-
"""Turn every rift reward/choice line into typed reward objects.

Rules are ordered and explicit. Anything that matches no rule lands in
'unclassified' and is REPORTED, never silently dropped — that is what makes
coverage provable instead of assumed.
"""
import json, os, re
from collections import Counter, defaultdict

from paths import DATA

RESOURCES = (r"astral threads|minerals?|energy|alloys?|food|exotic gas(?:es)?|rare crystals?|"
             r"dark matter|volatile motes?|living metal|influence|zro|consumer goods|nanites?")
RESEARCH  = r"physics|society|engineering|unity"

# (type, pattern, name-extractor group or None)
RULES = [
 # -- priority: explicit structural markers, so a substring elsewhere in the line cannot win
 ("recurring",   r"^recurring every|\brepeats every\b", None),
 # offering bonuses: "Black Curtain + astral threads: +25% …" names what was offered, not what you get
 ("modifier",    r"^(?:[\w' -]+ \+ |chapter \d+ )(?:astral threads|resources|alloys|energy|minerals)\s*:", None),
 # -- archaeology forms: reward CODES appear as prefixes (art1 / mat2 / rsh3 / uni1 / inf2)
 #    and the bulk currency is minor artifacts, not astral threads
 ("artifacts",   r"^art\d\b|\b\d+ minor artifacts\b|^minor artifacts\b", None),
 ("research",    r"^(?:rsh|res|uni)\d\b|^(?:mat|rsh|res)\d\s+(?:society|physics|engineering|unity)\b|"
                 r"^\d+x?\s+(?:society|physics|engineering)\s+research\b", None),
 ("resource",    r"^(?:mat|inf)\d\b|^\d+x?\s+living metal\b", None),
 ("cosmetic",    r"music track", None),
 # chain progression: a dig that reveals the next dig, or starts a named chain
 ("chain",       r"\breveals?\b.*\b(site|system)\b|contributes to revealing|special project.*\b(reveal|find)|starts the .* event chain|\bevent chain\b|unlocks Benign Cover-Up|enables the .* special project", None),
 ("routing",     r"^choice that sets a flag|^conditional on the chapter", None),
 ("undocumented",r"see wiki|mutually exclusive endgame options|the wiki does not name|unnamed reward|not documented", None),
 # relic by the word, never a specimen line and never the 'relic world' requirement
 ("relic",       r"^(?!.*\bspecimen\b)(?!.*relic world).*\brelic\b", None),
 ("specimen",    r"^specimen\b", None),
 # reward codes appearing mid-line: "OR rsh3 Society research", "66%: rsh4 Society research"
 ("research",    r"\b(?:rsh|res|uni)\d\b|\b\d+x\s+(?:society|physics|engineering|unity)\b|\bplus uni\d\b", None),
 ("resource",    r"\b(?:mat|inf)\d\b|\bspend \d+ energy\b|^or \d[\d,]*\s+(?:alloys|influence|minerals)|^\d+(?:-\d+)?\s+zro\b|^\d[\d,]*\s+(?:influence|alloys|minerals|energy)\b", None),
 ("modifier",    r"^removes the .* penalty|^otherwise you get|^replaces .* with", None),
 ("deposit",     r"on the rift\b|deposit to the planet|\+\d+ research deposit", None),
 ("planet",      r"gaia world|pre-ftl planet|size \d+ .*world|new colony appears|ship debris blocker|creates? a habitat|planetary feature|mutation vats|sentinels metal|terraform|relic world|planet modifier", None),
 ("modifier",    r"\bmodifier\b|^\+\d+% ", None),
 ("routing",  r"^sets you on|^sets up the|^adds an? \w+ payout to|^goes to \d|^forces outcome", None),
 ("threads",  r"^(small|medium|large) astral threads", None),
 ("threads",  r"astral threads scaled to|^no astral threads$|\bastral threads\b", None),
 ("specimen", r"^(?P<n>.+?)\s+specimen\b", "n"),

 ("penalty",  r"scientist (and science ship )?(is |are )?(dies|destroyed|killed|lost|disappears)|"
              r"scientist ages|kills the scientist|loses? ~?\d+% of|hostile fleet|goes nova|"
              r"spawns a hostile|demands 1 pop|sacrifices 1 pop|maimed|partially digested|traumatized|"
              r"obelisk's curse|-\d+% (happiness|resources)", None),
 ("followup", r"^follow-up:", None),
 ("deposit",  r"on the rift\b", None),
 ("tech",     r"progress toward|progress on|\btechnolog(y|ies)\b|\btech\b|next-tier|wormhole stabilization|gene tailoring|"
              r"basic cloaking fields", None),
 ("decision", r"\bdecisions?\b", None),
 ("edict",    r"astral cloaking|automated disinfection|spontaneous crystallization", None),
 ("unit",     r"\barmies\b|warpling|flamestorm|\bfleet\b(?! of 10)", None),
 ("species",  r"\bpops?\b|\bDNA\b|adaptive evolution|species gains|new (random )?species", None),
 ("leader",   r"level \d+ (commander|scientist|official)|new scientist|paragon|oakenstalk|plantoid leader|gains [\d,]+ experience|[\d,]+ experience|unique leader|\bkeides\b|the oracle|skrand sharpbeak|"
              r"becomes \d+ years younger|level 5 scholar|aged official|scholar\b|"
              r"returns? (in|after) \d+ years|recruit", None),
 ("trait",    r"scientist gains|gain psionic|rift warped|spark of genius|meticulous|roamer|psychic|planar theorist|riftwalker|"
              r"foreign consciousness|resilient|black light blinded|sanitary drone|latent psionic|"
              r"increased lifespan|society focus|expertise:", None),
 ("modifier", r"^(genesis insight|fractured ambassadors|colonization drones|procedural space|formula pink|rift fluid samples|extra dimensional spores|lonely planet|vortex fuel|restoring the balance|zroni insight|astral shield experimentation|grunur weapons interface|a star is born|revolutionary medi-gel|reconverted leader|harmonious crew|cultural maturity|cultural reconstruction|home cooking|harsh truth|mysterious universe|unified thought|frozen submariners|in memory|a life worthwhile|mycelial network|bane of the prophetess|forced mindfulness|anthem of aurora|local hive|sage rage|eldritch knowledge|killer microorganism|modern trench war|the memorex|spurred by the past|full circle|goes around|improved decryption|research allocation|genius caeli|studying polarian seeds|shallarian terraforming|rudari death laser|c\\.a\\.r\\.e|peace in this dimension|temporal distortions|dreadnought's reactor)\b", None),
 ("contact",  r"communications with|contact with|mirror empire|formless contact|opinion|subject type|\bvassal\b|designates the .*fallen empire|federation|cohesion", None),
 ("situation",r"\bsituation\b|the seal\b|spawns the crystal rift|^spawns ", None),
 ("system",   r"^azilash|strange wormhole", None),
 ("relic",    r"^(advisor core|celestial tear|daedalus seal|ever spinning top|infinity root|"
              r"plasmic core|the continuum|time crystal|eternal throne)", None),
 ("research", rf"^\d+x ({RESEARCH})\b|^({RESEARCH}) research\b|^(moderate|large|small) ({RESEARCH})|"
              rf"^\d+x ({RESEARCH}) (research|output)|^({RESEARCH}) output", None),
 ("resource", rf"^\d+x ({RESOURCES})|^\d+ ({RESOURCES})|^({RESOURCES})\b|^\+?\d+ ({RESOURCES})", None),
 ("modifier", r"^[A-Z][\w' ]+:\s|\+\d+%|-\d+%|\+\d+ |modifier|for \d+ years|"
              r"cloaking strength|\+0\.5 basic", None),
 ("resource", r"^-\d+\s|^-?\d+,?\d*\s*(food|minerals|energy|alloys|exotic gases|rare crystals|astral threads)\b", None),
 ("research", r"^(research and unity|unity|research)$", None),
 ("tech",     r"as a research option|^one of [A-Z]", None),
 ("planet",   r"appears in the system|alien site level \d|into a habitable planet", None),
 ("penalty",  r"goes missing for", None),
 ("decision", r"option to upgrade to", None),
 ("narrative",r"^(—|ends the rift\.?|narrative only|nothing)$|^or leave them undisturbed$|narrative only", None),
]
COMPILED=[(t,re.compile(p,re.I),g) for t,p,g in RULES]

GATE = re.compile(r"\[(?P<g>[^\]]+)\]|\bif (?P<g2>Evolutionary Predators|Gestalt[^,.;]*|"
                  r"the leader is Psychic|Latent Psionic[^,.;]*|Robotic[^,.;]*)", re.I)
COND = re.compile(r"\bif\b|\bunless\b|\botherwise\b|\bonly\b|\bwhen\b|\[|chance", re.I)

def classify(line):
    s=line.strip()
    if not s: return None
    for t,rx,g in COMPILED:
        m=rx.search(s)
        if m:
            name=None
            if g and m.groupdict().get(g): name=m.group(g).strip()
            return {"type":t,"name":name,"raw":s}
    return {"type":"unclassified","name":None,"raw":s}

SPLIT_ALSO = re.compile(r"\balso grants:\s*", re.I)
SPLIT_COST = re.compile(r"\bcost:\s*", re.I)
PAREN_GAIN = re.compile(r"\((species gains [^)]+|grants [^)]+|adds [^)]+|sets [^)]+)\)", re.I)

def from_choice(text):
    """Pull reward payloads out of a choice line: 'also grants:', 'cost:', '(species gains X)'."""
    out=[]
    for chunk in SPLIT_ALSO.split(text)[1:]:
        chunk=SPLIT_COST.split(chunk)[0]
        for part in re.split(r";\s*", chunk):
            part=re.sub(r"\s*\[.*?\]\s*$","",part).strip(" .")
            if part: out.append(("grant", part))
    for chunk in SPLIT_COST.split(text)[1:]:
        part=re.split(r"\s*\[|\s*\(", chunk)[0].strip(" .")
        if part: out.append(("cost", part))
    for m in PAREN_GAIN.finditer(text):
        out.append(("grant", m.group(1).strip()))
    return out

def main():
    d=json.load(open(f"{DATA}/astral_rifts.v2.1.json"))
    rows=[]; unclass=[]
    for e in d["entities"]:
        for c in e["chapters"]:
            for r in c["rewards"]:
                o=classify(r)
                if not o: continue
                o.update(entity=e["name"], uid=e["uid"], chapter=c["id"],
                         source="chapter", polarity="cost" if o["type"]=="penalty" else "grant")
                rows.append(o)
                if o["type"]=="unclassified": unclass.append((e["name"],c["id"],"reward",r))
            for ch in c["choices"]:
                for pol, payload in from_choice(ch):
                    o=classify(payload)
                    if not o: continue
                    o.update(entity=e["name"], uid=e["uid"], chapter=c["id"],
                             source="choice", polarity=pol)
                    rows.append(o)
                    if o["type"]=="unclassified": unclass.append((e["name"],c["id"],"choice",payload))
    for r in rows:
        g=GATE.search(r["raw"]); r["gate"]=(g.group("g") or g.group("g2")) if g else None
        r["conditional"]=bool(COND.search(r["raw"]))
    json.dump(rows, open("/tmp/rift_rewards_typed.json","w"), indent=1, ensure_ascii=False)

    print(f"typed reward objects: {len(rows)}   (from 437 reward lines + payloads inside 439 choice lines)")
    print(f"  from chapter reward cells : {sum(1 for r in rows if r['source']=='chapter')}")
    print(f"  from inside choice lines  : {sum(1 for r in rows if r['source']=='choice')}  <- the old finder indexed almost none of these")
    print(f"\nunclassified: {len(unclass)}")
    for x in unclass[:20]: print("   ", x[0], x[1], "|", x[3][:95])
    print("\n== type distribution ==")
    for t,n in Counter(r["type"] for r in rows).most_common(): print(f"  {n:4}  {t}")
    print(f"\nconditional (DLC / ethic / roll gated): {sum(1 for r in rows if r['conditional'])}")
    print("gates seen:", dict(Counter(r["gate"] for r in rows if r["gate"]).most_common(8)))

if __name__ == "__main__":
    main()
