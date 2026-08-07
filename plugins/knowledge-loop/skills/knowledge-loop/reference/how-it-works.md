# How the knowledge loop works

The plugin closes a three-step loop so each session leaves the repo a little smarter
than it found it.

```
   capture (skill / /learn)          store (store.py)             retrieve (retrieve.py)
  ┌──────────────────────┐        ┌──────────────────────┐     ┌───────────────────────────┐
  │ model distills a      │        │ append 1 JSON line to │     │ hybrid TF-IDF + keyword    │
  │ durable lesson from   │──────▶ │ .claude/knowledge/    │────▶│ RRF fusion, recency decay, │
  │ what just happened    │        │ notes.jsonl (+ dedup) │     │ importance/usefulness       │
  └──────────────────────┘        └──────────────────────┘     └───────────────────────────┘
            ▲                                │                                  │
            │        Stop hook NUDGES ───────┤   /consolidate merges + forgets  │
            └────────────────────────────────┴──────────────────────────────────┘
                                                        SessionStart hook surfaces top-K
```

The design borrows directly from the agent-memory literature: **Reflexion** (agents that
reuse distilled lessons improve), **Mem0** and **A-Mem** (importance-weighted, deduplicated
memories with an episodic/semantic split and consolidation), **reciprocal rank fusion**
(run several searches and fuse their ranked lists), and an exponential **recency-decay**
forgetting curve.

## Capture → store

Capture is **model-driven**, and deliberately so. A hook runs shell commands; it cannot
see the model's chain of thought, so it has no way to know *what* was learned in a
session. Only the model (prompted by the `knowledge-loop` skill or the `/learn` command,
or by the user) can distill the lesson. It writes the note by invoking `store.py`, which
appends a single JSON object to `.claude/knowledge/notes.jsonl`, creating the file on
first use. The `Stop` hook (`capture-nudge.sh`) is purely a **reminder** — it prints a
one-line nudge when the store looks small; it never fabricates notes.

### Episodic vs semantic (A-Mem)

Every note has a `kind`:

- **episodic** — *what happened*: a specific bug, fix, or surprise in a session. The
  default.
- **semantic** — *a reusable principle*: a distilled reflection that should apply beyond
  the moment it was learned (`store.py --kind semantic`).

Retrieval gives `semantic` notes a small multiplier, so distilled principles surface a
little more readily than raw episodes — the intuition behind A-Mem's memory typing.

### Dedup on ingest (Mem0 / A-Mem)

Before appending, `store.py` compares the new note (by TF-IDF cosine) to existing notes
**in the same folder**. If the closest match is `≥ 0.85`, it **merges** into that note
instead of adding a near-duplicate: it keeps the longer text, unions the tags, bumps
`importance` (a lesson learned twice matters more), lets a `semantic` kind win, and
refreshes `ts`. This keeps the store from filling with slight rewordings of the same
lesson.

## Retrieve → surface

Retrieval is **automatic**. The `SessionStart` hook runs `retrieve.sh`, which calls
`retrieve.py` with the current working directory. The ranking blends several signals:

1. **Two parallel searches.** For every note it computes a **TF-IDF cosine** score and a
   **keyword-overlap** score against the query (the current relative folder path as words,
   plus any extra terms). Each produces its own ranked list of hits.
2. **Reciprocal Rank Fusion (RRF).** The two lists are fused by
   `rrf = 1/(K + rank_cosine) + 1/(K + rank_keyword)` with `K = 60` — the canonical "run
   vector + keyword search in parallel and fuse the ranked lists" recipe. A note absent
   from one list simply contributes nothing from it.
3. **Recency decay.** The fused score is multiplied by `exp(-age_days / HALF_LIFE)`
   (`HALF_LIFE = 90` days), so stale lessons fade unless they are re-confirmed. A note with
   no parseable `ts` gets a neutral factor of `1.0`.
4. **Importance & usefulness.** Multiplied by the note's `importance` (default `1.0`) and by
   a usefulness boost `1 + 0.1 · log1p(access_count)` — notes that repeatedly proved worth
   surfacing rise over time (Reflexion-style reuse; Mem0-style importance).
5. **Folder-lineage boost.** ×`1.5` when a note's `folder` is an ancestor/descendant/equal
   of the current folder, so locally-relevant lessons rise even when wording differs.
6. **Episodic vs semantic.** A small ×`1.1` nudge for `semantic` notes.

It prints a compact top-K (default 3) list and then **reinforces what it surfaced**:
best-effort, it increments `access_count` and sets `last_used` on the returned notes. That
write is fully guarded — a read-only or locked store never breaks the hook, which always
exits 0. If the store is missing or has no relevant match, it prints nothing and exits 0.

## Consolidation / forgetting (`/consolidate`)

A store that only grows gets noisy. `consolidate.py` (wired to `/consolidate`) runs a
maintenance pass over the **whole** store:

- **Merge near-duplicates** — any pair with TF-IDF cosine `≥ 0.85` is merged (same rule as
  ingest dedup: longer text kept, tags unioned, importance bumped, semantic wins).
- **Prune stale, low-value notes** — a note is forgotten only when it is older than
  `--max-age-days` (default `365`) **and** has `importance < 1.0` **and** was never used
  (`access_count == 0`). Default-importance notes are therefore never pruned; only
  explicitly low-importance, never-reused, stale notes are. `--dry-run` previews the counts.

## The "vector search", honestly labeled

The cosine half of the hybrid is a **lexical vector search**: TF-IDF turns text into sparse
term-frequency vectors and cosine measures their angle. It is implemented by hand with
`math` and `collections` (standard library only) so it runs from a hook with zero
dependencies — no pip, no model download, no network. TF-IDF, briefly:

- **TF** (term frequency): how often a term appears in a note, normalised by note length.
- **IDF** (inverse document frequency): `log((1 + N) / (1 + df)) + 1`, down-weighting
  terms common across all notes and up-weighting distinctive ones.
- **Cosine similarity**: dot product of two vectors divided by the product of their
  norms — similarity of direction, insensitive to length.

Because it is lexical, it matches on **shared words**, not meaning ("auth" won't match
"login" unless both words appear); the keyword-overlap signal and RRF make the ranking more
robust to any single signal's blind spots. To get **semantic** matching, swap the
vectorizer: keep the same JSONL store, the same RRF fusion, and the same recency/importance
weighting, but replace TF-IDF vectors with sentence embeddings (a local embedding model or
an embeddings API). The retrieval contract — folder path + query in, ranked notes out —
stays the same, so only `retrieve.py`'s vectorization step changes.

## Folder scoping

Learnings are tied to a `folder` (project-relative path). Retrieval favors the folder you
are working in and its lineage, so a lesson recorded under `src/auth` surfaces when you
work in `src/auth` or its subfolders, while repo-wide lessons live under `.` and can
surface anywhere.

## Backward compatibility

Older notes may predate the `kind`, `importance`, `access_count`, and `last_used` fields.
Every reader defaults them (`kind = episodic`, `importance = 1.0`, `access_count = 0`,
recency neutral when `ts` is missing), so an existing `notes.jsonl` keeps working unchanged
and simply gains the new behavior as notes are re-touched.
