# verify-before-review

A self-verification loop for Claude Code. It embodies the "Step 1 → Step 2"
discipline: **verify that your change works before you ask anyone (or any agent)
to review it.**

## What it installs

- **Command `/verify`** — asks Claude to detect the project's toolchain and run
  its tests, lint, and build, then report a clear PASS/FAIL summary and a verdict
  on whether the changes are ready for review.
- **Stop hook** — when Claude finishes responding, runs
  `scripts/verify.sh`, which auto-detects and executes the project's checks and
  prints a PASS/FAIL summary into the transcript.
- **`scripts/verify.sh`** — a POSIX `sh` script that detects:
  - `package.json` → runs `npm test` / `npm run lint` / `npm run build` when those
    scripts exist,
  - Python (`pyproject.toml`, `pytest.ini`, …) → runs `pytest -q` and `ruff check .`,
  - `Makefile` with a `test:` target → runs `make test`.

## How to use

1. Install/enable the plugin in Claude Code.
2. Run `/verify` any time you want an on-demand verification report.
3. The Stop hook runs automatically at the end of each turn and appends a
   PASS/FAIL summary.

## Notes

- The Stop hook is **non-blocking** by design (`verify.sh` always exits `0`) so it
  never wedges your session; the summary is advisory. If you want a hard gate,
  change the final `exit 0` in `scripts/verify.sh` to `exit 1` on failure.
- `scripts/verify.sh` is a **starting point** — adapt the detected commands to
  match your project's real scripts and package manager.
