#!/bin/sh
# verify.sh — auto-detect and run the project's verification checks.
#
# Invoked by the Stop hook of the verify-before-review plugin so that the
# project's own quality gates run before you review the work. It is a starting
# point: adapt the detected commands to match your project's real scripts.
#
# Exit code is always 0 so the hook never blocks the session; the PASS/FAIL
# summary is advisory. Tighten this to `exit 1` on failure if you want a hard gate.

set -u

overall_status=0
ran_anything=0

section() {
  printf '\n=== %s ===\n' "$1"
}

run_check() {
  label="$1"
  shift
  ran_anything=1
  printf -- '--- %s: %s\n' "$label" "$*"
  if "$@"; then
    printf '[PASS] %s\n' "$label"
  else
    printf '[FAIL] %s\n' "$label"
    overall_status=1
  fi
}

# --- Node / npm projects -------------------------------------------------
if [ -f package.json ]; then
  section "Node project detected (package.json)"
  if command -v npm >/dev/null 2>&1; then
    # Only run scripts that actually exist to avoid npm errors.
    if npm run 2>/dev/null | grep -q '^  test$'; then
      run_check "npm test" npm test --silent
    fi
    if npm run 2>/dev/null | grep -q '^  lint$'; then
      run_check "npm run lint" npm run lint --silent
    fi
    if npm run 2>/dev/null | grep -q '^  build$'; then
      run_check "npm run build" npm run build --silent
    fi
  else
    printf 'npm not found on PATH; skipping Node checks.\n'
  fi
fi

# --- Python projects -----------------------------------------------------
if [ -f pyproject.toml ] || [ -f setup.cfg ] || [ -f pytest.ini ] || [ -f tox.ini ]; then
  section "Python project detected"
  if command -v pytest >/dev/null 2>&1; then
    run_check "pytest" pytest -q
  elif command -v python >/dev/null 2>&1 && python -c "import pytest" >/dev/null 2>&1; then
    run_check "pytest" python -m pytest -q
  fi
  if command -v ruff >/dev/null 2>&1; then
    run_check "ruff check" ruff check .
  fi
fi

# --- Make-based projects -------------------------------------------------
if [ -f Makefile ]; then
  if grep -Eq '^test:' Makefile; then
    section "Makefile detected (test target)"
    if command -v make >/dev/null 2>&1; then
      run_check "make test" make test
    fi
  fi
fi

# --- Summary -------------------------------------------------------------
section "Verification summary"
if [ "$ran_anything" -eq 0 ]; then
  printf 'No known checks detected (no package.json, pyproject, or Makefile test target).\n'
  printf 'Adapt %s to run your project checks.\n' "${CLAUDE_PLUGIN_ROOT:-this plugin}/scripts/verify.sh"
elif [ "$overall_status" -eq 0 ]; then
  printf 'RESULT: PASS — all detected checks succeeded. Safe to move on to review.\n'
else
  printf 'RESULT: FAIL — one or more checks failed. Fix before review.\n'
fi

# Non-blocking by design.
exit 0
