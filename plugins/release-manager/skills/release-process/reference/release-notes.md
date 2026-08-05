# Release Notes Template

Draft release notes for `vX.Y.Z` from the promoted changelog section. Keep them
skimmable and honest about breaking changes.

```markdown
## vX.Y.Z — YYYY-MM-DD

<One-sentence summary of the release theme.>

### Highlights
- <Most important change for users>

### Breaking Changes
- <BREAKING: what changed and the migration step> (omit section if none)

### Added
- ...

### Fixed
- ...

### Upgrade notes
- <Steps to upgrade, config changes, deprecations to act on> (omit if none)

**Full changelog:** vA.B.C...vX.Y.Z
```

## Guidance

- Lead with what a user or operator must know, not internal refactors.
- Every breaking change names the migration; never bury it.
- Link the compare range so readers can see the full diff.
- If tests were skipped or an exception was made in pre-flight, say so here.
