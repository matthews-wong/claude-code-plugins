#!/bin/sh
# docs-scan.sh - first-pass documentation drift scanner. Lists changed source
# files, finds doc files, and heuristically flags likely-stale docs. It emits
# leads only and never blocks. Always exit 0.

set -u

if ! command -v git >/dev/null 2>&1 || ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "docs-scan: not a git repository; skipping change detection."
  exit 0
fi

# Changed source files (staged + unstaged + untracked), doc/config files excluded.
CHANGED=$(git status --porcelain 2>/dev/null | awk '{print $2}' \
  | grep -Ev '(\.md$|^docs/|README|CHANGELOG|mkdocs|docusaurus|conf\.py)' \
  | grep -Ei '\.(py|js|ts|tsx|jsx|go|rb|java|kt|rs|php|cs|sh)$' || true)

if [ -z "${CHANGED:-}" ]; then
  echo "docs-scan: no changed source files detected."
  exit 0
fi

echo "docs-scan: changed source files:"
printf '  %s\n' $CHANGED

# Locate documentation surfaces in the repo.
DOCS=$(git ls-files 2>/dev/null | grep -Ei '(^README|(^|/)docs/|\.md$|^CHANGELOG|mkdocs\.ya?ml|docusaurus\.config|conf\.py|\.env\.example)' || true)

echo ""
if [ -n "${DOCS:-}" ]; then
  echo "docs-scan: documentation surfaces to check:"
  printf '%s\n' "$DOCS" | sed 's/^/  /'
else
  echo "docs-scan: no documentation files found in the repo."
fi

# High-signal heuristics on the diff itself.
echo ""
echo "docs-scan: potential drift signals in the diff:"
DIFF=$(git diff 2>/dev/null; git diff --staged 2>/dev/null)
flag() { printf '%s\n' "$DIFF" | grep -Eiq "$1" && echo "  - $2" || true; }

flag '^[+-].*(def |function |func |public |export ).*\(' "public signature(s) changed -> update API docs/examples"
flag '^[+-].*(add_argument|argparse|flag\.|cobra|yargs|click\.|commander)' "CLI flags/commands changed -> update README usage and --help"
flag '^[+-].*(os\.environ|process\.env|getenv|ENV\[|System\.getenv)' "env var usage changed -> update config docs and .env.example"
flag '^[+-].*(version|VERSION).*=.*[0-9]' "version constant changed -> update install/CHANGELOG"
flag '^[+-].*(default ?= ?|DEFAULT)' "default value changed -> update docs describing behavior"

echo ""
echo "docs-scan: leads only. Verify each against the actual docs before editing."
exit 0
