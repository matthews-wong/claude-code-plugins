# Changelog

All notable changes to this marketplace are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2026-08

### Added
- **20 enterprise-ready plugins** across five new categories:
  - **Security & compliance** — `secret-scanner`, `dependency-auditor`, `license-compliance`, `sbom-generator`, `data-classification`, `compliance-checklist`, `access-review`
  - **Governance & standards** — `pr-governance`, `conventional-commits`, `adr-manager`, `changelog-generator`, `release-manager`, `codeowners-manager`, `standards-enforcer`
  - **Quality & reliability** — `test-coverage-gate`, `api-contract-guard`, `docs-guardian`, `incident-runbook`, `terraform-policy`
  - **Context engineering** — `context-budget` (flagship)
- **Research docs**: `docs/writing-good-plugins.md` and `docs/lean-structured-context.md`.
- **Marketplace validation**: `scripts/validate_marketplace.py` + a `validate-marketplace` GitHub Actions workflow.
- Enterprise plugins apply **progressive disclosure**: lean `SKILL.md` files with heavier detail deferred to `reference/*.md`.

### Changed
- Marketplace now ships **40 plugins** (was 20); bumped to `2.0.0`.
- Expanded the README with enterprise sections and a research/guides section.

## [1.0.0] — 2026-08

### Added
- Initial marketplace: **20 plugins** for agentic workflows, organized around
  Boris Cherny's five stages of AI adoption (verification, permissions, context,
  orchestration, governance).
