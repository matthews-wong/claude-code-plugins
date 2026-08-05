# Ecosystem audit tools reference

Use the native tool for each ecosystem. Each reads from an authoritative advisory database. Do not substitute memorized CVE data for real tool output.

## Node.js — npm / pnpm / yarn

- `npm audit` — audits the dependency tree against the GitHub Advisory Database. Requires a lockfile.
- `npm audit --json` — machine-readable output for parsing.
- `npm audit --omit=dev` — production dependencies only.
- `npm audit fix` — applies non-breaking upgrades; `npm audit fix --force` may apply breaking ones (get consent first).
- pnpm: `pnpm audit` / `pnpm audit --json`.
- yarn (berry): `yarn npm audit --recursive`; classic yarn: `yarn audit`.

## Python — pip-audit

- Install: `pipx install pip-audit` (preferred) or `pip install pip-audit`.
- `pip-audit` — audits the current environment against PyPI and the OSV database.
- `pip-audit -r requirements.txt` — audit a requirements file without installing.
- `pip-audit -f json` — JSON output.
- `pip-audit --fix` — attempt to upgrade to fixed versions.
- Note: for Poetry/PDM, export or point at the locked requirements. `safety` is an alternative tool but pip-audit is OSV-backed and vendor-neutral.

## Rust — cargo audit

- Install: `cargo install cargo-audit`.
- `cargo audit` — checks `Cargo.lock` against the RustSec Advisory Database.
- `cargo audit --json` — JSON output.
- Also flags yanked crates and unmaintained crates (informational advisories).

## Go — govulncheck

- Install: `go install golang.org/x/vuln/cmd/govulncheck@latest`.
- `govulncheck ./...` — checks against the Go vulnerability database.
- Key advantage: **call-graph reachability** — it reports whether vulnerable symbols are actually reachable from your code, not just present in the module graph. This dramatically reduces noise.
- `govulncheck -json ./...` — JSON output.

## General gotchas

- A lockfile is usually required for an accurate tree; audits of manifests-only can be incomplete.
- Dev vs prod scoping matters — a dev-only vuln may be lower priority.
- Re-run after remediation to confirm the finding clears.
