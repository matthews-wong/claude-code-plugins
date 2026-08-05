# Choosing a Commit Type

| Type | Use when | Semver |
|------|----------|--------|
| `feat` | Adds user-facing capability | minor |
| `fix` | Corrects a bug | patch |
| `docs` | Documentation only | none |
| `style` | Formatting, whitespace, no logic change | none |
| `refactor` | Restructure without behavior change | none |
| `perf` | Performance improvement | patch |
| `test` | Adds or fixes tests only | none |
| `build` | Build system or dependency changes | none |
| `ci` | CI configuration and scripts | none |
| `chore` | Maintenance not touching src or tests | none |
| `revert` | Reverts a previous commit | context |

## Tie-breakers

- Behavior visible to a user or API consumer? Prefer `feat` or `fix` over
  `chore`/`refactor`.
- Touches both code and its tests for one feature? Use the code type (`feat`
  or `fix`); the tests ride along.
- Dependency bump that fixes a security issue affecting users? `fix` with a
  note, not `build`.
