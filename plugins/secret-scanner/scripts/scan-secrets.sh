#!/bin/sh
# secret-scanner: heuristic, grep-based secret detector for the working diff.
# NON-BLOCKING by design: always exits 0. This is a safety net, not a gate,
# and NOT a replacement for a dedicated secret scanner (gitleaks/trufflehog).

set -u

PREFIX="[secret-scanner]"

# Prefer scanning only what is about to change. Fall back gracefully.
DIFF=""
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  DIFF="$( { git diff --staged; git diff; } 2>/dev/null | grep -E '^\+' | grep -Ev '^\+\+\+' )"
fi

if [ -z "${DIFF}" ]; then
  echo "${PREFIX} No pending diff to scan (or not a git repo). Skipping heuristic scan."
  exit 0
fi

# Heuristic patterns. Broad on purpose; expect false positives.
PATTERNS='
AKIA[0-9A-Z]{16}
ASIA[0-9A-Z]{16}
AIza[0-9A-Za-z_-]{35}
ghp_[0-9A-Za-z]{36,}
gho_[0-9A-Za-z]{36,}
ghs_[0-9A-Za-z]{36,}
github_pat_[0-9A-Za-z_]{22,}
glpat-[0-9A-Za-z_-]{20}
xox[baprs]-[0-9A-Za-z-]{10,}
sk_live_[0-9A-Za-z]{16,}
rk_live_[0-9A-Za-z]{16,}
sk-[0-9A-Za-z]{20,}
SG\.[0-9A-Za-z_-]{16,}\.[0-9A-Za-z_-]{16,}
npm_[0-9A-Za-z]{36}
-----BEGIN [A-Z ]*PRIVATE KEY-----
(password|passwd|secret|token|api[_-]?key|client[_-]?secret)[[:space:]]*[:=][[:space:]]*.{8,}
(postgres|postgresql|mysql|mongodb|redis|amqp)://[^:@/]+:[^@/]+@
'

FOUND=0
echo "${PREFIX} Heuristic scan of pending additions:"
for p in ${PATTERNS}; do
  # -I ignores binary; case-insensitive for the generic assignment patterns is fine.
  MATCHES="$(printf '%s\n' "${DIFF}" | grep -InE "${p}" 2>/dev/null)"
  if [ -n "${MATCHES}" ]; then
    FOUND=$((FOUND + 1))
    echo "  ! possible match for /${p}/:"
    printf '%s\n' "${MATCHES}" | head -n 5 | sed 's/^/      /'
  fi
done

if [ "${FOUND}" -eq 0 ]; then
  echo "  clean (no heuristic matches). Note: absence of matches does NOT prove absence of secrets."
else
  echo "${PREFIX} ${FOUND} pattern group(s) matched. Review above — some may be placeholders or false positives."
  echo "${PREFIX} If a real credential is exposed, rotate/revoke it; removing the line is not enough once pushed."
fi

# Always non-blocking.
exit 0
