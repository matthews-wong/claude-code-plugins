# Changelog

All notable changes to this marketplace are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.0] — 2026-08

### Added
- **6 auto-invocable language & stack skills**: `javascript-standards`, `typescript-typing`, `react-patterns`, `css-responsive`, `rest-api-design`, `node-backend-patterns` — they fire automatically when you write or review matching code.
- A **"How to use"** section in the README: install, the four ways a plugin runs (skill auto-invoke / slash / subagent / hook), how to confirm a skill is firing, and how to manage plugins.

### Changed
- Marketplace now ships **59 plugins**; bumped to `2.4.0`.

## [2.3.0] — 2026-08

### Added
- **5 enterprise, auto-invocable skill plugins**: `threat-modeling` (STRIDE), `dockerfile-hardening`, `k8s-security-policy` (Pod Security Standards), `db-migration-safety` (expand-contract), `accessibility-audit` (WCAG 2.2 AA).

### Changed
- **Every plugin is now auto-invocable.** Added a `name:` to skills that lacked one, and gave the 9 command/agent/hook-only plugins a routing skill so Claude pulls them in automatically (not only via slash command).
- Marketplace now ships **53 plugins**; bumped to `2.3.0`.

## [2.2.1] — 2026-08

### Changed
- **Deepened the flagship plugins** with worked, on-demand reference examples (progressive disclosure):
  - `skills-connector` — SKILL.md anatomy, good-vs-bad routing descriptions, an authoring checklist, and a copyable worked example.
  - `context-budget` — a before/after CLAUDE.md transformation, the context-budget token math, and the `/context-audit` checklist.
  - `verify-app` — verification playbooks (web app / HTTP API / CLI / worker) and an evidence-report template.
- **Expanded the Boris Cherny playbook** (`docs/boris-cherny-principles.md`) with insights from his Feb 2026 Lenny's Podcast and Pragmatic Engineer interviews.

## [2.2.0] — 2026-08

### Added
- **5 workflow-pattern plugins** packaged from the official Claude Code best-practices guide: `verify-app` (e2e-verification subagent), `spec-writer` (interview → SPEC.md), `writer-reviewer` (fresh-context adversarial review), `context-cleaner` (`/clear` hygiene), and `fan-out-migrate` (headless fan-out migrations).
- **Docs index** (`docs/README.md`) and a **quickstart** (`examples/quickstart.md`) with suggested plugin bundles by goal.

### Changed
- Marketplace now ships **48 plugins**; bumped to `2.2.0`.

## [2.1.0] — 2026-08

### Added
- **3 plugins modeled on Boris Cherny's documented workflow**: `code-simplifier` (his own subagent), `mistake-logger` (the preserve-mistakes loop), and `senior-standards` (his three engineering principles).
- **Research doc** `docs/boris-cherny-principles.md` — how Claude Code's creator uses it, with each plugin mapped to a practice, heavily sourced.

### Changed
- Marketplace now ships **43 plugins**; bumped to `2.1.0`.
- Refined the original 20 plugins with sharper routing descriptions and fixed hook `matcher` fields to the correct string form.

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
