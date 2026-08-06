---
name: db-migration-safety
description: Use when reviewing or writing a "database migration" or "schema change" — triggers on "ALTER TABLE", "zero-downtime migration", "add column", "drop column", "rename column", "add index", "backfill", "expand-contract", or when a migration file (Rails/Alembic/Flyway/Liquibase/Prisma/Django/golang-migrate) is shown. Flags locking, downtime, and compatibility risks and rewrites the migration into safe phased steps.
---

# Database Migration Safety Review

Review a schema migration for **zero-downtime, backward-compatible** deployment. Assume the app runs in rolling deploy: old and new code execute simultaneously against the same schema. A migration is safe only if it works for both.

## Method

1. **Identify the operations.** List each DDL/DML statement and the table + approximate row count if known.
2. **Classify risk** using `reference/operation-risks.md`: locking behavior, whether it breaks old or new code, and engine-specific gotchas (Postgres vs MySQL differ significantly).
3. **Check the golden rules** below.
4. **Rewrite unsafe migrations** into the expand-contract phases (see `reference/expand-contract.md`), splitting across deploys where required.
5. **Report**: table of Statement | Risk | Why | Safe alternative, then the phased plan.

## Golden rules

1. **Expand-contract, never in-place breaking changes.** Add the new shape (expand), migrate reads/writes in code, then remove the old shape (contract) in a *later* deploy. Never drop or rename a column/table that current code still references.
2. **Additive first, destructive last.** New columns/tables/indexes are safe to add early; drops and NOT-NULL-without-default happen only after all code paths stop using the old shape.
3. **Add columns nullable (or with a safe default), then backfill.** On Postgres, adding a column with a non-volatile constant default is fast (metadata-only, 11+); a volatile default or older engines rewrite the table. Backfill in **batches**, not one giant `UPDATE`.
4. **Add NOT NULL in two steps.** Add nullable → backfill → add a validated `CHECK (col IS NOT NULL)` (Postgres: `NOT VALID` then `VALIDATE CONSTRAINT`) → optionally set NOT NULL. Avoid a single `ALTER ... SET NOT NULL` that scans/locks the whole table.
5. **Create indexes concurrently.** Postgres: `CREATE INDEX CONCURRENTLY` (outside a transaction). MySQL/InnoDB: most index adds are online (`ALGORITHM=INPLACE, LOCK=NONE`) — verify. A plain `CREATE INDEX` can lock writes on large tables.
6. **Avoid long-held locks.** Keep transactions short; set a `lock_timeout` / `statement_timeout` so a blocked `ALTER` fails fast instead of queueing behind it and freezing the table. Beware `ALTER TABLE` that forces a full rewrite.
7. **Rename via add-copy-drop, never `RENAME`.** A direct rename breaks old code instantly. Add the new column, dual-write, backfill, switch reads, then drop the old one later.
8. **Every migration is reversible or has a tested recovery.** Provide a `down`/rollback, or document why forward-only with a recovery plan.
9. **Foreign keys & constraints: add NOT VALID, then VALIDATE.** Adding a validated FK/constraint locks and scans; split it.
10. **Separate schema change from data change from code deploy.** Ship DDL, backfill, and the code that depends on them as distinct, ordered steps.

## Output

Risk table + phased expand-contract plan + rewritten migration statements. State assumptions (engine, version, table size) explicitly; ask nothing — flag unknowns as caveats. Do not fabricate row counts, lock durations, or benchmark numbers.

## References

- `reference/expand-contract.md` — the full pattern with worked column-rename and add-NOT-NULL sequences.
- `reference/operation-risks.md` — per-operation risk table for Postgres and MySQL.
