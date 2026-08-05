---
name: dependency-audit
description: Run and triage dependency vulnerability audits across Node.js, Python, Rust, and Go using native tools (npm audit, pip-audit, cargo audit, govulncheck). Use when auditing dependencies for known CVEs or prioritizing remediation.
---

# Dependency audit

Audit dependencies for known vulnerabilities using each ecosystem's native, authoritative tooling. Report only what the tools return — never fabricate CVE IDs, severities, or advisory text.

## Workflow

1. Identify the ecosystem from manifest/lock files.
2. Run the native audit tool (see `reference/tools.md` for exact commands and flags).
3. Triage each finding (see `reference/triage.md`).
4. Produce a prioritized remediation plan.
5. Recommend wiring the same tool into CI for continuous coverage.

## Quick command map

- **Node.js**: `npm audit` (or `npm audit --json`); `pnpm audit`; `yarn npm audit`.
- **Python**: `pip-audit` (uses PyPI + OSV advisory data).
- **Rust**: `cargo audit` (RustSec Advisory DB).
- **Go**: `govulncheck ./...` (Go vuln DB, with call-graph reachability).

See `reference/tools.md` for installation, JSON output, and options.

## Triage priorities (summary)

Rank by: severity → fix availability → reachability → direct vs transitive → exposure of the affected code path. A critical CVE in an unreachable transitive dev-dependency may rank below a high CVE in a reachable runtime path. Full rubric in `reference/triage.md`.

## Honesty rules

- Only report advisory IDs, severities, and fixed versions that the tool actually emitted.
- If unsure whether a finding applies, say so and point to the upstream advisory URL.
- Note the timestamp of the run; advisory databases update continuously.

## References (load on demand)

- `reference/tools.md` — per-ecosystem commands, install, JSON flags, gotchas.
- `reference/triage.md` — severity/reachability triage rubric and remediation patterns.
