# CHANGELOG.md Format

## File skeleton

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- ...

### Fixed
- ...

## [1.2.0] - 2026-07-01

### Added
- Initial public release.

[Unreleased]: https://example.com/compare/v1.2.0...HEAD
[1.2.0]: https://example.com/releases/tag/v1.2.0
```

## Rules

- Only include category subsections (`### Added`, etc.) that have entries.
- Keep releases in reverse-chronological order; `Unreleased` is always first.
- Each released heading is `## [X.Y.Z] - YYYY-MM-DD`.

## Promoting Unreleased to a release (done at release time)

1. Rename `## [Unreleased]` to `## [X.Y.Z] - <today>`.
2. Add a fresh empty `## [Unreleased]` above it.
3. Update the comparison links at the bottom so `Unreleased` compares from the
   new tag and a new `[X.Y.Z]` link is added.

The `/update-changelog` command only fills the `Unreleased` section; promotion
is performed by the release process.
