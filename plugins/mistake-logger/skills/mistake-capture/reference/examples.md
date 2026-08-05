# Worked examples: mistake → durable rule

Each example shows the raw incident and the captured lesson, with the destination choice.

## Example 1 — wrong package manager (→ CLAUDE.md line)

**Incident:** Claude ran `npm install`; the repo uses pnpm and the lockfile broke.

**Captured (project `CLAUDE.md`, under a Tooling heading):**

```
- Use pnpm for all installs and scripts; never npm or yarn (pnpm-lock.yaml is the source of truth).
```

One fact, always relevant → a single CLAUDE.md line.

## Example 2 — skipped the migration guard (→ CLAUDE.md line)

**Incident:** Claude deployed with `--force`, which silently skipped the migration safety check.

**Captured:**

```
- Never pass --force to deploy.sh without user confirmation; it skips the migration guard.
```

## Example 3 — reinvented the migration flow (→ skill)

**Incident:** Claude hand-wrote a migration file in the wrong directory and forgot to register it, because the project has a specific multi-step flow.

**Captured** as `.claude/skills/add-migration/SKILL.md`:

```markdown
---
name: add-migration
description: Use when adding or modifying a database migration in this repo. Triggers on "new migration", "alter table", "schema change", "migrate".
---

# Add a database migration

## Steps
1. Generate the file: `pnpm db:new <name>` (creates it in `db/migrations/` with the right timestamp prefix).
2. Write `up` and `down`; both must be reversible.
3. Register it in `db/migrations/index.ts`.
4. Apply locally with `pnpm db:migrate` and verify with `pnpm db:status`.

## Gotchas
- Do not create the file by hand — the timestamp prefix must be generated or the runner ignores it.
```

A procedure with ordering and gotchas → a skill, not a CLAUDE.md paragraph.

## The test

If you're tempted to write more than one line into CLAUDE.md, it's probably a procedure — make a skill instead.
