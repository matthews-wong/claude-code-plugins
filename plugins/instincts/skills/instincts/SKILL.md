---
name: instincts
description: Durable, learned rules the agent should follow. Auto-invoke this skill when (1) a lesson recurs during work — the same mistake, correction, or preference shows up again — to PROPOSE promoting it into a durable instinct; and (2) when STARTING a task in a repo — to APPLY the active instincts already recorded so the agent follows established rules instead of relearning them.
---

# Instincts

An **instinct** is a high-confidence rule the agent should follow, distilled from
repeated experience — for example "In this repo, always run `make test` before
committing." Instincts are the promoted layer above raw learnings: when a lesson
recurs, it graduates into an instinct that is auto-surfaced every session.

## When starting work — APPLY instincts

At the start of a task, the active instincts for the current folder and the
global scope are already surfaced by the SessionStart hook. Treat them as
standing rules: follow them without being reminded. If you need the current list
explicitly, run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py list --scope "$(pwd)"
```

Higher confidence and higher support mean stronger, more-reinforced rules.

## When a lesson recurs — PROPOSE an instinct

If you notice the same correction, gotcha, or preference coming up again (the
user re-states it, or you hit the same wall twice), propose capturing it:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py add --rule "<concise imperative rule>" --scope <global|folder> --tags <a,b>
```

Phrase the rule as one short imperative sentence. If a near-duplicate exists in
the same scope, the tool reinforces it (support and confidence rise) rather than
duplicating.

## Auto-learning from the knowledge loop

To graduate accumulated raw notes in bulk, run the promotion step, which mines
the sibling `knowledge-loop` store and promotes recurring lessons:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py promote
```

## Reference

- `reference/how-it-works.md` — the memory → learning → instinct loop, the
  confidence/support model, export/import for cross-project sharing, and how
  this pairs with the `knowledge-loop` plugin.
- `reference/schema.md` — the instinct record schema.
