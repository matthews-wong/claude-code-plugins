---
name: conventional-commits
description: The Conventional Commits v1.0.0 grammar. Use when writing, formatting, or validating a git commit message so it declares type, optional scope, description, body, and breaking-change footer correctly.
---

# Conventional Commits

A commit message MUST follow this structure:

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Rules

- **type** — one of: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`,
  `test`, `build`, `ci`, `chore`, `revert`. `feat` and `fix` map to semver
  minor and patch respectively.
- **scope** — optional noun in parentheses naming the affected area, e.g.
  `feat(auth):`.
- **description** — imperative mood, lower-case start, no trailing period,
  ideally <= 72 characters.
- **body** — optional, separated by one blank line; explains *why* and *what*.
- **breaking change** — signal with a `!` before the colon
  (`feat(api)!: ...`) and/or a `BREAKING CHANGE: <detail>` footer. Either
  triggers a semver major bump.
- **footers** — `Token: value` or `Token #value` (e.g. `Refs: #123`,
  `Reviewed-by: name`). `BREAKING CHANGE` is the only multi-word token.

## Examples

```
feat(parser): add array literal support
fix: prevent race condition on token refresh
refactor(store)!: drop deprecated sync API

BREAKING CHANGE: syncNow() is removed; use flush() instead.
```

See `reference/spec-details.md` for edge cases, revert format, and validation
regex. See `reference/type-guide.md` for choosing the right type.
