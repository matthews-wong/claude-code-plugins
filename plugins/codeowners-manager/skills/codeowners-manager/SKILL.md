---
name: codeowners-manager
description: Scaffold and validate GitHub CODEOWNERS files — map path patterns to owning teams and ensure critical paths are covered. Use when creating, editing, or reviewing a CODEOWNERS file, setting up code-review ownership, or checking that sensitive paths have required reviewers. Triggers on "CODEOWNERS", "code owners", "who owns this path", "required reviewers", "ownership rules".
---

# CODEOWNERS Manager

Build and check GitHub CODEOWNERS files. The golden rule: **the last matching pattern wins** — order general-to-specific, not the reverse.

## Valid locations

GitHub reads CODEOWNERS from (first found wins): `.github/CODEOWNERS`, root `/CODEOWNERS`, or `/docs/CODEOWNERS`. Only one is used.

## Syntax essentials

- One rule per line: `<pattern>  <owner> [<owner>...]`.
- Patterns follow gitignore-style globs: `*`, `**`, leading `/` anchors to root, trailing `/` matches a directory.
- Owners are `@username`, `@org/team`, or an email tied to a GitHub account. Teams must have write access and be visible to the repo.
- `#` starts a comment. Blank lines ignored.
- A pattern with **no owner** removes ownership for that path — usually a mistake unless intentional.

Example:
```
# General
*                       @acme/maintainers
# More specific overrides (must come AFTER the general rule)
/src/auth/**            @acme/security
/.github/workflows/     @acme/platform
/CODEOWNERS             @acme/security
```

## Critical paths that should always be owned

Auth/identity, security config, `/.github/workflows/` (CI/CD), infra/IaC (Terraform, k8s, Helm), dependency manifests (package.json, requirements, go.mod, Cargo.toml), DB migrations, secrets/env templates, and the CODEOWNERS file itself. Load `reference/codeowners-syntax.md` for the full critical-path checklist and pattern recipes.

## Validation checklist (quick)

1. File is in a valid location.
2. Every rule has at least one owner (unless intentionally clearing).
3. No rule is fully shadowed by a later, broader match.
4. All critical paths resolve to an owner.
5. Patterns actually match files present in the repo (flag dead patterns).

## Going deeper

Full pattern-matching rules, ordering pitfalls, common recipes, and the complete critical-path list are in `reference/codeowners-syntax.md`. Load it when scaffolding a real file or debugging match behavior.
