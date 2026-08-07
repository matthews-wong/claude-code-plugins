# How the knowledge loop works

The plugin closes a three-step loop so each session leaves the repo a little smarter
than it found it.

```
   capture (skill / /learn)          store (store.py)             retrieve (retrieve.py)
  ┌──────────────────────┐        ┌──────────────────────┐     ┌───────────────────────────┐
  │ model distills a      │        │ append 1 JSON line to │     │ TF-IDF + cosine rank of    │
  │ durable lesson from   │──────▶ │ .claude/knowledge/    │────▶│ notes vs. current folder    │
  │ what just happened    │        │ notes.jsonl           │     │ + folder-lineage boost      │
  └──────────────────────┘        └──────────────────────┘     └───────────────────────────┘
            ▲                                                                │
            │        Stop hook NUDGES ────────────────────────┐             │
            └──────────────────────────────────────────────────┘             ▼
                                                        SessionStart hook surfaces top-K
```

## Capture → store

Capture is **model-driven**, and deliberately so. A hook runs shell commands; it cannot
see the model's chain of thought, so it has no way to know *what* was learned in a
session. Only the model (prompted by the `knowledge-loop` skill or the `/learn` command,
or by the user) can distill the lesson. It writes the note by invoking `store.py`, which
appends a single JSON object to `.claude/knowledge/notes.jsonl`, creating the file on
first use. The `Stop` hook (`capture-nudge.sh`) is purely a **reminder** — it prints a
one-line nudge when the store looks small; it never fabricates notes.

## Retrieve → surface

Retrieval is **automatic**. The `SessionStart` hook runs `retrieve.sh`, which calls
`retrieve.py` with the current working directory. The script:

1. Loads every note from the store (skipping blank/malformed lines).
2. Builds a **TF-IDF vector** for each note's searchable text (body + tags + folder) and
   for the **query** (the current relative folder path as words, plus any extra terms).
3. Ranks notes by **cosine similarity** between the query vector and each note vector.
4. Adds a **folder-lineage boost** to notes whose stored `folder` is an ancestor or
   descendant of the current folder, so locally-relevant lessons rise even when wording
   differs.
5. Prints a compact, top-K (default 3) list under a short header. If the store is missing
   or empty, it prints nothing and exits 0 — the hook is strictly non-blocking.

## The "vector search", honestly labeled

This is a **lexical vector search**: TF-IDF turns text into sparse term-frequency vectors
and cosine measures their angle. It is implemented by hand with `math` and `collections`
(standard library only) so it runs from a hook with zero dependencies — no pip, no model
download, no network. TF-IDF explained briefly:

- **TF** (term frequency): how often a term appears in a note, normalised by note length.
- **IDF** (inverse document frequency): `log((1 + N) / (1 + df)) + 1`, down-weighting
  terms common across all notes and up-weighting distinctive ones.
- **Cosine similarity**: dot product of two vectors divided by the product of their
  norms — similarity of direction, insensitive to length.

Because it is lexical, it matches on **shared words**, not meaning ("auth" won't match
"login" unless both words appear). To get **semantic** search, swap the vectorizer: keep
the same JSONL store and cosine ranking, but replace TF-IDF vectors with sentence
embeddings (e.g. a local embedding model or an embeddings API). The retrieval contract —
folder path + query in, ranked notes out — stays the same, so only `retrieve.py`'s
vectorization step changes.

## Folder scoping

Learnings are tied to a `folder` (project-relative path). Retrieval favors the folder you
are working in and its lineage, so a lesson recorded under `src/auth` surfaces when you
work in `src/auth` or its subfolders, while repo-wide lessons live under `.` and can
surface anywhere.
