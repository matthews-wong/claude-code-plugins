---
name: memory-promote
description: Use to graduate recurring or distilled learnings into durable instincts (auto-surfaced rules). Run occasionally, or when the same lesson keeps recurring and should become a standing rule the agent always follows.
---

You are promoting accumulated learnings into durable **instincts** — high-confidence
rules that get auto-surfaced at the start of every session.

Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py promote
```

What it does:

- **Semantic learnings** (already distilled principles) graduate into instincts on their own.
- **Recurring episodic learnings** are clustered by token overlap; a cluster with at least
  `--min-support` members (default `2`) graduates into one instinct, with the extra
  members credited as reinforcements (support and confidence rise).
- A repo-root learning (`folder: .`) promotes to the `global` scope; a folder-scoped
  learning keeps its folder as the instinct scope.
- Near-duplicate rules in the same scope are reinforced rather than duplicated.

Useful flag: `--min-support N` — how many recurring notes count as a pattern (default 2).

After running, report the counts (how many promoted vs reinforced, from how many
learnings). New and reinforced instincts will surface automatically next session.
