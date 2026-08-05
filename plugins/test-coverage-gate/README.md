# test-coverage-gate

Run your project's test coverage and gate it against a configurable threshold.

## Components

- **`/coverage-gate [threshold]`** — runs coverage and reports PASS/FAIL vs a
  threshold (arg > `COVERAGE_THRESHOLD` env > config > default 80).
- **Skill: coverage-gating** — guidance on thresholds, diff coverage, and
  reading results; deep tooling notes in `skills/coverage-gating/reference/`.
- **Hook (PostToolUse)** — a once-per-session nudge to re-check coverage after
  source edits. Non-blocking.
- **`scripts/coverage.sh`** — POSIX sh; auto-detects pytest-cov, nyc/c8, or
  `go test -cover` and prints `COVERAGE_TOTAL=<n>`. Always exits 0.

## Notes

The hook and script never fail your build — they inform. Wire the threshold into
CI (see the reference file) when you want a hard gate.

Author: Matthews Wong · License: MIT
