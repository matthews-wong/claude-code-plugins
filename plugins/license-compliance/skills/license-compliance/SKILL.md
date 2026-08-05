---
name: license-compliance
description: Inventory dependency licenses, normalize to SPDX identifiers, and flag licenses outside an allowlist (e.g. GPL/AGPL copyleft in proprietary code). Use when checking open-source license obligations or building a license inventory.
---

# License compliance

Build a dependency license inventory, express licenses as SPDX identifiers, and flag ones that conflict with the project's licensing policy. This supports a compliance decision — it is not legal advice.

## Workflow

1. Inventory licenses with a real per-ecosystem tool (see `reference/tools.md`).
2. Normalize each to an SPDX identifier; mark truly unknown ones `UNKNOWN` (never guess).
3. Classify by obligation family (permissive / weak copyleft / strong copyleft / network copyleft / proprietary / unknown).
4. Compare against the allowlist/denylist policy.
5. Flag conflicts with options and required sign-offs.

## SPDX in one line

SPDX (Software Package Data Exchange) is an ISO/IEC 5962 standard; **SPDX license identifiers** are short, unambiguous strings — `MIT`, `Apache-2.0`, `GPL-3.0-only`, `AGPL-3.0-or-later` — that name a license precisely and can be combined with expressions like `(MIT OR Apache-2.0)`. See `reference/spdx.md`.

## Obligation families (why licenses get flagged)

- **Permissive** (MIT, BSD-2/3, Apache-2.0, ISC): usually allowlisted; Apache-2.0 adds a patent grant + NOTICE handling.
- **Weak copyleft** (LGPL, MPL-2.0, EPL): file/library-level reciprocity; often allowed with dynamic linking care.
- **Strong copyleft** (GPL-2.0, GPL-3.0): distributing a combined work can require releasing your source under the GPL — high risk in proprietary distributed software.
- **Network copyleft** (AGPL-3.0): the copyleft trigger extends to network/SaaS use — high risk for hosted services even without distributing binaries.
- **Unknown / missing / custom**: treat as blocking until resolved.

Full policy model and default allowlist in `reference/policy.md`.

## Honesty rules

- Report the actually declared license; if metadata and LICENSE file disagree, flag it and prefer verifying the source text for high-risk items.
- Do not render legal conclusions; recommend counsel for genuine legal questions.

## References (load on demand)

- `reference/spdx.md` — SPDX identifiers and expression syntax.
- `reference/tools.md` — per-ecosystem license inventory tools.
- `reference/policy.md` — allowlist/denylist model and a default policy.
