# Session — move the project online

**Date:** 2026-09-20
**Surface:** Cowork (cloud session linked to mikes-macbook-pro-local)
**Status at close:** repo structured and committed locally; GitHub remote not yet connected

## What we set out to do

Make this project pickable-up from any machine, with current files and enough context to
resume mid-thought — including a running record of Claude sessions and research.

## What actually changed

- Repository initialised. Structure reorganised without touching `data/`, `Holo/` or
  `resources/` internals, so nothing in `data/tools/*.py` breaks.
- Loose documents filed: session log and audits → `docs/`, Word/PDF references → `reference/`,
  the old Drive-sync notes → `docs/archive/`.
- Added `CLAUDE.md` (auto-loaded project context), `README.md` (how to pick this up on a new
  machine), `.gitignore`, `docs/DECISIONS.md`, `docs/ARTIFACTS.md`.
- Retired the 2026-08-22 "local folder is source of truth + Drive mirror" arrangement.

## Decisions made

- **The Git repo is the source of truth**, replacing the local-folder-plus-Drive-mirror setup.
  Recorded in `docs/DECISIONS.md`.

## What's still open

- **GitHub remote is not connected yet.** The repo exists locally with one commit. It needs a
  private GitHub repo created and pushed to.
- **How Claude pushes on Mike's behalf** is unresolved. The sandbox this session runs commands
  in has no stored GitHub credentials and is ephemeral, so a token would need re-supplying each
  session. Options are in the hand-off below.
- Two empty directories (`Inspiration/`, `_sync/`) are left on disk. Their contents moved;
  the directories couldn't be removed without a deletion grant. Git ignores empty directories,
  so they're cosmetic.
- The Drive folder still holds two live Google Docs. If they're still being edited there,
  Drive remains authoritative for those and the `reference/` snapshots will drift.

## The thing worth knowing about session continuity

Researched against the Claude Code docs this session:

- **Claude Code CLI conversation history does not sync between machines.** It is stored at
  `~/.claude/projects/<escaped-path>/<session-id>.jsonl` on the machine it ran on, is not
  copied to the cloud, and is swept after ~30 days by default. `--resume` and `--continue`
  only search the local machine. There is an open feature request, no shipped feature.
- **Checkpoints / `/rewind` are local and session-scoped too** — and explicitly not a
  substitute for version control.
- **Cowork and claude.ai sessions are account-level and do sync** across any device signed in,
  and `claude --teleport` pulls a cloud session into a terminal. Scheduled tasks are
  account-level too.
- **Auto-memory is local-only** and swept on the same ~30-day cycle.

So the durable record is the one that gets committed. Hence `docs/sessions/` and the close-out
protocol in `CLAUDE.md`.

## Next three things

1. Create the private GitHub repo and push (see hand-off in the chat).
2. Decide how Claude authenticates to push — token each session, or GitHub Desktop.
3. Resume the actual work: Holo Deck direction is still unsettled (see
   `docs/sessions/2026-09-06-holo-deck.md` §7), and archaeological sites still need the v3 migration.

## Links

- Claude Design canvas: https://claude.ai/design/p/03be95db-3869-4f61-81e5-31ca2661406c
- Claude Code session docs: https://code.claude.com/docs/en/sessions
- Claude Code memory docs: https://code.claude.com/docs/en/memory

---

## Addendum — same session, after decisions

- **Remote set:** `https://github.com/nightowl-83/RiftNav.git`. Repo name is RiftNav, folder is
  still `Stellaris` locally; that's fine, nothing depends on the folder name.
- **Commit identity** corrected to `mcball83@gmail.com` (the GitHub account) and the first
  commit re-authored.
- **Google Drive retired.** Both Docs imported to `reference/` as Markdown. Neither had been
  edited since 20/21 August, so the exports were current — nothing was lost. The Drive folder
  and its daily parity audit are done.
- **Style guide artifact recovered.** The Mobbin doc pointed at a published Stellaris Helper
  Style Guide on claude.ai that wasn't recorded anywhere in the project. It's now in
  `docs/ARTIFACTS.md` — exactly the kind of thing that goes missing when a conversation closes.
- **`/close-out` and `/pick-up` slash commands added** under `.claude/commands/`. They're
  committed, so they exist on every clone.

---

## Addendum 2 — remote live

- **Pushed.** `main` is on GitHub at https://github.com/nightowl-83/RiftNav — two commits.
- **Auth:** fine-grained PAT, scoped to RiftNav only, Contents read/write. Stored at
  `.git/.credentials` (inside `.git`, so never committed) via `credential.helper store`.
  The token never passed through a chat transcript — it was handed over as a file in the
  project folder and deleted after install.
  **When it expires, pushes start failing.** Regenerate at
  https://github.com/settings/personal-access-tokens, save as `token.txt` in this folder,
  and ask Claude to reinstall it.
- **Weekly backstop:** a scheduled task runs Fridays 4pm CT. It pushes any commits sitting
  unpushed, reports uncommitted changes without committing them (a commit with no reasoning
  is worse than none), and flags commits that no session log covers. Silent when clean.
- **Caveat on the credential path:** `credential.helper` is set to the relative path
  `.git/.credentials`, which resolves from the repo root. It works from the sandbox Claude
  uses. If a `git push` run manually from Terminal ever prompts for a username, that's why —
  say so and it can be switched to an absolute path.
