---
name: changelog-maintenance
description: Keep a Changelog maintenance rules. Use when writing or updating CHANGELOG.md to map Conventional Commits into Added/Changed/Deprecated/Removed/Fixed/Security sections under an Unreleased heading.
---

# Changelog Maintenance

Maintain `CHANGELOG.md` in the [Keep a Changelog](https://keepachangelog.com)
1.1.0 format: newest first, one section per release, an `## [Unreleased]`
section at the top for pending changes.

## The six categories

- **Added** — new features.
- **Changed** — changes in existing behavior.
- **Deprecated** — soon-to-be-removed features.
- **Removed** — features removed in this release.
- **Fixed** — bug fixes.
- **Security** — vulnerability fixes.

## Mapping Conventional Commits

| Commit | Category |
|--------|----------|
| `feat` | Added |
| `fix` | Fixed |
| `perf` | Changed |
| `refactor` (user-visible) | Changed |
| any `!` / `BREAKING CHANGE` | Changed (prefix bullet with **BREAKING:**) |
| `revert` | Removed or Fixed (by intent) |
| `docs`, `style`, `test`, `ci`, `build`, `chore` | omit unless user-facing |

Commits removing a feature go under **Removed**; commits marking something for
removal go under **Deprecated**; security fixes go under **Security** even if
typed `fix`.

## Writing entries

- Rewrite commit subjects into user-facing prose. Drop the type prefix.
- One bullet per notable change; merge duplicates.
- Reference issues/PRs in parentheses when known.

See `reference/format.md` for the file skeleton and the released-section
promotion flow used at release time.
