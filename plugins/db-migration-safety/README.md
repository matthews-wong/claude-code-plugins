# db-migration-safety

A skill-first Claude Code plugin that reviews **database schema migrations for zero-downtime safety**.

## What it does
Auto-invokes on "database migration", "schema change", "ALTER TABLE", "zero-downtime migration", or when a migration file is shown. It flags locking, downtime, and backward-compatibility risks, then rewrites the migration into safe expand-contract phases: additive-first, nullable-then-backfill, concurrent index creation, and no destructive drops before deploy.

## Structure
- `skills/db-migration-safety/SKILL.md` — method and the golden rules.
- `skills/db-migration-safety/reference/expand-contract.md` — the parallel-change pattern with worked rename and add-NOT-NULL sequences.
- `skills/db-migration-safety/reference/operation-risks.md` — per-operation risk table for PostgreSQL and MySQL, plus tool-specific tips.

## Usage
Paste a migration (Rails/Alembic/Flyway/Liquibase/Prisma/Django/golang-migrate or raw SQL) and ask whether it is safe to deploy. The skill activates automatically.

## Note
Engine/version behavior differs; the skill states assumptions and does not fabricate lock durations or benchmarks.

## License
MIT © Matthews Wong
