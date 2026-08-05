# SBOM concepts

## Formats

### CycloneDX (OWASP)
- Security- and supply-chain-focused. JSON or XML.
- Rich support for: dependency graph, vulnerabilities, VEX (exploitability statements), services, and cryptographic/ML-BOM extensions.
- Widely used when the primary consumer is security tooling.

### SPDX (Linux Foundation)
- Standardized as ISO/IEC 5962:2021. Tag-value, JSON, YAML, RDF.
- Strong license/compliance heritage; common in legal, procurement, and OSS distribution.
- SPDX license identifiers give precise, canonical license naming.

Both are legitimate and interoperable in spirit; converters exist. Many enterprises emit both.

## NTIA minimum elements

US guidance (NTIA, following EO 14028) defines minimum SBOM data fields:
- Supplier name
- Component name
- Version of the component
- Other unique identifiers (e.g. PURL, CPE)
- Dependency relationship
- Author of the SBOM data
- Timestamp

Plus practices: automation-friendly format, and support for regular updates.

## Package URL (PURL)

A PURL is a compact, ecosystem-aware identifier, e.g.:
`pkg:npm/lodash@4.17.21`, `pkg:pypi/requests@2.31.0`, `pkg:cargo/serde@1.0.197`, `pkg:golang/golang.org/x/text@v0.14.0`.
PURLs make components matchable across SBOMs and vulnerability databases (OSV keys on them).

## VEX (Vulnerability Exploitability eXchange)

VEX statements say whether a product is actually affected by a vulnerability present in a component (e.g. "not affected — vulnerable code not reachable"). CycloneDX can embed VEX. It reduces noise when correlating SBOMs to CVE feeds.

## Why enterprises require SBOMs

- **Regulatory / contractual**: US EO 14028 and downstream federal procurement expectations; sectoral rules (medical devices/FDA, automotive, finance) increasingly mandate SBOMs from suppliers.
- **Incident response**: fast blast-radius answers when a new critical CVE appears.
- **Third-party risk / M&A due diligence**: buyers demand a component inventory.
- **License governance**: obligations tracked across the full tree.

## Source SBOM vs artifact SBOM

- **Source/lockfile SBOM**: what your project declares — reproducible, good for policy.
- **Built artifact / container image SBOM**: what actually ships, including OS packages and bundled binaries — good for runtime risk.
Generate the one that matches the question; often produce both.
