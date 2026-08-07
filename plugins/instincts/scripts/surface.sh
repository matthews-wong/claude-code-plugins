#!/bin/sh
# surface.sh -- print the top active instincts at session start.
#
# Runs from the SessionStart hook. It must be non-blocking and must always
# exit 0 so a missing python interpreter or an absent store never disrupts the
# session. Output is purely informational context for the agent.

ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}"
SCRIPT="$ROOT/scripts/instincts.py"

# Pick whatever Python is available; degrade silently if none is.
PY=""
if command -v python3 >/dev/null 2>&1; then
  PY="python3"
elif command -v python >/dev/null 2>&1; then
  PY="python"
else
  exit 0
fi

if [ ! -f "$SCRIPT" ]; then
  exit 0
fi

# Current folder relative to the project, used as the scope filter.
FOLDER="$(pwd)"

OUTPUT="$("$PY" "$SCRIPT" list --scope "$FOLDER" --min-confidence 0.5 2>/dev/null)"

if [ -n "$OUTPUT" ] && [ "$OUTPUT" != "No instincts recorded yet." ]; then
  echo "Active instincts (learned rules to follow this session):"
  echo "$OUTPUT"
fi

exit 0
