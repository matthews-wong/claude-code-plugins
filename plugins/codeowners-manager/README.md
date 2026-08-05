# codeowners-manager

Claude Code plugin to scaffold and validate a GitHub **CODEOWNERS** file — mapping path patterns to owning teams and ensuring critical paths (auth, CI/CD, infra, dependencies, migrations) always have an owner.

## Components

- **`/codeowners [scaffold|validate]`** — scaffolds a new CODEOWNERS file from the repo structure, or validates an existing one for syntax, ordering, coverage, and dead patterns. Auto-detects mode when no argument is given.
- **`codeowners-manager` skill** — auto-triggers when you work on CODEOWNERS or code-review ownership. Lean rules inline; full pattern semantics, ordering pitfalls, recipes, and the critical-path checklist load from `reference/codeowners-syntax.md` (progressive disclosure).

## Usage

```
/codeowners scaffold
/codeowners validate
```

## Notes

Enforces the GitHub "last matching pattern wins" rule and flags shadowed rules — the most common CODEOWNERS bug. Never invents team handles; unknown owners become explicit `# TODO: assign owner` placeholders.

MIT licensed. Author: Matthews Wong.
