# dependency-auditor

Guides a dependency vulnerability audit using each ecosystem's **native, authoritative** tooling and helps triage the results into a prioritized remediation plan.

## What it provides

- **`/audit-deps`** — detects the ecosystem, runs the right native audit tool, and triages findings.
- **`dependency-audit` skill** — per-ecosystem commands and a severity/reachability triage rubric (progressive disclosure via `reference/`).

## Supported ecosystems and tools

| Ecosystem | Tool | Advisory source |
|-----------|------|-----------------|
| Node.js | `npm audit` / `pnpm audit` / `yarn npm audit` | GitHub Advisory DB |
| Python | `pip-audit` | PyPI + OSV |
| Rust | `cargo audit` | RustSec Advisory DB |
| Go | `govulncheck` | Go vuln DB (with reachability) |

## Principles

- **No fabricated CVE data.** Only advisory IDs, severities, and fixed versions the tools actually emit are reported.
- Audits reflect the advisory databases at run time — wire the same tools into CI for continuous coverage.
- Non-mutating by default; dependency upgrades happen only with your consent.

## License

MIT — Matthews Wong
