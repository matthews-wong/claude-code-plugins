# Per-Operation Migration Risk Reference

Behavior varies by engine and version. Verify against your exact version; the notes below reflect common modern defaults (Postgres 12+ / MySQL 8+ InnoDB). Do not assume — when version is unknown, flag it as a caveat.

## PostgreSQL

| Operation | Lock / cost | Breaks old code? | Safe approach |
|---|---|---|---|
| ADD COLUMN nullable, no default | Metadata-only, fast | No | Safe as-is. |
| ADD COLUMN with constant default | Metadata-only on PG 11+ | No | Safe. Volatile default (e.g. `now()` per row) rewrites table — avoid. |
| ADD COLUMN NOT NULL no default | Rewrite + AccessExclusive | Yes (old inserts fail) | Add nullable → backfill → CHECK NOT VALID → VALIDATE. |
| DROP COLUMN | Fast (metadata) but breaks code | Yes if referenced | Contract phase only, after code stops using it. |
| RENAME COLUMN/TABLE | Fast but instantly breaks old code | Yes | Add-copy-dual-write-drop (expand-contract). |
| ALTER COLUMN TYPE | Usually full rewrite + lock | Maybe | New column + backfill, or check binary-coercible types. |
| SET NOT NULL | Full scan under AccessExclusive (pre-12) | No | PG12+ can use a validated CHECK to skip the scan. |
| CREATE INDEX | Locks writes for duration | No | `CREATE INDEX CONCURRENTLY` (no txn, can leave INVALID index on failure — drop & retry). |
| ADD FOREIGN KEY | Lock + scan both tables | No | Add `NOT VALID` then `VALIDATE CONSTRAINT` separately. |
| ADD CHECK constraint | Scan under lock | No | `NOT VALID` then `VALIDATE`. |
| ADD UNIQUE constraint | Builds index with lock | No | `CREATE UNIQUE INDEX CONCURRENTLY` then `ADD CONSTRAINT ... USING INDEX`. |

Always set `SET lock_timeout` (and `statement_timeout`) so a blocked DDL fails fast rather than queuing behind a lock and stalling all traffic on that table.

## MySQL (InnoDB, 8.0)

| Operation | Algorithm | Notes |
|---|---|---|
| ADD COLUMN | INSTANT (often, if added at end / 8.0.12+) | Very fast; some positions force INPLACE/COPY. |
| DROP COLUMN | INPLACE, rebuilds | Online but rebuilds table; breaks code if referenced. |
| ADD INDEX | INPLACE, LOCK=NONE | Generally online; verify with `ALGORITHM=INPLACE, LOCK=NONE`. |
| MODIFY COLUMN type | Often COPY, locks | Prefer add-new-column + backfill for large tables. |
| RENAME COLUMN | INSTANT-ish metadata | Still breaks old code — use expand-contract. |
| ADD FOREIGN KEY | Requires table copy / checks | Consider `foreign_key_checks` implications; do off-peak or via expand-contract. |
| CHANGE NOT NULL | May COPY | Add nullable → backfill → enforce. |

For very large MySQL tables, use an online-schema-change tool (gh-ost, pt-online-schema-change) which builds a shadow table and swaps — avoids the long metadata lock of a native COPY.

## Tool-specific tips

- **Rails**: `disable_ddl_transaction!` + `algorithm: :concurrently` for concurrent indexes; the `strong_migrations` gem catches most of these automatically.
- **Alembic**: use `op.create_index(..., postgresql_concurrently=True)` inside an autocommit block; separate data migrations from schema migrations.
- **Flyway/Liquibase**: keep each phase a separate versioned migration; use `splitStatements` / concurrent index annotations.
- **Prisma/Django/golang-migrate**: generated SQL is often naive — review the emitted DDL for the risky operations above and hand-edit to the safe form.

## Red flags to always call out
- A single migration that both adds AND drops/renames (expand + contract together).
- `NOT NULL` added without a default on a populated table.
- Plain `CREATE INDEX` on a large, write-heavy table.
- `UPDATE`/backfill with no batching (one statement over the whole table).
- Validated FK/CHECK added in one step on large tables.
- Any `DROP` or `RENAME` shipped in the same release as the code that stops using it (no soak time).
