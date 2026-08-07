# Design & feature list

An honest, factual list of what the `memory` plugin provides. No comparisons to other
projects — just what is in this code.

## Features

- **Unified store, one install.** A single directory `.claude/memory/` holds both
  `notes.jsonl` (learnings) and `instincts.jsonl` (rules), driven by one CLI
  (`scripts/memory.py`) and one shared helper module (`scripts/_common.py`). Installing
  this one plugin gives the whole capture → retrieve → promote → surface loop.
- **Zero dependencies, standard library only.** Pure Python 3 stdlib (`json`, `math`, `re`,
  `os`, `collections`, `datetime`, `time`, `uuid`, `argparse`). No pip installs, no model
  downloads, no network calls — safe to run straight from hooks. Shell glue is POSIX `sh`.
- **Hybrid retrieval.** Learnings are ranked by a TF-IDF cosine ("lexical vector search")
  AND a keyword-overlap signal, fused with **Reciprocal Rank Fusion** (`K = 60`).
- **Recency decay + importance/usefulness/confidence weighting.** The fused score is
  multiplied by an exponential recency factor (`exp(-age/90d)`), the note's `importance`,
  a usefulness boost from `access_count`, and a gentle confidence factor in `[0.7, 1.0]`.
- **Episodic / semantic / instinct tiers.** Notes are `episodic` (what happened) or
  `semantic` (a distilled principle, given a small retrieval nudge); recurring or semantic
  notes graduate into `instinct` rules — three tiers of increasing durability.
- **Auto-promotion.** `promote` graduates semantic notes on their own and clusters
  recurring episodic notes (Jaccard single-link) into rules, reinforcing near-duplicates
  by the `confidence = 1 - 0.5^support` model instead of duplicating them.
- **Folder + global scope.** Learnings and instincts carry a project-relative folder /
  scope; retrieval and surfacing favor the current folder and its lineage, while repo-wide
  items (`folder: .`) promote to `global` and can surface anywhere. Instinct scopes reuse
  the note folder vocabulary so lineage matching lines up across both stores.
- **Consolidation / forgetting.** `consolidate` merges near-duplicate learnings and prunes
  stale, low-value ones (two independent age/importance and age/confidence rules), with a
  `--dry-run` preview.
- **Export / import, both layers in one file.** `export` writes learnings + instincts under
  one JSON envelope; `import` merges both back with the same dedup/reinforce rules. Also
  accepts a legacy bare instincts array.
- **Dedup everywhere.** On ingest, on import, and during consolidation, near-duplicate
  learnings merge (cosine ≥ 0.85) and near-duplicate rules reinforce (Jaccard ≥ 0.8) —
  re-recording a known lesson strengthens it rather than cluttering the store.
- **Auto-surface every session.** A `SessionStart` hook prints both the top relevant
  learnings and the active instincts for the current folder; a `Stop` hook nudges capture.
- **Hook-safe by construction.** Every subcommand tolerates a missing store and exits 0;
  the surface script degrades silently if Python is absent; the access-bump write is fully
  guarded so a read-only store never breaks a session.
- **Status dashboard.** `status` reports learning counts by kind, instinct counts by scope,
  average confidences, top reinforced rules, and store size on disk.

## Honesty notes

- **Capture is model-driven, not automatic.** A hook cannot read the model's reasoning, so
  it cannot know what was learned; it can only nudge. The model (or user) decides what to
  record.
- **The vector search is lexical.** TF-IDF cosine matches shared words, not meaning; the
  keyword signal and RRF hedge its blind spots. Swapping in embeddings is a drop-in change
  to the vectorizer only.
- **Promotion is heuristic.** Clustering by token overlap can group loosely-related notes;
  promoted rules are worth a human/model review, which is why they surface for the agent to
  apply rather than being enforced silently.

## Relationship to the separate plugins

This plugin combines this repo's `knowledge-loop` (folder-scoped learnings + hybrid search)
and `instincts` (promotion into durable rules) into one install with one store. Those two
plugins remain available separately for anyone who wants just one half; `memory` is the
integrated option.
