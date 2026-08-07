---
name: consolidate
description: Use to tidy the local knowledge store — merge near-duplicate learnings and forget stale, low-value ones. Run occasionally (or when retrieval feels noisy) to keep the store lean so the most useful lessons keep surfacing.
---

You are running a consolidation / forgetting pass over the folder-scoped knowledge
store so it stays lean and the most useful learnings keep surfacing.

Run the consolidation script:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/consolidate.py"
```

What it does:

- **Merges near-duplicates** across the whole store (TF-IDF cosine ≥ 0.85): the
  longer text is kept, tags are unioned, importance is bumped, and a `semantic`
  kind wins over `episodic`.
- **Prunes stale, low-value notes**: a note is forgotten only when it is older than
  `--max-age-days` (default 365) AND has `importance < 1.0` AND was never used
  (`access_count == 0`). Default-importance notes are never pruned.

Useful flags:

- `--dry-run` — report what would be merged/pruned without changing the store.
- `--max-age-days N` — change the staleness cutoff (default 365).

To preview first, run:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/consolidate.py" --dry-run
```

After running, report the counts the script prints (how many notes went in, how many
remain, how many were merged and pruned). If nothing changed, say so plainly.
