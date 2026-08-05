#!/bin/sh
# coverage.sh - detect the project's test toolchain, run coverage, and print a
# machine-readable total plus a short human summary. Non-blocking: always exit 0.
#
# Output contract:
#   COVERAGE_TOOL=<pytest-cov|nyc|c8|go|none>
#   COVERAGE_TOTAL=<integer-or-unknown>
# followed by a readable summary. The caller decides pass/fail.

set -u

emit() {
  echo "COVERAGE_TOOL=$1"
  echo "COVERAGE_TOTAL=$2"
}

have() { command -v "$1" >/dev/null 2>&1; }

# --- Python: pytest-cov -----------------------------------------------------
if [ -f "pyproject.toml" ] || [ -f "setup.cfg" ] || [ -f "setup.py" ] || ls tests/*.py >/dev/null 2>&1; then
  if have pytest && python -c "import pytest_cov" >/dev/null 2>&1; then
    echo "Detected pytest-cov. Running coverage..."
    out=$(pytest --cov --cov-report=term-missing 2>/dev/null | tee /dev/stderr)
    total=$(printf '%s\n' "$out" | grep -Ei '^TOTAL' | grep -oE '[0-9]+%' | tail -n1 | tr -d '%')
    [ -n "${total:-}" ] && emit "pytest-cov" "$total" || emit "pytest-cov" "unknown"
    exit 0
  fi
fi

# --- JavaScript/TypeScript: nyc or c8 --------------------------------------
if [ -f "package.json" ]; then
  if have npx && npx --no-install nyc --version >/dev/null 2>&1; then
    echo "Detected nyc. Running coverage..."
    out=$(npx --no-install nyc --reporter=text-summary npm test 2>/dev/null | tee /dev/stderr)
    total=$(printf '%s\n' "$out" | grep -i 'Lines' | grep -oE '[0-9]+(\.[0-9]+)?%' | head -n1 | tr -d '%' | cut -d. -f1)
    [ -n "${total:-}" ] && emit "nyc" "$total" || emit "nyc" "unknown"
    exit 0
  fi
  if have npx && npx --no-install c8 --version >/dev/null 2>&1; then
    echo "Detected c8. Running coverage..."
    out=$(npx --no-install c8 --reporter=text-summary npm test 2>/dev/null | tee /dev/stderr)
    total=$(printf '%s\n' "$out" | grep -i 'Lines' | grep -oE '[0-9]+(\.[0-9]+)?%' | head -n1 | tr -d '%' | cut -d. -f1)
    [ -n "${total:-}" ] && emit "c8" "$total" || emit "c8" "unknown"
    exit 0
  fi
fi

# --- Go: go test -cover -----------------------------------------------------
if [ -f "go.mod" ] && have go; then
  echo "Detected Go. Running go test -cover..."
  out=$(go test -cover ./... 2>/dev/null | tee /dev/stderr)
  # Average the per-package coverage percentages as a rough total.
  total=$(printf '%s\n' "$out" | grep -oE 'coverage: [0-9]+(\.[0-9]+)?%' | grep -oE '[0-9]+(\.[0-9]+)?' | awk '{s+=$1; n++} END{ if(n>0) printf "%d", s/n; else print "unknown" }')
  [ -n "${total:-}" ] && emit "go" "$total" || emit "go" "unknown"
  exit 0
fi

echo "No supported coverage tool detected (looked for pytest-cov, nyc, c8, go)."
emit "none" "unknown"
exit 0
