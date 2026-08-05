# Skill anatomy — the exact structure of a SKILL.md

A skill is a directory whose name is the skill's identity, containing a `SKILL.md` and,
optionally, bundled files it points to.

```
skills/
  <skill-name>/          # kebab-case; this name is the skill's identity
    SKILL.md             # REQUIRED — frontmatter + instruction body
    reference/           # optional — deeper docs, loaded on demand
    scripts/             # optional — helper scripts the skill can run
    assets/              # optional — templates, data files, images
```

The bundled folder names (`reference/`, `scripts/`, `assets/`) are conventions, not
keywords. What makes a file "load on demand" is that the body mentions it by relative path;
nothing loads a bundled file until Claude reads that pointer and decides it needs it.

## Frontmatter

The frontmatter is YAML between two `---` fences at the very top of the file.

| Field         | Required | Purpose |
|---------------|----------|---------|
| `description` | **Yes**  | The routing signal — what the skill does AND when to use it. This is the only text Claude sees before deciding to load the skill. |
| `name`        | No       | Human/display name. Defaults to the folder name if omitted. Keep it aligned with the folder. |

Keep the frontmatter minimal. `description` does the routing work; see
`../descriptions.md` for how to write one that fires.

## Body

Everything after the closing `---` is the instruction body. It is loaded **only after** the
skill triggers, so it can be as detailed as the capability needs — but stay lean and push
depth into `reference/`. Lead with the highest-value procedure, use imperative headings and
short lists, and state hard rules (must/never) explicitly.

## Minimal correct example

The smallest thing that is still a valid, well-routed skill:

```markdown
---
description: Use when writing or editing a git commit message — enforces Conventional
  Commits (type(scope): summary), imperative mood, and a 50-character subject cap.
---

# Commit message writer

1. Pick a type: feat, fix, docs, refactor, test, chore.
2. Format the subject as `type(scope): summary` in the imperative mood, under 50 chars.
3. Add a body only when the change needs a "why"; wrap at 72 chars.
```

## Fuller example (with bundled reference)

When the guidance outgrows a screen, split the depth into a `reference/` file and point to
it from the body:

```markdown
---
name: SQL Migrations
description: Use when writing, ordering, or reviewing Postgres schema migrations — covers
  safe column drops, backfills, index creation without downtime, and migration ordering.
---

# SQL migrations

## Procedure
1. Write the migration as an idempotent, reversible step where possible.
2. For a destructive change (drop column/table), stage it: deploy code that stops using it,
   then drop in a later migration.
3. Create indexes with `CREATE INDEX CONCURRENTLY` to avoid table locks.

## Rules
- Never drop and re-add a column in one migration to "rename" it — use `ALTER ... RENAME`.
- Never run a long backfill inside the same transaction as a DDL change.

## Deep reference
For lock-severity by statement and the online-migration playbook, see
`reference/online-migrations.md`.
```

Directory for that skill:

```
skills/
  sql-migrations/
    SKILL.md
    reference/
      online-migrations.md
```

## Checklist for the structure

- [ ] Folder is kebab-case and names the capability.
- [ ] `SKILL.md` exists with valid YAML frontmatter (`---` … `---`).
- [ ] `description` present and written as a trigger (see `../descriptions.md`).
- [ ] Body leads with the procedure; depth pushed into `reference/`.
- [ ] Every bundled file is pointed to from the body by relative path.
