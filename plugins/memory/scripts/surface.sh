#!/bin/sh
# surface.sh -- SessionStart auto-surface for the unified memory plugin.
#
# Prints BOTH:
#   (a) the top relevant prior LEARNINGS for the current folder (hybrid search), and
#   (b) the active INSTINCTS (global + folder-lineage) the agent should follow.
#
# Runs from the SessionStart hook. It must be non-blocking and must ALWAYS exit 0
# so a missing python interpreter or an absent store never disrupts the session.
# Output is purely informational context for the agent.

ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}"
SCRIPT="$ROOT/scripts/memory.py"

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

FOLDER="$(pwd)"

# (a) Relevant prior learnings for the current folder (already prints its own header).
"$PY" "$SCRIPT" recall "$FOLDER" 2>/dev/null

# (b) Active instincts (learned rules) for the global scope + current folder lineage.
INSTINCTS="$("$PY" "$SCRIPT" instincts --scope "$FOLDER" --min-confidence 0.5 2>/dev/null)"
if [ -n "$INSTINCTS" ]; then
  echo "Active instincts (learned rules to follow this session):"
  echo "$INSTINCTS"
fi

exit 0
