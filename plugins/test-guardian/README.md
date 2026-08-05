# test-guardian

Runs your project's **fast test suite automatically after every edit**, so
regressions surface the moment they're introduced — the tight feedback loop that
makes "Step 1: verify" cheap.

## What it installs

- **PostToolUse hook** — after any `Edit` or `Write`, runs
  `scripts/run-tests.sh`.
- **`scripts/run-tests.sh`** — a POSIX `sh` script that detects the toolchain and
  runs the quick unit suite:
  - `package.json` + `npm test` script → `npm test`,
  - Python (`pyproject.toml` / `pytest.ini` / `setup.cfg`) → `pytest -q -x`,
  - `Makefile` with a `test:` target → `make test`,
  - `go.mod` → `go test ./...`.
  It prints a `[test-guardian] PASS/FAIL` summary and, on failure, the tail of the
  output.
- **Command `/test-guardian`** — explains the guard and runs the fast suite on
  demand.

## How to use

Enable the plugin and just work normally. After Claude edits a file, the hook runs
your fast tests and reports the result inline. Run `/test-guardian` any time to
trigger the same check manually or to see what it detects.

## Notes

- The hook is **non-blocking** by design (`run-tests.sh` always exits `0`) so a
  failing test never halts the session — treat the output as advisory feedback.
- It targets the **fast** suite (e.g. `pytest -x`) because it fires on every write;
  keep full end-to-end runs for `/verify` or CI.
- `scripts/run-tests.sh` is a **starting point** — adapt the detected commands to
  your project's real test setup and package manager.
