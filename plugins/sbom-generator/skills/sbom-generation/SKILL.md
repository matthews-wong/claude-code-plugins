---
name: sbom-generation
description: Generate a Software Bill of Materials (CycloneDX or SPDX) with standard tools (syft, cdxgen, ecosystem-native generators), pick the right format, and validate the result. Use when producing an SBOM or explaining SBOM requirements.
---

# SBOM generation

A Software Bill of Materials (SBOM) is a formal, machine-readable inventory of every component and dependency in a piece of software, with versions and (often) licenses and suppliers. Generate it with real tooling — never hand-author component data.

## What an SBOM is and why enterprises need it

An SBOM answers "what is actually in this software?" It enables:
- **Vulnerability response** — when a new CVE lands (e.g. a Log4j-class event), correlate it against SBOMs to find exposure fast.
- **License/compliance** — inventory obligations across the dependency tree.
- **Supply-chain integrity** — provenance, and a basis for attestation/signing.
- **Procurement & regulation** — US EO 14028 and NTIA minimum-elements guidance, and sector rules, increasingly require SBOMs from vendors.

See `reference/concepts.md` for formats, minimum elements, and PURLs.

## Workflow

1. Pick a format (CycloneDX vs SPDX) — see `reference/concepts.md`.
2. Pick a generator suited to the project — see `reference/tools.md`.
3. Generate from lockfiles/source for reproducibility (and/or from the built image for what actually ships).
4. Validate the output — see `reference/tools.md` (validation section).
5. Attach the SBOM to the release and regenerate every build; an SBOM is a point-in-time snapshot.

## Format one-liner

- **CycloneDX** (OWASP): security/supply-chain oriented; rich vuln + dependency-graph + VEX support.
- **SPDX** (Linux Foundation / ISO/IEC 5962): license/compliance oriented; long-standing in legal and procurement.

Both are valid; many orgs produce both. Choose by primary consumer.

## Honesty rules

- Drive a real generator; report the tool, command, and spec version used.
- Do not fabricate component lists, hashes, or PURLs.
- Distinguish "SBOM of the source tree" from "SBOM of the built artifact/image" — they can differ.

## References (load on demand)

- `reference/concepts.md` — formats, NTIA minimum elements, PURL, VEX, regulation.
- `reference/tools.md` — generator commands and validation.
