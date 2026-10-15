# Session — reward timing, and the Cowork commit constraint

**Date:** 2026-10-15
**Surface:** Cowork (cloud session linked to mikes-macbook-pro-local)
**Status at close:** timing settled; see open items for one judgment call left to Mike

## What we set out to do

Pick up the two items left open on 26 Sep: model reward timing (now that relics had landed),
then document why committing from Cowork fails.

## What actually changed

**Timing is modelled end to end.** New `data/tools/timing.py` derives a `timing` object for
every reward. 54 of 343 rewards now carry a real temporal shape, in six: duration (15),
delayed (8), permanent (26), uses (3), cycle (1), while_active (1) — plus 22 relic activation
cooldowns. 289 are `instant`, which is the default, not a finding.

- `mode` is the dominant shape for a chip; `days` / `delay_days` / `uses` / `cycle_days` /
  `activation` are independently nullable, so a reward that arrives in 5 years *and then* lasts
  10 carries both.
- Canonical unit is days. **A Stellaris year is 360 days** — the relic cooldowns (900/1800/3600)
  divide exactly by 360 and give fractions under 365. `years` is derived, so it cannot drift.
- `activation` is relic-only (`cooldown_days`, `cooldown_years`, `cost[]`). A relic is kept
  permanently while its triumph sits on a cooldown; one `mode` field could not say both.
- `derived_from` and `match` record where each mode came from, so any row is checkable by hand.
- 18 new validator checks (107 passing overall), including regression guards on The Seal and on
  the `recurring`-type/`timing.mode` pair never disagreeing.
- The UI bundle carries a **compact** projection — nulls dropped, nothing emitted for a plain
  instant reward, so **missing `timing` means instant**. Total bundle growth: ~4 KB.
- `GENERATED` was a hardcoded constant still reading 2026-09-27; bumped to 2026-10-15. Worth
  knowing it does not auto-update.
- `CLAUDE.md` gained a section on the Cowork commit constraint; `data/README.md` gained a timing
  section; `docs/DECISIONS.md` gained the timing decision.

## Decisions made

One, in `docs/DECISIONS.md`: timing is a `timing` object, not a reward type. It supersedes the
26 Sep "capture relic effects first" entry, which had sequenced this correctly.

## What went wrong, and what it cost

**I truncated `data/tools/build_ui_data.py` to zero bytes.** A patch script of mine opened the
file for writing before reading it. The file was committed, so `git show HEAD:… > …` restored all
359 lines with a zero diff and nothing was lost — but only because it was committed. This is the
"commit at the end of every sitting" rule paying for itself. Subsequent edits read fully into
memory first and assert on size before writing.

Also found and fixed before shipping: `while_active` was outranking `duration`/`delayed` in mode
precedence, so Volcanic Plane's delayed follow-up was mis-typed on the strength of a
"while on the council" sub-clause.

## What's still open

**1. The `recurring` reward type is now redundant — Mike's call.** `timing.mode: "cycle"` says
the same thing. I left the type in place because the UI renders it (`TYPE_SHORT`, `yieldKey` in
`Rift Finder Holo.dc.html`), and retiring it means a UI change I was not going to make
unilaterally against live work. The validator asserts the two cannot disagree, so there is no
drift risk while it sits there.

**2. Reward `name` quality.** Several chips read as sentence fragments rather than names —
"Choice", "If you took option 1", "OR 100 Influence and fight two mega-warforms". Pre-existing
in `clean_name`, unrelated to timing, but visible now that timing put more detail on the card.
`data/overrides/` exists for exactly this.

**3. The relic version mismatch stands.** `relics.v3.json` was captured from a wiki page tagged
game version **4.5**; rifts and sites are documented against **3.14**. Timing inherits that for
all 22 activation cooldowns. Already recorded in the relic dataset's own assumptions, now also in
`timing.ASSUMPTIONS`.

**4. Unchanged from before:** reward magnitudes never verified against a live patch; choice-line
rewards carry the choice's chapter not the payout's; `resources/images/` still empty pending the
licensing call; `reference/_graphics/` film stills must come out before this repo could go public.

**5. Stale git litter from the 26 Sep session** (`.git/_stale/`, `.git/objects/maintenance.lock`,
9 `tmp_obj_*`). Harmless, but the cleanup command is in `CLAUDE.md`.

## Next three things

1. Decide on the `recurring` type (open item 1) — a small UI change if retiring it.
2. Reward name quality pass via `data/overrides/`.
3. Resume Holo Deck direction — `docs/sessions/2026-09-06-holo-deck.md` §7 first.

## Links

- `data/tools/timing.py` (self-tests: `python3 data/tools/timing.py`)
- Sources: `Relics` (game v4.5) and `Astral_rift` / `Archaeological_site` (3.14) on
  stellaris.paradoxwikis.com
