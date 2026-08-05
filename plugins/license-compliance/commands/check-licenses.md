---
name: check-licenses
description: Inventory dependency licenses, normalize them to SPDX identifiers, and flag any that fall outside the project's allowlist.
---

You are helping the user build a license inventory of their dependencies and flag anything that conflicts with their licensing policy. Legal risk is involved — be careful, cite the actual declared license, and recommend counsel for genuine legal questions rather than giving a legal opinion.

## What to do

1. Detect the ecosystem(s) and choose a real license-inventory tool:
   - Node.js: `license-checker` / `license-checker-rseidelsohn`, or `npx license-report`.
   - Python: `pip-licenses`.
   - Rust: `cargo-license` or `cargo-deny check licenses`.
   - Go: `go-licenses report ./...`.
   - Cross-ecosystem: derive from an SBOM (see the `sbom-generator` plugin) — CycloneDX/SPDX components carry license fields.
2. Load the `license-compliance` skill for SPDX explanation, the allowlist/denylist model, and copyleft categories.
3. Produce an inventory: for each dependency, name, version, and its declared license normalized to an SPDX identifier where possible. Mark `UNKNOWN` where the license cannot be determined — do not guess.
4. Compare against the policy allowlist. If the project has no explicit policy, propose a sensible default (permissive-allow, strong-copyleft-flag) and make the assumption explicit.
5. Flag conflicts by risk: strong copyleft (GPL/AGPL) in a proprietary/distributed context, network-copyleft (AGPL) for SaaS, unknown/missing licenses, and license incompatibilities.

## How to report

Give a summary table (counts per license family), then a flagged list with dependency, license, why it's flagged, and options (replace, isolate, obtain a commercial license, or accept with sign-off). State clearly that this is an engineering inventory to support a compliance decision, not legal advice, and that declared metadata can differ from the actual license text — verify high-risk items against the source.
