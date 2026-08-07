---
name: memory-consolidate
description: Use to tidy the local memory store — merge near-duplicate learnings and forget stale, low-value ones. Run occasionally (or when retrieval feels noisy) to keep the store lean so the most useful lessons keep surfacing.
---

You are running a consolidation / forgetting pass over the learnings store so it stays
lean and the most useful lessons keep surfacing.

Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py consolidate
```

What it does:

- **Merges near-duplicates** across the whole store (TF-IDF cosine ≥ 0.85): the longer
  text is kept, tags are unioned, importance is bumped, and a `semantic` kind wins over
  `episodic` (this also raises confidence — corroboration).
- **Prunes stale, low-value notes** — a note is forgotten when it matches **either**:
  - older than `--max-age-days` (default 365) AND `importance < 1.0` AND never used
    (`access_count == 0`); or
  - `confidence < 0.3` AND never used AND older than `--low-conf-age-days` (default 30).

  Default-importance notes are never pruned by the first rule; default-confidence (0.5)
  notes are never pruned by the second — only unproven, unused, stale ones.

Useful flags: `--dry-run` (preview counts without changing the store), `--max-age-days N`,
`--low-conf-age-days N`. To preview first:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py consolidate --dry-run
```

After running, report the counts the script prints. If nothing changed, say so plainly.
