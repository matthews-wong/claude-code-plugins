---
name: audit-deps
description: Run a dependency vulnerability audit using the project's native ecosystem tooling and triage the findings by severity and exploitability.
---

You are helping the user audit their project's dependencies for known vulnerabilities using real, ecosystem-native tools. Never invent CVE identifiers, severities, or advisory data — only report what the tools actually return.

## What to do

1. Detect the ecosystem(s) present by looking for manifest/lock files:
   - Node.js: `package.json` + `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`
   - Python: `requirements.txt` / `pyproject.toml` / `poetry.lock` / `Pipfile.lock`
   - Rust: `Cargo.toml` + `Cargo.lock`
   - Go: `go.mod` + `go.sum`
2. Load the `dependency-audit` skill for the exact commands, flags, and triage workflow for each ecosystem.
3. Run the appropriate native audit tool(s). Ask before installing anything the user does not already have. Prefer non-mutating audit commands (do not auto-upgrade dependencies without consent).
4. Parse the real output and triage:
   - Severity (from the advisory: critical/high/moderate/low).
   - Whether a fix is available (fixed version) and whether it is a breaking upgrade.
   - Direct vs transitive dependency.
   - Reachability/exploitability context if the tool provides it (e.g. govulncheck call-graph analysis).
5. Produce a prioritized remediation plan: what to upgrade, to which version, and which findings can be deferred or need a documented risk acceptance.

## How to report

Summarize counts by severity, then list actionable findings (package, installed version, advisory ID, fixed version, direct/transitive). Distinguish "fix available now" from "no fix yet". Recommend re-running the audit after remediation. Be explicit that this reflects the advisory databases as of the run time and should be integrated into CI for continuous coverage.
