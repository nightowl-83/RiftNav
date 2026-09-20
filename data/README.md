# Stellaris discovery datasets

Machine-readable companions to the reference documents one folder up.
Everything here is generated, not hand-edited.

## Which file do I load?

| If your PoC… | Load |
|---|---|
| does astral rifts (current) | **`astral_rifts.v3.json`** |
| renders rifts and archaeological sites from one component | `stellaris_discovery.v2.1.json` |
| only does archaeological sites | `archaeological_sites.v2.1.json` |

**v3 is rifts only, and it is the current shape for rifts.** It supersedes the rift half of
v2.1: rewards are parsed deterministically instead of hand-curated, the 4 astral rift
situations are included, and bulk resource payouts are split out of the reward index.
Archaeological sites have not been migrated to v3 yet — they are still v2.1.

The v2.1 files are untouched so existing wiring keeps working. `astral_rifts.json` (v2.0) and
`archaeological_sites.json` (v1.0) are older still; don't build on them.

## v3 shape (rifts)

```
{ dataset, kind, schema, version, generated, source, wiki_version, coverage,
  reward_groups[{key,label,blurb,types[]}],   // the 6 chip groups
  payout_types[], reward_codes[], groups[], mechanics[],
  entities[ { uid, id, kind, name, group, group_label, dlc, requirements,
              restrictions, notes,
              chapters[ { id, index, title, rewards[], choices[],
                          reward_ids[], payout_ids[] } ] } ],
  rewards[ { rid, group, group_label, type, name, entity, entity_uid,
             chapter, chapter_index, polarity, source, conditional, gate, raw } ],
  payouts[ { pid, type, entity, entity_uid, chapter, chapter_index,
             polarity, source, conditional, gate, raw } ],
  assumptions[] }
```

**Two levels on purpose.** `group` is what goes on a chip row (6 of them). `type` is what
picks an icon or a detail label (18 of them). Render whichever depth the view needs — you
never have to re-cut the taxonomy.

## Six things that will bite you

1. **`rewards[]` and `payouts[]` are separate arrays.** 362 of the 519 typed objects are bulk
   resource payouts. They are deliberately out of the reward index — that is what stopped the
   finder being 70% astral threads. Merge them only if you actually want that.
2. **Sort chapters on `index`, never `id`.** Rift chapter ids are not numbers: `4-A`, `3/4/5`,
   `2b`, `4-A-fail`, and named nodes like `fungal_bloom`.
3. **Choice-line rewards inherit the chapter of the *choice*, not the payout.** Ruined Planet's
   chapter-4/5 offers resolve at chapter 7. `source: "choice"` marks these — 24 rows.
4. **`type: "recurring"` fires more than once.** One row: The Seal's every-10-years choice.
   Any "total value of this rift" calculation is wrong for The Seal until you special-case it.
5. **`type: "undocumented"` is real, not a bug.** One row, where the wiki declines to name a
   reward. Surface it as unknown rather than dropping it.
6. **Situations are entities with `kind: "astral_rift_situation"`.** Filter on `kind` if you
   want rifts only; their uids are prefixed `situation:`.

## Reward values are not numbers

Payouts are multipliers of your *current* empire output with a min–max clamp, expanded in
`reward_codes`. `rsh3` is "24x of the named research (500~1,000,000)", not a fixed figure.
A UI showing a payout as one number is wrong at every stage but one.

## Regenerating

`tools/build_v3.py` reads v2.1 plus `tools/situations.py` and rebuilds v3. `tools/parse_rewards.py`
is the classifier — anything matching no rule is reported as unclassified, currently zero.
`tools/validate_v3.py` runs 17 checks. Never hand-edit a generated file.

## Provenance

Wiki-sourced (`stellaris.paradoxwikis.com`), documented against game version **3.14**. Rift
data captured 2026-08-30, situations added 2026-09-14, reward codes verified against
`Template:Reward`. Read the `assumptions` array before shipping — reward *magnitudes* have
never been re-verified against a live patch, only presence and typing.
