---
name: coverage-gating
description: >
  Use when the user asks to check, enforce, or gate test coverage, set a
  coverage threshold, find untested code, or wants to know why coverage
  dropped. Triggers: "coverage", "coverage gate", "coverage threshold",
  "untested code", "pytest-cov", "nyc", "c8", "go test -cover", "fail build
  under X% coverage".
---

# Coverage Gating

Measure test coverage, compare it to a threshold, and turn the result into an
actionable verdict. Coverage is a floor for confidence, not a proof of
correctness — treat a passing gate as "no obvious untested paths," not "bug-free."

## Quick workflow

1. Pick the threshold: CLI arg > `COVERAGE_THRESHOLD` env > project config > 80.
2. Run `sh "${CLAUDE_PLUGIN_ROOT}/scripts/coverage.sh"`. It auto-detects the
   toolchain and prints `COVERAGE_TOTAL=<n>`.
3. Compare total to threshold. Report PASS/FAIL with the gap and the
   least-covered files.

## Choosing a threshold honestly

- 100% is rarely worth it; 70-85% line coverage is a common enterprise floor.
- Prefer a **ratchet**: never let coverage fall below its current value, and
  raise the floor as it improves. Avoid a hard number that blocks unrelated work.
- Gate on **diff/patch coverage** (new code) when possible — it catches
  under-tested changes without penalizing legacy code.

## Reading results well

- Line coverage counts executed lines; branch coverage counts decision paths.
  Branch coverage is the stronger signal — a line can run without its
  false-branch ever being tested.
- A high total can hide a critical untested module. Always name the
  lowest-covered files, not just the aggregate.

## Tool specifics and CI wiring

See `./reference/tooling.md` for exact commands, config keys, and CI examples
for pytest-cov, nyc/c8, and Go.

## Guardrails

- The gate is advisory unless the user wires it into CI. The provided hook and
  script never block; they inform.
- Never fabricate a percentage. If the script reports `unknown`, say the tool or
  report was not found and suggest how to enable it.
