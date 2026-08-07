---
name: memory-status
description: Use when the user wants an overview of the memory store — how many learnings and instincts exist, their kinds and scopes, average confidence, the most-reinforced rules, and the store size.
---

The user wants a dashboard of the unified memory store (both learnings and instincts).

Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py status
```

The dashboard reports:
- **Learnings** — total, breakdown by kind (episodic / semantic), average confidence.
- **Instincts** — total, breakdown by scope, average confidence, the top reinforced rules.
- **Store size** — bytes on disk for each file.

Summarize the results for the user in plain language. Point out any high-confidence,
heavily-reinforced instincts that clearly matter for the current work, and note whether
the store looks healthy (a growing base of learnings, some promoted into instincts) or
whether a `/memory-promote` or `/memory-consolidate` pass would help.
