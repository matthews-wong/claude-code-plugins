---
name: verify
description: Run the project's tests, lint, and build, then report a clear PASS/FAIL summary before the user reviews the changes.
---

You are performing **Step 1: self-verification** before any human review. Your job
is to prove the current changes actually work, not to assume they do.

Do the following:

1. **Detect the project's toolchain** by inspecting the repo root:
   - `package.json` → Node/npm (or the lockfile's package manager: pnpm, yarn, bun).
   - `pyproject.toml` / `setup.cfg` / `pytest.ini` → Python.
   - `Makefile` with a `test` target → Make.
   - `Cargo.toml` → Rust, `go.mod` → Go, etc. Use the idiomatic commands for whatever you find.

2. **Run the available checks**, in this order, skipping any that don't exist:
   - Tests (e.g. `npm test`, `pytest -q`, `make test`, `cargo test`, `go test ./...`).
   - Lint / static analysis (e.g. `npm run lint`, `ruff check .`, `golangci-lint run`).
   - Build / typecheck (e.g. `npm run build`, `tsc --noEmit`, `cargo build`).

   Only run scripts that genuinely exist — check `package.json` scripts or the
   Makefile targets first. Do not invent commands.

3. **Report a concise PASS/FAIL summary** as a table: each check, the exact command
   you ran, and its result. For any failure, quote the relevant error lines and
   name the file(s) involved.

4. **State a clear verdict**: either "Verified — ready for review" or
   "Not ready — the following must be fixed first," followed by the specific
   failing items. Do not attempt fixes unless the user asks; the goal here is an
   honest verification report.

If no checks can be found, say so explicitly and suggest which scripts the project
should add rather than silently reporting success.
