---
name: memory
description: Unified project memory + auto-learning for a repo. Use when you solve a tricky bug, hit a non-obvious gotcha, work around a quirk, or make a design decision worth keeping — record it as a concise folder-scoped learning. Also use when starting a task in a folder or picking up unfamiliar code — recall prior learnings AND apply the active learned rules (instincts) first, so you inherit what past sessions figured out instead of relearning it. Triggers: "remember this", "record a learning", "note this gotcha", "what did we learn here", "recall prior context", "why did we decide", "apply our rules", "promote this into a rule", capturing fixes/decisions/pitfalls, or resuming work in a folder.
---

# Memory

One local, folder-scoped memory system for this repo with two layers, both stored under
`.claude/memory/`:

- **Learnings** (`notes.jsonl`) — concise episodic/semantic notes captured as you work,
  retrieved by a folder-scoped **hybrid search** (TF-IDF cosine + keyword, fused with
  reciprocal rank fusion, then reweighted by recency, importance, usefulness, confidence).
- **Instincts** (`instincts.jsonl`) — durable rules that recurring learnings graduate into,
  auto-surfaced every session so the agent follows them without being reminded.

## Recall + apply before you build

When you begin a task in a folder or touch unfamiliar code, check what past sessions
learned here, and follow the active rules:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py recall "$(pwd)" <optional query terms>
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py instincts --scope "$(pwd)"
```

Both also run automatically at session start via the SessionStart hook. Add query terms
(the problem, feature, or filenames) to sharpen recall. Treat surfaced instincts as
standing rules — higher confidence / support means stronger, more-reinforced.

## Capture when you learn something non-obvious

When you solve a tricky bug, discover a gotcha, or make a notable decision, record one
durable, self-contained note — name the folder and the problem, then the lesson:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py remember --text "the lesson" --folder "src/auth" --tags "bug,async"
```

Keep notes short (1–3 sentences), one insight each, no secrets. Add `--kind semantic` for
a reusable principle (default `episodic`). Near-duplicates in the same folder merge
automatically and grow more confident. `/learn` is the same thing.

## Promote when a lesson recurs

When the same lesson keeps coming up, graduate recurring/semantic learnings into instincts:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py promote
```

`/memory-consolidate` occasionally merges duplicate learnings and forgets stale, low-value
ones. `/memory-status` shows a dashboard; `/memory-export` and `/memory-import` move both
layers between projects in one file.

## Honesty about what is and isn't automatic

- **Retrieval + rule-surfacing are automatic** — a `SessionStart` hook surfaces relevant
  learnings and active instincts.
- **Capture is model-driven** — a hook cannot read your reasoning, so it cannot write notes
  for you. A `Stop` hook only *nudges*. You decide what is worth remembering and write it.
- **Promotion is heuristic** — clustering by token overlap; review promoted rules.

## Deeper reference

- `reference/how-it-works.md` — the unified loop (capture → hybrid retrieval → promotion →
  auto-surface), the retrieval math, and the support/confidence model.
- `reference/schema.md` — both record schemas (learnings and instincts).
- `reference/design.md` — a factual feature list of what this plugin provides.
