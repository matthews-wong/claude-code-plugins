# The Expand-Contract (Parallel Change) Pattern

The core technique for evolving a schema with zero downtime while old and new code run side by side.

## The three phases

1. **Expand** — add the new schema shape *additively*. It must not break existing code. New columns are nullable or defaulted; new tables/indexes are created concurrently. Ship this, then deploy code that can read the old shape but writes both (dual-write) or reads new-or-old.
2. **Migrate** — backfill existing data into the new shape in batches; move all readers to the new shape; ensure no code path depends on the old shape.
3. **Contract** — in a *later* deploy, remove the old shape (drop column/table/constraint) now that nothing references it.

Each phase is a separate, independently deployable and revertible step. Never collapse expand and contract into one migration.

## Worked example: rename `email` → `email_address`

A direct `ALTER TABLE users RENAME COLUMN email TO email_address` breaks every running instance of the old code the instant it commits. Do this instead:

**Deploy 1 (expand):**
```sql
ALTER TABLE users ADD COLUMN email_address text;  -- nullable, fast
```
Deploy code that writes BOTH `email` and `email_address`, reads `email` (or coalesces).

**Deploy 2 (migrate):** backfill in batches:
```sql
-- repeat until no rows updated; keep each batch small to avoid long locks
UPDATE users
SET email_address = email
WHERE email_address IS NULL AND id IN (
  SELECT id FROM users WHERE email_address IS NULL LIMIT 5000
);
```
Then deploy code that reads `email_address` and still dual-writes.

**Deploy 3 (migrate → constraint):** once backfill is complete and verified:
```sql
ALTER TABLE users ADD CONSTRAINT email_address_not_null
  CHECK (email_address IS NOT NULL) NOT VALID;      -- fast, no scan
ALTER TABLE users VALIDATE CONSTRAINT email_address_not_null; -- scans without heavy lock
```
Deploy code that reads AND writes only `email_address` (stop touching `email`).

**Deploy 4 (contract):**
```sql
ALTER TABLE users DROP COLUMN email;
```

## Worked example: add a NOT NULL column safely

Bad (rewrites/locks on large tables or old engines, and breaks inserts from old code):
```sql
ALTER TABLE orders ADD COLUMN status text NOT NULL;  -- risky
```

Safe sequence:
```sql
-- Deploy 1: add nullable with a safe constant default (metadata-only on PG 11+)
ALTER TABLE orders ADD COLUMN status text DEFAULT 'pending';
-- Deploy 2: backfill any rows the default didn't cover, in batches
-- Deploy 3: enforce NOT NULL without a blocking full-table scan
ALTER TABLE orders ADD CONSTRAINT orders_status_nn CHECK (status IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_nn;
-- Optional later: ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
```

## Backfill guidance

- Batch by primary key range or `LIMIT`; sleep briefly between batches to spare replication lag and locks.
- Run backfills outside the migration transaction where the tool allows (Rails `disable_ddl_transaction!`, Alembic autocommit block).
- Make backfills idempotent and resumable (guard with `WHERE new_col IS NULL`).
- Monitor replica lag; throttle if it grows.

## Rollback thinking

- Expand steps are trivially reversible (drop the thing you added) *only* while no code depends on them.
- Once code depends on the new shape, rolling back the code is the safer lever than reversing the data migration.
- Contract steps are effectively irreversible (data loss) — gate them behind confidence that the new shape is fully adopted, and keep a backup.
