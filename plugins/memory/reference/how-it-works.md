# How the unified memory loop works

The `memory` plugin is one install with two cooperating layers under a single store
directory, `.claude/memory/`:

- **Learnings** — `notes.jsonl`: episodic/semantic notes, high-volume, captured cheaply.
- **Instincts** — `instincts.jsonl`: durable rules, low-volume, promoted when a lesson
  recurs, surfaced every session.

Together they close one continuous-learning loop so each session leaves the repo a little
smarter than it found it:

```
   capture (skill / /remember)      store + dedup            hybrid retrieval + rule surfacing
  ┌───────────────────────┐       ┌───────────────────┐    ┌───────────────────────────────┐
  │ model distills a       │       │ .claude/memory/    │    │ recall: TF-IDF + keyword RRF,  │
  │ durable lesson from    │─────▶ │ notes.jsonl        │──▶ │ recency decay, importance/use, │
  │ what just happened     │       │ (dedup on ingest)  │    │ confidence, folder boost       │
  └───────────────────────┘       └───────────────────┘    └───────────────────────────────┘
            ▲                               │                              │
            │  Stop hook NUDGES ────────────┤   promote (recurring →       │
            │                               │   instincts.jsonl)           ▼
            │                               │                     SessionStart hook surfaces
            └───────────────────────────────┴──────── recurs ─────  top-K learnings + instincts
```

The design borrows from the agent-memory literature: **Reflexion** (agents that reuse
distilled lessons improve), **Mem0** and **A-Mem** (importance-weighted, deduplicated
memories with an episodic/semantic split and consolidation), **reciprocal rank fusion**
(run several searches and fuse their ranked lists), and an exponential **recency-decay**
forgetting curve.

## Capture → store (learnings)

Capture is **model-driven**, and deliberately so. A hook runs shell commands; it cannot
see the model's chain of thought, so it has no way to know *what* was learned. Only the
model (prompted by the `memory` skill, `/remember`/`/learn`, or the user) can distill the
lesson. It writes the note via `memory.py remember`, which appends one JSON object to
`.claude/memory/notes.jsonl`. The `Stop` hook (`capture-nudge.sh`) is purely a **reminder**
when the store looks small; it never fabricates notes.

### Episodic vs semantic (A-Mem)

Every note has a `kind`: **episodic** (what happened — a specific bug/fix/surprise, the
default) or **semantic** (a distilled, reusable principle, `--kind semantic`). Retrieval
gives `semantic` notes a small multiplier so principles surface a little more readily.

### Dedup on ingest (Mem0 / A-Mem)

Before appending, `remember` compares the new note (TF-IDF cosine) to existing notes **in
the same folder**. If the closest match is `≥ 0.85`, it **merges** instead of adding a
near-duplicate: keeps the longer text, unions tags, bumps `importance`, raises `confidence`
toward 1.0 (corroboration), lets a `semantic` kind win, and refreshes `ts`.

### Confidence-scored learnings

Every note carries a `confidence` in `[0.0, 1.0]` (default `0.5`). Two signals raise it
toward 1.0 with diminishing returns (`conf → conf + (1 - conf)·gain`): **corroboration**
(a dedup-merge, `gain = 0.3`) and **used-and-survived** (retrieval surfaces it,
`gain = 0.05`). Set an initial value with `--confidence 0.8` when you already trust a
lesson.

## Retrieve → surface

Retrieval is **automatic**. The `SessionStart` hook runs `surface.sh`, which calls
`memory.py recall "$(pwd)"` and `memory.py instincts --scope "$(pwd)"`. The learnings
ranking blends several signals:

1. **Two parallel searches** — a **TF-IDF cosine** score and a **keyword-overlap** score
   against the query (the current relative folder path as words, plus any extra terms).
2. **Reciprocal Rank Fusion (RRF)** — `rrf = 1/(K + rank_cosine) + 1/(K + rank_keyword)`
   with `K = 60`, the canonical "fuse a vector and a keyword ranked list" recipe.
3. **Recency decay** — × `exp(-age_days / HALF_LIFE)` (`HALF_LIFE = 90` days); a note with
   no parseable `ts` gets a neutral `1.0`.
