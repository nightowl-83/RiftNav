# Stellaris Helper

Reference data and UI design for an Astral Rifts / Archaeological Sites companion tool.

**This repository is the source of truth.** Not any one laptop. If it isn't committed and
pushed, it doesn't exist.

---

## Picking this up on a new machine

```bash
git clone <REPO_URL> stellaris
cd stellaris
claude
```

That's it. Claude Code reads `CLAUDE.md` automatically and comes up with the full project
context. Then read, in order:

1. **`docs/DECISIONS.md`** — every decision that still binds, and why.
2. **`docs/sessions/`** — newest file. Where the last working session left off.
3. **`docs/ARTIFACTS.md`** — the live Claude Design canvas, published artifacts, research outputs.

## Finishing a working session

Ask Claude to "close out the session." It will write a session log, update the decision log
and artifact index, and commit and push. Nothing should be left uncommitted at the end of a
sitting — that's the whole mechanism.

## What's here

| Path | What it is |
|---|---|
| `data/` | Generated datasets + the Python that builds them. **Read `data/README.md` before touching anything here.** |
| `Holo/` | "Holo Deck" background prototypes, reference stills, motion spec |
| `reference/` | Source reference documents (Word/PDF exports) |
| `resources/` | Image manifest + fetch tooling |
| `docs/` | Decisions, session logs, audits, artifact index |
| `docs/archive/` | Retired setups kept for history — see the note inside |

## Conventions

- Generated files are never hand-edited. Regenerate with the scripts in `data/tools/`.
- Reference documents are inputs. Datasets are outputs. Don't blur them.
- Session logs are dated `YYYY-MM-DD-topic.md` and are append-only history — don't rewrite old ones.
