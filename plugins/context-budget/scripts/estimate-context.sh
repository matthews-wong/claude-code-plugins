#!/bin/sh
# estimate-context.sh — non-blocking SessionStart notice.
# Estimates the token weight of always-loaded memory files (CLAUDE.md) so the
# user notices when their always-on context is getting heavy. Advisory only:
# it never edits files, never fails the session, and exits 0 no matter what.
#
# Token estimate uses words / 0.75 (~1.33 tokens/word for English prose).
# The threshold below is a soft nudge, not a hard rule.

THRESHOLD_TOKENS=1500

# Word count -> rough token estimate. POSIX awk integer math.
estimate_tokens() {
  words=$(wc -w < "$1" 2>/dev/null | tr -d ' ')
  [ -z "$words" ] && words=0
  # tokens = words / 0.75  ==  words * 4 / 3
  echo $(( words * 4 / 3 ))
}

scan_dir="${CLAUDE_PROJECT_DIR:-.}"

# Collect candidate memory files without failing if none exist.
total=0
found=0
for f in "$scan_dir/CLAUDE.md" "$scan_dir/.claude/CLAUDE.md"; do
  [ -f "$f" ] || continue
  found=1
  t=$(estimate_tokens "$f")
  total=$(( total + t ))
  if [ "$t" -ge "$THRESHOLD_TOKENS" ]; then
    echo "[context-budget] $f ~${t} tokens (heavy — consider /context-audit)"
  else
    echo "[context-budget] $f ~${t} tokens (lean)"
  fi
done

if [ "$found" -eq 1 ] && [ "$total" -ge "$THRESHOLD_TOKENS" ]; then
  echo "[context-budget] Always-loaded memory ~${total} tokens. Run /context-audit to trim bloat and apply progressive disclosure."
fi

exit 0
