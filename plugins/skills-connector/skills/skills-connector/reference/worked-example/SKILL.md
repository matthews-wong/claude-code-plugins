---
name: Conventional Commit Writer
description: Use when writing a git commit message or rewriting one that was rejected —
  produces Conventional Commits (type(scope): summary) in the imperative mood with a
  50-character subject cap, an optional wrapped body explaining why, and BREAKING CHANGE and
  issue-reference footers. Fires on "commit message", "write a commit", "conventional
  commit", or a commitlint failure.
---

# Conventional Commit Writer

Turn a described or staged change into a well-formed Conventional Commit.

## Procedure

1. **Determine the type** from the change (see the full list in
   `reference/commit-types.md`). The common ones: `feat`, `fix`, `docs`, `refactor`,
   `test`, `chore`.
2. **Add a scope** in parentheses when it sharpens the message — the affected package,
   module, or area, e.g. `feat(auth):`. Omit it rather than invent one.
3. **Write the subject** as `type(scope): summary`:
   - Imperative mood — "add", not "added" or "adds".
   - No trailing period.
   - **50 characters or fewer**, including the `type(scope): ` prefix.
4. **Add a body only when the change needs a "why"** — the motivation or the trade-off, not
   a restatement of the diff. Separate it from the subject with a blank line and wrap lines
   at 72 characters.
5. **Add footers** when relevant:
   - `BREAKING CHANGE: <what broke and the migration>` for incompatible changes.
   - `Refs: #123` / `Closes: #123` to link issues.

## Rules

- Never exceed 50 characters in the subject line.
- Never use past tense or a gerund in the subject — imperative only.
- Never pad the body with a bullet-by-bullet retelling of the diff; explain intent.
- One logical change per commit — if the subject needs "and", the commit should be split.

## Examples

```
feat(auth): add refresh-token rotation

Access tokens now rotate on every refresh so a leaked token is valid
for at most one cycle. Old tokens are revoked server-side.

Closes: #482
```

```
fix(parser): handle empty input without throwing
```

For the complete type list with when-to-use guidance, see
`reference/commit-types.md`.
