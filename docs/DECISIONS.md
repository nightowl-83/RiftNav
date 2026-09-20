# Decision log

Decisions that still bind, newest first. Each entry: what was decided, when, why, and what
would overturn it. If a decision is reversed, don't delete it — add a new entry that
supersedes it and say so.

---

## 2026-09-20 — This repository is the source of truth

**Decided:** The Git repository, hosted on GitHub (private), is authoritative for this
project. Any machine is a working copy.

**Why:** Work needs to move between machines. The previous arrangement made one laptop
authoritative with a Google Drive mirror, which meant the project only existed where that
laptop was. Git also gives real history — the `(pre-audit backup 2026-08-30).docx` file in
`reference/_superseded/` is exactly the kind of manual versioning that stops being necessary.

**Supersedes:** The 2026-08-22 decision that `~/Desktop/Projects/Stellaris` on
mikes-macbook-pro was the source of truth, with Drive as mirror. That setup and its daily
parity audit are retired; the notes are preserved in `docs/archive/`.

**What would overturn it:** Assets growing past what Git handles comfortably (large video,
many high-res PNGs). Current repo is ~15MB. Past roughly 1GB, or if `Holo/refs/` starts
churning binary stills every session, move heavy assets out and consider Git LFS.

---

## 2026-09-19 — Rewards are parsed deterministically, not hand-curated (v3)

**Decided:** `astral_rifts.v3.json` replaces the hand-curated rift reward index. Rewards
carry two levels — `group` (6, for chip rows) and `type` (18, for icons and detail labels).

**Why:** Two classes of reward were simply missing from v2.1. (1) 24 named rewards lived
inside chapter *choice* lines as `also grants:` / `cost:` / `(species gains X)` payloads and
were never indexed. (2) The `Astral_rift_situations` wiki page had never been read at all,
contributing 13 more. Hand-curation is how both happened.

**Source:** `docs/audits/2026-09-19-rift-rewards-v3.md`; wiki data from
stellaris.paradoxwikis.com, game version 3.14.

**Still open:** Archaeological sites have not been migrated to v3 — they remain on v2.1.

---

## 2026-09-19 — Recurring rewards are typed but not modelled

**Decided:** The Seal's every-10-years choice is typed `recurring` so it can be found, but
the schema has no way to express recurrence.

**Consequence to respect:** Any "total value of this rift" calculation is **wrong for The
Seal** until recurrence is modelled. Don't ship a totals view without special-casing it.

---

## 2026-09-07 — The background is a particle system, not video

**Decided:** Build the Holo Deck background as a canvas/WebGL particle simulation. The
video-based approach — a state graph of short generated clips with pixel-matched junction
frames — is the fallback, not the plan.

**Why:** With video, a transition can only begin at a loop boundary, so a click can sit for
up to 3 seconds with nothing happening. That was the worst problem in the video design. A
particle system morphs on the click frame. "Seamless loop" also stops being a problem, since
a continuous simulation has no loop to close.

**Artifact:** `Holo/Holo Deck Motion Spec — v1.3.html` is the superseded video spec, kept.

**Still open as of that session:** Mike's assessment of the latest prototype was "not really
what I am looking for." Direction is **not** settled. Read
`docs/sessions/2026-09-06-holo-deck.md` §7 before building.

---

## 2026-09-06 — "Events" are out of scope

**Decided:** The tool covers Astral Rifts and Archaeological Sites only. General events are
deferred.
