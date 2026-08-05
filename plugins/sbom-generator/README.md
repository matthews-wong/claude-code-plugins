# sbom-generator

Produces a **Software Bill of Materials** (CycloneDX or SPDX) for your project using standard tooling, and explains what an SBOM is and why enterprises need one.

## What it provides

- **`/generate-sbom`** — picks a format and generator, runs it against the project, and validates/explains the output.
- **`sbom-generation` skill** — format selection, tool commands, and SBOM concepts (progressive disclosure via `reference/`).

## Formats

- **CycloneDX** (OWASP) — security/supply-chain focused; rich vulnerability, dependency-graph, and VEX support.
- **SPDX** (Linux Foundation, ISO/IEC 5962) — license/compliance focused; common in legal and procurement.

## Tools it drives

`syft`, `cdxgen`, and ecosystem-native generators (`npm sbom`, `cyclonedx-py`, `cargo-cyclonedx`, `cyclonedx-maven-plugin`). It runs a real generator — component data is never hand-authored or fabricated.

## Why it matters

SBOMs power fast vulnerability response, license governance, supply-chain integrity, and satisfy procurement/regulatory expectations (US EO 14028, NTIA minimum elements). An SBOM is a point-in-time snapshot — regenerate on every release and attach it to the build artifacts.

## License

MIT — Matthews Wong
