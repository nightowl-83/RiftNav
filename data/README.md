# Stellaris discovery datasets

Generated, never hand-edited. Both halves are now on the same shape.

## Which file do I load?

| If your UI… | Load |
|---|---|
| renders rifts and sites together | **`stellaris_discovery.v3.json`** (768 KB) |
| only does astral rifts | `astral_rifts.v3.json` (384 KB) |
| only does archaeological sites | `archaeological_sites.v3.json` (448 KB) |
| needs relic effects on their own | `relics.v3.json` (also in the merged file as `relics[]`) |
| is the Rift Finder handoff | nothing: it reads `design_handoff_rift_finder/rift-data.js` / `dig-data.js`, generated from these files (see below) |

`*.v2.1.json` are the **build inputs** for v3 — not stale outputs. Don't load them, don't
delete them. `_superseded/` holds genuinely retired files, including the old merged
`stellaris_discovery.v2.1.json` which carried pre-v3 rift data behind an innocent filename.

## Shape

```
{ dataset, kind, schema, version, generated, wiki_version, source, coverage,
  reward_groups[{key,label,blurb,types[]}],  payout_types[],
  reward_codes[], groups[], mechanics[],
  entities[ { uid, id, kind, name, group, group_label, dlc, requirements,
              restrictions, notes, unlocks[],
              chapters[ { id, index, title, rewards[], choices[],
                          reward_ids[], payout_ids[], chain_ids[] } ] } ],
  rewards[ { rid, group, group_label, type, name, entity, entity_uid, kind,
             chapter, chapter_index, polarity, source, conditional, gate, raw } ],
  payouts[ { pid, type, … same fields … } ],
  chains[  { cid, targets[], target_kind, … same fields … } ],
  ignored_lines[ { entity, chapter, type, raw } ],
  corrections[ { entity_uid, op, removed_lines[], source, revid, evidence_sha256, why } ],  # sites
  relics[ … ],                                                     # merged file only
  assumptions[] }
```

Every row in `rewards[]`, `payouts[]` and `chains[]` has **`raw`** (the verbatim source line) and
**`text`** (player wording: reward codes expanded to multiplier + min–max clamp, `a~b` written
`a–b`). Relic rewards also carry **`relic_id`**, or `relic_link_exception` with the reason.

### `relics.v3.json`

```
{ dataset, kind: "relic", schema, version, generated, wiki_version, source, captured,
  captured_with, capture_sha256, coverage, categories[], dlc_names{},
  relics[ { id, uid, name, category, category_key, subsection, stage,
            passive[], triumph[], triumph_cost[{resource, amount}], triumph_cooldown_days,
            activatable, source, source_kind, score, dlc[], dlc_codes[],
            raw{passive[], triumph[]}, rewarded_by[rid] } ],
  link_exceptions[ { entity, entity_uid, raw, why } ], assumptions[] }
```

68 relics from the Relics wiki page, one per relic; upgradeable relics (The Key, Celestial
Chart) have one entry per stage. `rewarded_by` lists the merged-file reward ids that grant it.
The page is tagged for game version **4.5**, newer than the 3.14 the rest of the data documents.

Four arrays, one purpose each:

- **`rewards[]`** — the ~341 things a player actually chases. Two levels: `group` (6, for chip
  rows) and `type` (20, for icons and detail labels). Render whichever depth a view needs.
- **`payouts[]`** — 815 bulk currency lines (astral threads, minor artifacts, research,
  resources). Deliberately out of the reward index; this is what stopped the finder being
  mostly astral threads.
- **`chains[]`** — 30 graph edges: which dig reveals which next dig. Not rewards to your
  empire, so not in `rewards[]`. `entities[].unlocks[]` is the same information denormalised.
- **`ignored_lines[]`** — lines the parser deliberately drops (branch flags, "narrative only").
  Recorded rather than discarded so "nothing was lost" is checkable.

## Seven things that will bite you

1. **Sort chapters on `index`, never `id`.** Rift ids are not numbers: `4-A`, `3/4/5`, `2b`,
   `fungal_bloom`. Site ids are ordinals *as strings*.
2. **Join on `uid`, not `id` or `name`.** Ids collide across kinds. Prefixes: `rift:`,
   `situation:`, `site:`.
3. **Two bulk currencies.** Rifts pay astral threads, sites pay minor artifacts. `payout_types`
   is `[threads, artifacts, research, resource]` — don't assume one.
4. **Choice-line rewards carry the chapter of the *choice*, not the payout.** Ruined Planet's
   ch4/ch5 offers resolve at ch7. 24 rows, flagged `source: "choice"`.
