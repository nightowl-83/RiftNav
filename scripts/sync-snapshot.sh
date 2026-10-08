#!/usr/bin/env bash
# Prints a sync snapshot of this repo for the Sync Ledger page
# (https://claude.ai/artifact/66KvEXdWfRziYjH3EyRj9v) and, on a Mac, copies it to the clipboard.
# Paste the output into the ledger's "Update from snapshot" box.
#
# Usage:  scripts/sync-snapshot.sh            # production branch = main
#         scripts/sync-snapshot.sh release    # a different production branch
#         scripts/sync-snapshot.sh main --print   # print only, don't touch the clipboard
set -euo pipefail
prod="${1:-main}"
cd "$(git rev-parse --show-toplevel)"
git fetch -q --all || echo "warning: fetch failed; GitHub numbers may be stale" >&2

out="$(
  echo "taken=$(date '+%Y-%m-%d %H:%M')"
  echo "branch=$(git branch --show-current)"
  echo "sha=$(git rev-parse --short HEAD)"
  echo "date=$(git log -1 --format=%cs)"
  echo "subject=$(git log -1 --format=%s)"
  echo "dirty=$(git status --porcelain | wc -l | tr -d ' ')"
  echo "upstream=$(git rev-parse --abbrev-ref '@{u}' 2>/dev/null || true)"
  echo "upsha=$(git rev-parse --short '@{u}' 2>/dev/null || true)"
  echo "aheadbehind=$(git rev-list --left-right --count 'HEAD...@{u}' 2>/dev/null || true)"
  for b in $(git for-each-ref refs/heads --format='%(refname:short)'); do
    echo "br=$b|$(git rev-parse --short "$b")|$(git log -1 --format=%cs "$b")|$(git rev-list --count "origin/$prod..$b" 2>/dev/null || echo 0)|$(git rev-list --left-right --count "$b...$b@{u}" 2>/dev/null || true)"
  done
)"

echo "$out"
if [[ "${2:-}" != "--print" ]] && command -v pbcopy >/dev/null 2>&1; then
  printf '%s\n' "$out" | pbcopy
  echo "(copied to clipboard)" >&2
fi
