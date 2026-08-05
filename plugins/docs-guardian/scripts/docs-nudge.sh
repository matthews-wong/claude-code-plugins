#!/bin/sh
# docs-nudge.sh - PostToolUse nudge. If the edited file looks like source code
# (not a doc), suggest running /docs-check. Once per session. Never blocks.

set -u

MARKER="${TMPDIR:-/tmp}/.docs_guardian_nudged"
[ -f "$MARKER" ] && exit 0

# Try to read the edited file path from the hook payload on stdin (best effort).
PAYLOAD=$(cat 2>/dev/null || true)
FILE=$(printf '%s' "$PAYLOAD" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed 's/.*"\([^"]*\)"$/\1/')

# Only nudge for source-looking files; skip doc edits.
case "$FILE" in
  *.md|*README*|*CHANGELOG*|*/docs/*) exit 0 ;;
esac

touch "$MARKER" 2>/dev/null || true
echo "[docs-guardian] Source changed. Docs may be stale — run /docs-check to verify."
exit 0
