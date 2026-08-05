# standards-enforcer

Claude Code plugin that checks a diff against an **editable org coding-standards profile**: naming, file organization, error handling, no secrets or leftover debug prints, and docstrings on public APIs.

## Components

- **`/enforce-standards [diff range]`** — reviews the current change set (or a git range) against the profile, grades findings by severity (Blocker / Warning / Nit), cites the exact rule, and gives a pass/fail verdict.
- **`standards-enforcer` skill** — auto-triggers on diff/PR convention reviews. Lean summary inline; the enforceable rules live in `reference/standards-profile.md`, which the team edits to tune the org's standards.

## Customizing

Edit `skills/standards-enforcer/reference/standards-profile.md`. Each rule has a stable ID (e.g. `NAME-1`, `ERR-2`) so findings cite it directly. The enforcer only applies rules present in that file.

## Usage

```
/enforce-standards
/enforce-standards origin/main...HEAD
```

## Notes

Reviews only changed lines, prefers the repo's own linter config on conflict, and never invents rules — missing rules are proposed as profile additions.

MIT licensed. Author: Matthews Wong.
