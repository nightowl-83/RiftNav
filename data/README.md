# Stellaris discovery datasets

Generated, never hand-edited. Both halves are now on the same shape.

## Which file do I load?

| If your UI… | Load |
|---|---|
| renders rifts and sites together | **`stellaris_discovery.v3.json`** (768 KB) |
| only does astral rifts | `astral_rifts.v3.json` (384 KB) |
| only does archaeological sites | `archaeological_sites.v3.json` (448 KB) |

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
  assumptions[] }
```

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
   assumes both kinds branch.

## Reward values are not numbers

Payouts are multipliers of *current* empire output with a min–max clamp, expanded in
`reward_codes`. `rsh3` is "24x of the named research (500~1,000,000)". A UI showing one
figure is wrong at every game stage but one.

## Regenerating

```
python3 data/tools/build_all_v3.py     # builds all three from v2.1 + situations.py
python3 data/tools/validate_all_v3.py  # 50 checks
```

`parse_rewards.py` is the classifier. Anything matching no rule is reported as
`unclassified` — currently **zero across both datasets**. Keep it there: that is what makes
coverage provable instead of asserted. Add new rules to the **priority block at the top**, not
the bottom — a substring elsewhere in a line will otherwise win (this is how "100 Astral
Threads" inside a *cost* clause once got typed as a payout).

## Provenance

Wiki-sourced, documented against game version **3.14**. Rifts captured 2026-08-30, rift
situations 2026-09-14, sites migrated to v3 2026-09-26, reward codes verified against
`Template:Reward`. Reward **magnitudes** have never been checked against a live patch — only
presence and typing.
