# license-compliance

Inventories dependency licenses, normalizes them to **SPDX identifiers**, and flags anything outside your allowlist — for example strong-copyleft (GPL) or network-copyleft (AGPL) licenses in a proprietary or SaaS codebase.

## What it provides

- **`/check-licenses`** — inventories licenses with a real per-ecosystem tool and flags policy conflicts.
- **`license-compliance` skill** — SPDX explanation, inventory tooling, and an allowlist/denylist policy model (progressive disclosure via `reference/`).

## Highlights

- Explains **SPDX** identifiers and expressions (`MIT`, `Apache-2.0`, `GPL-3.0-only`, `(MIT OR Apache-2.0)`).
- Classifies licenses by obligation family: permissive, weak copyleft, strong copyleft, network copyleft, unknown.
- Ships a sensible **default policy** for proprietary/distributed software, with context modifiers for SaaS and on-prem.
- Uses real tools: `license-checker`, `pip-licenses`, `cargo-license` / `cargo-deny`, `go-licenses`.

## Not legal advice

This is an engineering inventory to support a compliance decision. Declared metadata can differ from the actual license text — verify high-risk items against source, and involve counsel for genuine legal questions.

## License

MIT — Matthews Wong
