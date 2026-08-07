---
name: memory-import
description: Use when the user wants to bring memory in from a file — restoring a backup, or carrying learnings and instincts from another project or teammate into this repo.
---

The user wants to merge a portable memory file (learnings + instincts) into this
project's store.

1. Confirm the input file path (ask only if it is ambiguous).
2. Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py import --in <path>
```

Merging is non-destructive and follows the same dedup rules as normal capture:
- **Learnings** near-duplicate an existing note in the same folder are merged (importance
  and confidence rise) rather than duplicated.
- **Instincts** near-duplicate a rule in the same scope reinforce it (support rises).

It accepts the `memory-export` envelope, and also a bare list of instinct records (a
legacy instincts-only export). Report how many learnings were added vs merged and how
many instincts were added vs reinforced.
