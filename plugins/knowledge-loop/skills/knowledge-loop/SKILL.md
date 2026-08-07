---
name: knowledge-loop
description: Folder-scoped knowledge memory for a repo. Use when you solve a tricky bug, hit a non-obvious gotcha, work around a quirk, or make a design decision worth remembering — record it as a concise learning. Also use when starting a task in a folder or picking up unfamiliar code — recall prior learnings first so you inherit what past sessions figured out. Triggers: "remember this", "record a learning", "note this gotcha", "what did we learn here", "recall prior context", "why did we decide", capturing fixes/decisions/pitfalls, or resuming work in a folder.
---

# Knowledge Loop

A local, folder-scoped memory for this repo. It closes a loop: **capture** concise
learnings as you work, **store** them locally, and **retrieve** the most relevant ones
(by a folder-scoped hybrid search — TF-IDF + keyword, fused with reciprocal rank fusion,
then reweighted by recency, importance, and usefulness) when a future session starts or
asks.

## Recall before you build

When you begin a task in a folder or touch unfamiliar code, check what past sessions
learned here before diving in:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieve.py" "$(pwd)" <optional query terms>
```

Add query terms (the problem, feature, or filenames) to sharpen the match. Fold anything
relevant into your plan. (This also runs automatically at session start via a hook.)

## Capture when you learn something non-obvious

When you solve a tricky bug, discover a gotcha, or make a notable decision, record it as
one durable, self-contained note — name the folder and the problem, then the lesson:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/store.py" --text "the lesson" --folder "src/auth" --tags "bug,async"
```

Keep notes short (1-3 sentences), one insight each, no secrets. Skip the trivial. Add
`--kind semantic` when the note is a reusable principle rather than a one-off episode
(default is `episodic`). Near-duplicates in the same folder are merged automatically on
store, so re-recording a known lesson strengthens it instead of cluttering the store.

The `/recall` and `/learn` commands wrap these two steps for on-demand use. `/consolidate`
runs an occasional cleanup — merging duplicates and forgetting stale, low-value notes.

## Honesty about what is and isn't automatic

- **Retrieval is automatic** — a `SessionStart` hook surfaces relevant learnings.
- **Capture is model-driven** — a hook cannot read your reasoning to know what was
  learned, so it cannot write notes for you. A `Stop` hook only *nudges* you to record.
  You (via this skill or `/learn`) decide what is worth remembering and write it.

## Deeper reference

- `reference/how-it-works.md` — the capture→store→retrieve loop, folder scoping, the hybrid
  RRF search with recency/importance weighting, episodic-vs-semantic, dedup/consolidation,
  and how to swap in embeddings for semantic search.
- `reference/store-format.md` — the `notes.jsonl` schema and the privacy / gitignore note.
