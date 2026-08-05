---
name: codeowners
description: Scaffold a new CODEOWNERS file or validate and improve an existing one, ensuring critical paths have owning teams.
args: "[scaffold|validate] — default: auto-detect (validate if a CODEOWNERS file exists, otherwise scaffold)"
---

Manage the repository's GitHub CODEOWNERS file. Mode: `$ARGUMENTS` (if empty, validate when a CODEOWNERS file already exists, otherwise scaffold a new one).

Load the `codeowners-manager` skill for syntax rules, valid locations, and the critical-path coverage list.

## If scaffolding

1. Explore the repo structure to identify top-level domains (services, packages, apps, infra, docs, CI config).
2. Locate any existing team hints (existing CODEOWNERS, MAINTAINERS, package.json authors, directory naming). Do not invent team names — where an owner is unknown, insert a clearly marked `# TODO: assign owner` placeholder rather than guessing.
3. Propose a CODEOWNERS file with the most-general rules first and the most-specific last (last matching rule wins in GitHub), covering the critical paths from the skill.
4. Write it to a valid location (`.github/CODEOWNERS`, root `CODEOWNERS`, or `docs/CODEOWNERS`), asking before overwriting an existing file.

## If validating

1. Read the existing CODEOWNERS file. Check syntax: valid patterns, `@org/team` or `@user` or email owners, no rule with zero owners (which un-assigns), correct ordering semantics.
2. Verify critical paths are covered — auth, security config, CI/CD workflows, infra/IaC, dependency manifests, migrations, and the CODEOWNERS file itself.
3. Flag: unowned critical paths, unreachable rules shadowed by later ones, patterns that match nothing in the repo, and duplicate/conflicting rules.
4. Output a findings table (Path pattern | Owner | Issue | Fix) and offer to apply corrections.

Report ordering pitfalls explicitly, since GitHub applies the last matching pattern, not the most specific. Do not fabricate team handles; use placeholders when ownership is genuinely unknown.
