# Stellaris — Source of Truth & Sync

**Established:** 2026-08-22
**Owner:** Mike (Product Design Lead)

## The rule

`/Users/callisto/Desktop/Projects/Stellaris` on **mikes-macbook-pro** is the
**source of truth** for this project.

If the local folder and the Drive folder disagree about a file that exists in
both, **local wins**. Drive is a mirror and a collaboration surface, not the
system of record.

## The paired locations

| Side | Location |
|---|---|
| Local (source of truth) | `/Users/callisto/Desktop/Projects/Stellaris` |
| Drive (mirror) | My Drive → **Stellaris Helper** — https://drive.google.com/drive/folders/1fasaDAjT6Yvqo58fdlUmVctGeLaT6cqi |

Drive folder is owned by `mcball83@gmail.com`.

## How parity is maintained

Two layers, deliberately. Neither one alone is sufficient.

**Layer 1 — Google Drive for desktop (the sync engine).**
A real file-sync daemon. It handles continuous propagation, renames, deletes,
partial writes, and conflict copies. This is what actually keeps the bytes in
step. Setup steps are in `SETUP-DRIVE-FOR-DESKTOP.md`.

**Layer 2 — the daily parity audit (scheduled Claude task, 8:00 AM CT).**
Software syncs; it doesn't tell you when something looks wrong. The daily task
compares both sides, exports Drive-native docs to a local snapshot, refreshes
`DRIVE_MANIFEST.md`, and reports drift — files present on one side only,
conflict copies, and anything modified on the Drive side (which, under the rule
above, is a signal that someone edited the mirror instead of the source).

## Google-native files (Docs / Sheets / Slides)

These have **no true local file form**. A `.gdoc` on disk is just a pointer.
So the convention here is:

1. Each native Drive file gets a **local snapshot** (`.docx` / `.xlsx`, or
   `.pdf` when a faithful Office export isn't available).
2. Every native file is listed in `DRIVE_MANIFEST.md` with its live URL.

**Snapshots are read-only in practice.** Editing a snapshot does *not* change
the live Doc. For native docs, Drive — not local — is the authoritative copy.
This is the one carve-out to the source-of-truth rule, and it is unavoidable.

## What lives where

- `_sync/` — this folder. Sync convention, manifest, audit log. Not project content.
- Everything else — project content, mirrored to Drive.