5. **`type: "recurring"` fires repeatedly.** One row (The Seal, every 10 years). Any totals
   view is wrong for it. See `docs/DECISIONS.md`.
6. **`type: "undocumented"` is real.** 3 rows where the wiki declines to name a reward.
   Show as unknown; don't drop.
7. **Sites have no choice tree.** `choices[]` is always empty and chapter `title` always null
   for `archaeological_site`. Source limitation, not a conversion gap — don't build UI that
   assumes both kinds branch. Some site *reward lines* do offer a pick ("Choice: … / OR …"); the UI
   file groups those into `choices` option groups (see below). That is a different thing from a
   rift's event choices.

## Reward values are not numbers

Payouts are multipliers of *current* empire output with a min–max clamp, expanded in
`reward_codes`. `rsh3` is "24x of the named research (500~1,000,000)". A UI showing one
figure is wrong at every game stage but one.

## Regenerating

```
python3 data/tools/build_all_v3.py     # all four JSON files, then the two UI .js files
python3 data/tools/validate_all_v3.py  # 85 checks
```

Inputs, in the order the build uses them:

| Input | What it is |
|---|---|
| `astral_rifts.v2.1.json`, `archaeological_sites.v2.1.json` | the captured rift and site data |
| `tools/situations.py` | the four rift situations |
| `tools/corrections.py` | sourced fixes to the v2.1 inputs, each citing a wiki revision and an evidence hash. Never edit the JSON instead |
| `tools/capture/relics.wiki.json` | the relic capture. Re-capture with `tools/capture/capture_relics.js` in a browser tab on the wiki (the wiki blocks scripted API clients); the build refuses a file that doesn't match its own hash |

The tools find the repo from their own location; set `STELLARIS_ROOT` to point them elsewhere.

## The UI data files

`design_handoff_rift_finder/rift-data.js` (`window.RIFT_DATA`) and `dig-data.js`
(`window.DIG_DATA`) are **generated** by `tools/build_ui_data.py`. Don't edit them. Every field
the UI already read is still there with the same name; everything new is additive:

- `counts` (rifts, situations, chapters, rewards; sites, phases, …) and `meta` (sources, versions,
  corrections). The design's header stats read `counts`.
- Chapters keep `rewards[]` as display strings (now plain wording), plus `raw[]` (verbatim),
  `guaranteed[]` (indexes of lines that always pay out) and option groups:

```
choices (dig chapters) / rewardChoices (rift chapters, where choices[] is already the event's choices):
  [ { kind: "choice" | "random" | "either",
      options: [ { label, payouts[], raw, line } ] } ]
```

`choice` means the player picks, `random` means the game picks ("Random: …" / "OR …"), and
`either` means the wiki doesn't say. Don't draw a `random` group as a pick. Every group has at
least two options, and every line is either guaranteed or in exactly one group.

- Reward rows add `rid`, `type`, `rewardGroup`, `source`, `polarity`, `conditional`, `gate`,
  `text`, `raw`, and for relics `relicId` + `relic` (passive, triumph, cost, cooldown, DLC).
- Reward rows also carry **`short`** (a heading-length name, 1–60 characters: the part before the first
  colon when there is one, otherwise the first clause) and **`effect`** (the rest, or the full text when
  it adds anything). Option-group options carry `short` + `shortDetail` the same way. The validator
  fails any reward or option without a short name of 60 characters or less.
- Rift reward `path` is the curated v2.1 path when it still resolves, else the shortest route
  through the chapter graph; `pathSource` says which (`curated`, `computed`, `failure` via an
  "on failure →" edge, `direct` for situation stages).
- `dig-data.js` `mechanics[]` ends with the glossary line explaining that "6x" is six months of
  current output clamped to the min–max shown.

`parse_rewards.py` is the classifier. Anything matching no rule is reported as
`unclassified` — currently **zero across both datasets**. Keep it there: that is what makes
coverage provable instead of asserted. Add new rules to the **priority block at the top**, not
the bottom — a substring elsewhere in a line will otherwise win (this is how "100 Astral
Threads" inside a *cost* clause once got typed as a payout).

## Provenance

Wiki-sourced, documented against game version **3.14**. Rifts captured 2026-08-30, rift
situations 2026-09-14, sites migrated to v3 2026-09-26, reward codes verified against
`Template:Reward` (`inf4` added from it on 2026-09-26). Relics captured 2026-09-26 from the
Relics page, revision 119679, tagged game version **4.5**. Reward **magnitudes** have never been checked against a live patch — only
presence and typing.
