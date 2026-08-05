#!/bin/sh
# run-tests.sh — detect and run the project's fast test suite after an edit.
#
# Invoked by the PostToolUse hook of test-guardian after Edit/Write so you get an
# immediate pass/fail signal without asking. It is intentionally NON-BLOCKING:
# it always exits 0 so a failing test never interrupts the session — the summary
# is advisory feedback. This is a starting point; adapt the commands to your project.
#
# Keep it FAST: prefer the quick unit suite over full end-to-end runs, since this
# fires on every file write.

set -u

status=0
ran=0

report() {
  label="$1"
  shift
  ran=1
  if "$@" >/tmp/test-guardian.$$ 2>&1; then
    printf '[test-guardian] PASS: %s\n' "$label"
  else
    printf '[test-guardian] FAIL: %s\n' "$label"
    # Surface the tail of the output so the failure is visible in-transcript.
    tail -n 25 /tmp/test-guardian.$$ 2>/dev/null
    status=1
  fi
  rm -f /tmp/test-guardian.$$ 2>/dev/null
}

# --- Node / npm ----------------------------------------------------------
if [ -f package.json ] && command -v npm >/dev/null 2>&1; then
  if npm run 2>/dev/null | grep -q '^  test$'; then
    # Pass through to whatever the project's test script is; keep it quiet.
    report "npm test" npm test --silent
  fi
fi

# --- Python --------------------------------------------------------------
if [ "$ran" -eq 0 ] && { [ -f pyproject.toml ] || [ -f pytest.ini ] || [ -f setup.cfg ]; }; then
  if command -v pytest >/dev/null 2>&1; then
    # -x stops at first failure to stay fast on the post-edit path.
    report "pytest" pytest -q -x
  elif command -v python >/dev/null 2>&1 && python -c "import pytest" >/dev/null 2>&1; then
    report "pytest" python -m pytest -q -x
  fi
fi

# --- Make ----------------------------------------------------------------
if [ "$ran" -eq 0 ] && [ -f Makefile ] && grep -Eq '^test:' Makefile && command -v make >/dev/null 2>&1; then
  report "make test" make test
fi

# --- Go ------------------------------------------------------------------
if [ "$ran" -eq 0 ] && [ -f go.mod ] && command -v go >/dev/null 2>&1; then
  report "go test" go test ./...
fi

# --- Summary -------------------------------------------------------------
if [ "$ran" -eq 0 ]; then
  printf '[test-guardian] No test suite detected; skipping. Adapt scripts/run-tests.sh for this project.\n'
elif [ "$status" -eq 0 ]; then
  printf '[test-guardian] All detected tests passed.\n'
else
  printf '[test-guardian] Tests failing — see output above.\n'
fi

# Non-blocking: never fail the hook.
exit 0
