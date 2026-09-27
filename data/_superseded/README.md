# Superseded datasets

Kept for history only. **Do not build on anything in this folder.**

| File | Was | Why retired |
|---|---|---|
| `stellaris_discovery.v2.1.json` | merged rifts + sites | Held **pre-v3 rift data and no situations** — 4 entities and 25 reward rows behind `astral_rifts.v3.json`, with nothing in the filename to say so. A consumer loading it got silently stale rifts. Replaced by `stellaris_discovery.v3.json`. Retired 2026-09-26. |
| `astral_rifts.json` | v2.0 rifts | Hand-curated 16-category reward finder. Superseded by v3 (2026-09-19). |
| `archaeological_sites.json` | v1.0 sites | First authored shape, pre-normalisation. Superseded by v2.1 then v3. |

`astral_rifts.v2.1.json` and `archaeological_sites.v2.1.json` stay in `data/` — they are the
**build inputs** for v3, not stale outputs. Deleting them breaks `build_all_v3.py`.

| `stellaris-discovery-2.1.schema.json` | JSON Schema for the v2.1 shape | Described `reward_finder[]`, which v3 replaced with `rewards[]` / `payouts[]` / `chains[]`. A schema that no longer matches the data is worse than no schema. **No v3 schema has been written yet** — `data/README.md` documents the shape instead. Retired 2026-09-26. |
