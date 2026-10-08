---
description: Close out the working session — write the log, update decisions, commit and push
---

Close out this working session so the next machine can pick it up cold.

Do all of the following, in order. Don't skip a step because it seems empty — write "nothing
this session" instead, so the record is explicit.

1. **Write the session log.** Create `docs/sessions/YYYY-MM-DD-<short-topic>.md` using
   `docs/sessions/_TEMPLATE.md`. Use today's real date. Write it for a reader with no memory
   of this conversation: what we set out to do, what actually changed, what was decided, what
   is still open (including what went wrong), and the next three things. Be concrete — name
   files, name the reasoning. If a session log for today already exists, append to it rather
   than creating a second one.

2. **Update `docs/DECISIONS.md`** with any decision made this session that will still bind
   next month. Newest first. Include: what was decided, why, and what would overturn it. If
   this session reversed an earlier decision, add a new entry that says it supersedes the old
   one — never edit the old entry away.

3. **Update `docs/ARTIFACTS.md`** with any Claude Design page, published artifact, research
   output, or upstream source touched or created this session.

4. **Check nothing generated was hand-edited.** If `data/*.json` changed, confirm it came from
   `data/tools/build_v3.py` and that `data/tools/validate_v3.py` passes. Say so in the log.

5. **Commit and push.**
   - `git add -A`
   - Commit with a real message: a summary line, then a short body explaining *why*, not just
     what. End with the standard co-author trailer.
   - `git push`
   - If the push fails on auth, say so plainly and tell me what to do — do not retry in a loop.

6. **Update the Sync Ledger** (https://claude.ai/artifact/66KvEXdWfRziYjH3EyRj9v) so it shows
   where things stand after this push.
   - Run `scripts/sync-snapshot.sh main --print` and keep its output.
   - If the `ArtifactData` tool is available: `get` the document `projects/stellaris`, then
     `update` it (pin `if_version` to the version you read) with:
     - `snapshot`: the script output as an object — `taken`, `branch`, `sha`, `date`, `subject`,
       `dirty` (number), `upstream`, `upsha`, `ahead` and `behind` (from `aheadbehind`), and
       `branches`: one `{name, sha, date, vsMain, ahead, behind, tracked}` per `br=` line
       (`tracked` is false when the last field is empty).
     - `leftOff`: `summary` (one or two sentences on where this session stopped), `lastLog`
       (the session log path you just wrote), `warnings`, `open` and `next` (from the log).
     - `checklist`: `{}` and `updatedAt`: now.
     Leave `host` and `tools` alone unless this session changed hosting or a linked tool.
   - If `ArtifactData` isn't available (e.g. the CLI on another machine), print the script output
     and tell me to paste it into the ledger's **Update from snapshot**. Don't skip this step
     silently.

7. **Report back** in three lines: what was committed, what's still open, and the single
   next thing to pick up.
