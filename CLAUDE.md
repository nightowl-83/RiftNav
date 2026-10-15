# Stellaris Helper — project context

Read this first. It is loaded automatically at the start of every Claude Code session in
this repo, on any machine.

## What this project is

A companion tool for Stellaris players covering **Astral Rifts** and **Archaeological
Sites** — what the events are, what they require, and what they pay out. Two halves:

1. **The data** (`data/`) — wiki-sourced, parsed deterministically, schema-versioned.
2. **The UI** ("Rift Nav") — lives in **Claude Design**, not in this repo. See `docs/ARTIFACTS.md`.

Mike is a Product Design Lead. He works in HTML/CSS comfortably; explain anything involving
databases, installation, or backend development in plain, step-ordered terms.

## The repo is the source of truth

As of 2026-09-20 this repository — not any local folder — is authoritative. Work is expected
to move between machines. Assume nothing about local state that isn't committed.

## Hard rules

- **Never hand-edit anything in `data/*.json`.** They are build outputs. Regenerate with
  `data/tools/build_all_v3.py` and validate with `data/tools/validate_all_v3.py`.
- **Both halves are on v3.** `astral_rifts.v3.json`, `archaeological_sites.v3.json`, and
  `stellaris_discovery.v3.json` (both kinds, load this one for a combined UI). The
  `*.v2.1.json` files are the **build inputs** — don't load them, don't delete them.
  `data/_superseded/` holds retired files; nothing there should be built on.
- **Sort chapters on `index`, never `id`.** Rift chapter ids are not numeric (`4-A`, `3/4/5`,
  `2b`, `fungal_bloom`).
- **`rewards[]`, `payouts[]` and `chains[]` are separate on purpose.** 815 of 1,186 typed
  objects are bulk currency; merging them is what made the finder mostly astral threads.
  `chains[]` is the site-unlock graph, not a reward.
- **Two bulk currencies.** Rifts pay astral threads, sites pay minor artifacts.
- **Reward values are not numbers.** They are multipliers of current empire output with a
  min–max clamp. A UI that shows one figure is wrong.

`data/README.md` has the full schema and the seven gotchas. Read it before any data work.

## The UI direction that holds

Build the background as a **canvas/WebGL particle system, not generated video.** With video,
a transition can only start at a loop boundary — up to 3 seconds of the user clicking and
nothing happening. A particle system morphs on the click frame, and "seamless loop" stops
being a problem because there is no loop.

`Holo/Holo Deck Motion Spec — v1.3.html` is the superseded video-based spec. It is kept as a
fallback, not as the plan.

Design vernacular already in the product — reuse it, don't invent parallel terms:
RIFT NAV · HOLO DECK · GUIDE ONLINE · SELECT RIFT · SCAN COMPLETE · SIG-#### · RETARGET ·
ABORT RIFT · EVENT LOG · CLASSIC/HOLO toggle.

## The data goes stale on its own — a weekly task watches for it

The datasets are copied from the community wiki. The game gets patched, the wiki lags the game,
and our copy lags the wiki. None of that announces itself.

**`data/sources.json`** pins the wiki pages we depend on and the revision each was last verified
against. A scheduled task, **"Stellaris source watch"** (Mondays), compares live revision ids
against those pins and scans recent Paradox patch notes for mentions of rifts, dig sites or
relics. It only reports — it never re-captures and never commits.

**Do not trust the pages' own `{{version}}` tags.** The Relics tag read `{{Version|4.5}}` when we
captured it on 2026-09-26 and reads `{{version|3.14}}` today, having moved *backwards*. Pinned
revision ids are the only reliable staleness signal, which is why the manifest exists.

When the watch flags a change:

1. Re-capture. For relics that means pasting `data/tools/capture/capture_relics.js` into a browser
   console on a wiki tab — the wiki blocks scripted clients, so this is a human step.
2. Run `python3 data/tools/diff_relic_capture.py`. It reads the baseline from git (so saving over
   the capture cannot destroy it) and diffs only the five fields the dataset consumes. It says
   whether any relic cooldown moved, which is the one thing that would invalidate `timing`.
3. Rebuild, validate, then update `verified_revid` and `status` in `data/sources.json`.

State as of 2026-10-15: `Relics` is **BEHIND** (captured at 119679, page now 120038).
`Astral_rift` and `Archaeological_site` are **BASELINE_ONLY** — watched from now on, but the
August captures were never revision-pinned, so August-to-now is unmeasured.

## Committing from Cowork needs one extra step

**A Cowork session cannot stage or commit until file deletion is granted for the folder.**

Why: `git add` writes `.git/index.lock` and then *renames* it over `.git/index`. A rename has to
unlink the destination, and the Cowork folder mount blocks deletes by default. So `git add`
silently stages nothing and leaves the lock behind, and the next git command trips over it.
Nothing is lost — the working tree is intact — but the close-out cannot finish.

The fix, in order:

1. Claude calls `device_request_delete_permission` for the repo folder. Mike approves the prompt.
2. Deletion then works for the rest of that session, and `git add` / `commit` / `push` behave normally.

The grant **expires with the session**, so it is needed again next time. If it is declined or
nobody is around to approve it, write every file as normal and leave the commit to Mike:

```bash
cd ~/Desktop/Projects/Stellaris && git add -A && git commit && git push
```

If a session already hit the blocker, stale locks may be left behind. Clear them on the Mac:

```bash
rm -rf .git/_stale .git/objects/maintenance.lock
find .git/objects -name 'tmp_obj_*' -delete
git gc --prune=now
```

**Claude Code on the Mac is not affected** — it writes to the filesystem directly. This is a
Cowork-only constraint, and it sits alongside the other one: `/pick-up` and `/close-out` are
Claude Code commands that do not exist in Cowork, where you say "pick up" / "close out" instead.

## Session protocol — important

Claude Code conversation history is **local to one machine and is not synced anywhere**. The
only thing that survives a move between machines is what gets committed. So:

**At the start of a session:** run `/pick-up` (or `git pull`, then read `docs/DECISIONS.md`
and the newest file in `docs/sessions/`).

**At the end of a session** — run `/close-out`, or do this when Mike says "close out":
1. Write `docs/sessions/YYYY-MM-DD-<topic>.md` — what was done, what was decided, what's open,
   what to do next. Write it for a reader with no memory of the conversation.
2. Add any binding decision to `docs/DECISIONS.md` with its date and reasoning.
3. Add any new Claude Design page, published artifact, or research output to `docs/ARTIFACTS.md`.
4. Commit and push.

A session that ends without this is a session that didn't happen, as far as the next machine
is concerned.

## Tone

Lead with a recommendation and the reasoning behind it, and name the source when citing a
number or a claim. Flag assumptions worth pressure-testing rather than presenting them as
settled.
