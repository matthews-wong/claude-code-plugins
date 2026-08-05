---
name: generate-sbom
description: Generate a Software Bill of Materials (CycloneDX or SPDX) for the project using standard tooling and explain the output.
---

You are helping the user generate a Software Bill of Materials (SBOM) for their project using real, standard tooling. Do not hand-write an SBOM or fabricate component data — drive an actual generator so the output is accurate and verifiable.

## What to do

1. Load the `sbom-generation` skill for format selection, tool commands, and validation guidance.
2. Decide the format with the user (or recommend one):
   - **CycloneDX** — security/supply-chain focused, rich vulnerability + dependency-graph support.
   - **SPDX** — license/compliance focused, ISO/IEC 5962 standard, common in legal/procurement.
3. Choose a generator based on what the project is and what is installed:
   - `syft` — broad: scans source dirs, lockfiles, and container images; emits CycloneDX or SPDX.
   - `cdxgen` — CycloneDX-native, strong multi-language support.
   - Ecosystem-native: `npm sbom`, `cyclonedx-npm`, `cyclonedx-py`, `cargo-cyclonedx`.
4. Run the generator against the project (source tree and/or built artifact/image). Ask before installing tools. Prefer scanning lockfiles for reproducibility.
5. Validate the result (well-formed JSON/XML, component count sane, metadata/author/timestamp present) and briefly explain its structure.

## How to report

State the format and spec version, the tool and command used, where the SBOM was written, and a summary (component count, ecosystems covered). Explain at a high level what the SBOM contains and how it will be used downstream (vulnerability correlation, license review, procurement/attestation). Note that an SBOM is a point-in-time snapshot — it should be regenerated on each release and ideally attached to the build/release artifacts.