4. **Importance & usefulness** — × `importance` (default `1.0`) and × `1 + 0.1·log1p(access_count)`.
5. **Confidence** — × `0.7 + 0.3·confidence`, a gentle factor in `[0.7, 1.0]`.
6. **Folder-lineage boost** — × `1.5` when a note's folder is an ancestor/descendant/equal.
7. **Episodic vs semantic** — a small × `1.1` nudge for `semantic` notes.

It prints a compact top-K (default 3) and then **reinforces what it surfaced**: best-effort,
increments `access_count`, sets `last_used`, and gives `confidence` a small used-and-survived
bump. The write is fully guarded — a read-only or locked store never breaks the hook, which
always exits 0. Missing store or no match → prints nothing, exits 0.

## Promotion: recurring learnings → instincts

`memory.py promote` is the step that turns repeated lessons into durable rules:

- **Semantic notes** graduate on their own (already distilled).
- **Recurring episodic notes** are clustered by Jaccard token overlap (greedy single-link);
  a cluster of `≥ --min-support` (default 2) graduates into one instinct, with the extra
  members credited as reinforcements.
- A repo-root learning (`folder: .`) promotes to the `global` scope; a folder-scoped
  learning keeps its folder as the instinct scope — so instinct scopes reuse the note
  folder vocabulary and folder-lineage matching lines up across both stores.

### Instinct confidence / support model

Each instinct tracks a `support` integer (times reinforced) and a derived `confidence`:

```
confidence = 1 - 0.5 ** support
```

| support | confidence |
|---------|-----------|
| 1       | 0.50      |
| 2       | 0.75      |
| 3       | 0.875     |
| 4       | 0.9375    |
| 5       | 0.969     |

A fresh rule starts modest (0.50); every reinforcement roughly halves the remaining doubt,
climbing toward but never reaching 1.0. When adding, importing, or promoting, a rule is
compared against existing rules **in the same scope** by Jaccard overlap (stopwords
removed); overlap `≥ 0.8` **reinforces** the existing rule instead of duplicating.

### Surfacing instincts

`memory.py instincts --scope <folder>` lists active rules whose scope is `global` or
folder-related to the current folder, sorted by scope relevance then confidence/support.
The SessionStart hook prints them under "Active instincts" so the agent follows them.

## Consolidation / forgetting

`memory.py consolidate` runs a maintenance pass over the **learnings** store:

- **Merge near-duplicates** — any pair with TF-IDF cosine `≥ 0.85` (same rule as ingest).
- **Prune stale, low-value notes** — dropped when **either**: (1) older than
  `--max-age-days` (default 365) **and** `importance < 1.0` **and** never used; or
  (2) `confidence < 0.3` **and** never used **and** older than `--low-conf-age-days`
  (default 30). Default-importance / default-confidence notes are protected. `--dry-run`
  previews counts.

## Export / import (both layers, one file)

`memory.py export --out <file>` writes BOTH stores under one envelope
(`{"kind":"memory-export","version":1,"notes":[...],"instincts":[...]}`). `import --in
<file>` merges both back with the same dedup rules (notes merge per folder, instincts
reinforce per scope). A bare list is accepted as a legacy instincts-only import. This
carries hard-won memory between repos, teammates, or backups.

## The "vector search", honestly labeled

The cosine half of the hybrid is a **lexical vector search**: TF-IDF turns text into sparse
term-frequency vectors and cosine measures their angle. It is implemented by hand with
`math` and `collections` (standard library only) so it runs from a hook with zero
dependencies — no pip, no model download, no network. Because it is lexical it matches on
**shared words**, not meaning; the keyword-overlap signal and RRF make the ranking robust
to any single signal's blind spot. To get semantic matching, swap the vectorizer for
sentence embeddings — the store, RRF fusion, and weighting stay the same.

## Folder scoping

Learnings and instincts are tied to a `folder`/`scope` (project-relative path). Retrieval
and surfacing favor the folder you are working in and its lineage, so a lesson recorded
under `src/auth` surfaces when you work in `src/auth` or its subfolders, while repo-wide
lessons live under `.` (and promote to `global`) and can surface anywhere.

## Backward compatibility

Older notes may predate the `kind`, `importance`, `confidence`, `access_count`, and
`last_used` fields; every reader defaults them, so an existing store keeps working and
gains the new behavior as notes are re-touched.
