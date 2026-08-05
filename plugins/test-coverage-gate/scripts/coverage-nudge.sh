#!/bin/sh
# coverage-nudge.sh - PostToolUse nudge. When a source file is edited, remind
# (once per session) that coverage may have shifted. Non-blocking: exit 0 always.

set -u

MARKER="${TMPDIR:-/tmp}/.coverage_gate_nudged"

# Only nudge once per session to avoid noise.
if [ -f "$MARKER" ]; then
  exit 0
fi

touch "$MARKER" 2>/dev/null || true
echo "[test-coverage-gate] Source changed. Consider running /coverage-gate before committing."
exit 0
