#!/bin/sh
# Stop hook: a gentle NUDGE to record learnings.
#
# Honesty note: a hook cannot read the model's reasoning, so it cannot know what
# was actually learned. It only reminds the model/user to distill any notable
# lesson with /learn (or /remember). Capture itself is skill/command-driven, not
# automatic.
#
# Always non-blocking; always exits 0.
STORE="${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/memory/notes.jsonl"

count=0
if [ -f "$STORE" ]; then
  # Count non-empty lines; tolerate any failure.
  count=$(grep -c . "$STORE" 2>/dev/null || echo 0)
fi

# Nudge when the store looks small/stale (few or no notes captured yet).
if [ "$count" -lt 5 ] 2>/dev/null; then
  echo "memory: if something non-obvious was solved or decided, capture it with /learn so the next agent inherits it (store has ${count} learning(s))."
fi
exit 0
