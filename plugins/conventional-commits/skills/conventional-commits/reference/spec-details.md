# Conventional Commits — Details

Based on the Conventional Commits v1.0.0 specification.

## Validation regex (header line)

The subject line should match:

```
^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9._-]+\))?(!)?: .+
```

This is the same pattern used by `scripts/check-commit-msg.sh`.

## Breaking changes

- `!` before the colon marks a breaking change and MAY be combined with a
  `BREAKING CHANGE:` footer for detail.
- The footer form is `BREAKING CHANGE:` or `BREAKING-CHANGE:` (both accepted),
  followed by a description of the migration.
- Any breaking marker forces a semver **major** bump regardless of type.

## Reverts

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## Footer grammar

- One footer per line: `Token: value` or `Token #value`.
- Tokens use `-` in place of spaces (`Reviewed-by`), except `BREAKING CHANGE`
  which keeps the space by convention.

## Common mistakes

- Capitalized or past-tense descriptions ("Added", "Fixed") — use imperative.
- Trailing period in the subject.
- Missing blank line between subject and body (breaks `git log` formatting).
- Using `chore` for user-facing changes that deserve `feat` or `fix`.
