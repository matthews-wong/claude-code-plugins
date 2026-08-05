# License inventory tools

Use a real inventory tool per ecosystem. These read declared package metadata; for high-risk findings, verify against the actual LICENSE text.

## Node.js

- `npx license-checker-rseidelsohn --summary` — counts by license.
- `npx license-checker-rseidelsohn --json` — full per-package detail.
- `npx license-report` — alternative reporter.
- Options typically support `--onlyAllow` / `--failOn` to enforce a policy in CI.

## Python

- Install: `pipx install pip-licenses`.
- `pip-licenses --format=markdown --with-authors --with-urls`
- `pip-licenses --format=json`
- `pip-licenses --allow-only="MIT;BSD;Apache 2.0;ISC"` to enforce an allowlist (note: matches names, normalize to SPDX yourself).

## Rust

- `cargo install cargo-license` then `cargo license` (or `--json`).
- `cargo-deny`: `cargo deny check licenses` — policy-driven allow/deny in `deny.toml`, SPDX-aware. Preferred for enforcement.

## Go

- Install: `go install github.com/google/go-licenses@latest`.
- `go-licenses report ./...` — per-module licenses.
- `go-licenses check ./...` — fail on disallowed license types.

## Cross-ecosystem via SBOM

If you already generate an SBOM (see the `sbom-generator` plugin), CycloneDX and SPDX documents carry `licenses`/`licenseConcluded` fields per component. Tools like `cyclonedx` and `syft` can emit license data directly, giving one inventory across all ecosystems.

## Caveats

- Declared metadata can be wrong or missing (`UNKNOWN` / `NOASSERTION`).
- A monorepo may mix ecosystems — run each relevant tool.
- Enforcement in CI (fail the build on a denied license) is where this becomes a real control.
