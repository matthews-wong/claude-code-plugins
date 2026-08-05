# SBOM generation tools

Use a real generator. Report the tool, command, and spec version you actually ran.

## syft (Anchore) — broad, multi-target

Scans source directories, lockfiles, filesystems, and container images. Emits CycloneDX or SPDX.

- `syft dir:. -o cyclonedx-json > sbom.cdx.json`
- `syft dir:. -o spdx-json > sbom.spdx.json`
- `syft <image>:<tag> -o cyclonedx-json` — SBOM of a container image (includes OS packages).
- List formats: `syft --help` (supports `cyclonedx-json`, `cyclonedx-xml`, `spdx-json`, `spdx-tag-value`, `syft-json`).

## cdxgen (CycloneDX project) — CycloneDX-native, multi-language

- `cdxgen -o sbom.cdx.json` — auto-detects languages in the current project.
- `cdxgen -t <type> -o sbom.cdx.json` — hint the project type (e.g. `java`, `python`, `npm`).
- Strong at polyglot/monorepo projects.

## Ecosystem-native generators

- Node.js: `npm sbom --sbom-format cyclonedx` (npm 9+), or `npx @cyclonedx/cyclonedx-npm --output-file sbom.cdx.json`.
- Python: `cyclonedx-py environment` / `cyclonedx-py requirements requirements.txt`.
- Rust: `cargo cyclonedx` (from the `cargo-cyclonedx` crate).
- Java/Maven: `mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom`.
- Go: `syft` is the common path; `cyclonedx-gomod` for Go modules.

## Validation

- CycloneDX: `cyclonedx validate --input-file sbom.cdx.json` (from the `cyclonedx-cli` tool).
- SPDX: `pyspdxtools` / online SPDX validators; check required fields per NTIA minimum elements.
- Sanity checks regardless of tool: well-formed JSON/XML, non-empty component list, plausible count vs the lockfile, metadata author + timestamp present, PURLs populated.

## Practical guidance

- Prefer generating from lockfiles for reproducibility; add an image SBOM for what ships.
- Pin the SBOM to the release (attach as a build artifact / attestation).
- Regenerate on every build — an SBOM is a point-in-time snapshot, not a one-off document.
