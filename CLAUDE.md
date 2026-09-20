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
  `data/tools/build_v3.py` and validate with `data/tools/validate_v3.py` (17 checks).
- **`astral_rifts.v3.json` is current for rifts.** Archaeological sites are still on
  `archaeological_sites.v2.1.json` — the v3 migration hasn't happened.
- **Sort chapters on `index`, never `id`.** Rift chapter ids are not numeric (`4-A`, `3/4/5`,
  `2b`, `fungal_bloom`).
- **`rewards[]` and `payouts[]` are separate on purpose.** Don't merge them without a reason —
  362 of 519 typed objects are bulk resource payouts, and merging is what made the finder 70%
  astral threads.
- **Reward values are not numbers.** They are multipliers of current empire output with a
  min–max clamp. A UI that shows one figure is wrong.

`data/README.md` has the full schema and the six gotchas. Read it before any data work.

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

## Session protocol — important

Claude Code conversation history is **local to one machine and is not synced anywhere**. The
only thing that survives a move between machines is what gets committed. So:

**At the start of a session:** `git pull`, then read `docs/DECISIONS.md` and the newest file
in `docs/sessions/`.

**At the end of a session** (or when Mike says "close out"):
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
