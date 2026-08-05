---
name: test-guardian
description: Explain the test-guardian auto-test hook and run the project's fast test suite on demand.
---

The **test-guardian** plugin installs a `PostToolUse` hook that runs the project's
fast test suite automatically after Claude edits or writes a file, giving an
immediate, non-blocking pass/fail signal. This command lets you understand and
trigger that guard manually.

Do the following:

1. **Explain the guard briefly**: after each `Edit`/`Write`, the hook runs
   `scripts/run-tests.sh`, which detects the toolchain (npm test, `pytest -q -x`,
   `make test`, or `go test ./...`) and prints a PASS/FAIL summary. It is
   non-blocking — a failing test reports but never halts the session.

2. **Run the fast test suite now**, the same way the hook would:
   - Detect the project's test command from `package.json`, `pyproject.toml` /
     `pytest.ini`, a `Makefile` `test:` target, or `go.mod`.
   - Run the quick unit suite (not the full end-to-end run) and report the result.

3. **If tests fail**, summarize which tests failed and the likely cause, and offer
   to fix them — but do not change code unless I confirm.

4. **If no test suite is detected**, say so and suggest how to wire one up so the
   guard becomes useful (e.g. add a `test` script to `package.json`).

This is the tight feedback loop behind "Step 1: verify" — catch regressions the
moment they're introduced, before review.
