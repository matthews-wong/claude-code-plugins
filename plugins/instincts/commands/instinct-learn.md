---
name: instinct-learn
description: Use when the user wants the agent to learn from accumulated notes — scan recurring lessons from the knowledge-loop store and graduate them into durable instincts. Run periodically or after a burst of work.
---

The user wants to run the auto-learning step: scan raw learnings and promote recurring ones into durable instincts.

Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py promote
```

This reads the sibling `knowledge-loop` store at `.claude/knowledge/notes.jsonl` (if present), clusters notes by similarity, and promotes any lesson that recurs (a cluster of 2 or more) or any note explicitly marked `kind: semantic` into an instinct. Duplicates reinforce existing instincts instead of piling up.

If the knowledge store is absent the command does nothing and exits cleanly. After running, report how many instincts were promoted versus reinforced, and optionally run `list` to show the newly graduated rules.

Optional flags: `--notes <path>` to point at a different notes file, `--min-support N` to require larger clusters before promoting.
