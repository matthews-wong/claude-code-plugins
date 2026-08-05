---
name: coverage-gate
description: Run test coverage and check it against a configurable threshold.
args: "[threshold] (optional integer percent, e.g. 80)"
---

Run the project's test coverage and evaluate it against a threshold.

Steps:

1. Determine the threshold. Use the argument if provided. Otherwise look for a
   configured value in this order: `COVERAGE_THRESHOLD` environment variable,
   a `coverage-gate` key in project config, then default to 80.

2. Run the coverage helper script, which auto-detects the toolchain:

   ```sh
   sh "${CLAUDE_PLUGIN_ROOT}/scripts/coverage.sh"
   ```

   The script detects pytest-cov, nyc/c8 (JS/TS), or `go test -cover` and prints
   a `COVERAGE_TOTAL=<number>` line plus a human summary. It never fails the
   build itself (always exits 0) — you own the pass/fail decision.

3. Parse the reported total percentage. Compare against the threshold.

4. Report clearly:
   - PASS when total >= threshold. State the margin.
   - FAIL when total < threshold. State the gap and name the least-covered
     files or packages from the report so the user knows where to add tests.

5. If no coverage tool or report is detected, say so plainly and suggest the
   right tool for the detected language (pytest-cov, nyc/c8, or go cover).
   Do not invent a coverage number.

Keep the output short: verdict first, then the few actionable details.
