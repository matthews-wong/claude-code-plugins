---
name: instinct-status
description: Use when the user wants to review their learned instincts — how many exist, their scopes, average confidence, and which rules are most reinforced.
---

The user wants an overview of the instincts store.

Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py status
```

Then, if useful, also list the active rules:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py list
```

Summarize the results for the user in plain language: total instincts, breakdown by scope, average confidence, and the top reinforced rules. Point out any high-confidence rules (support seen multiple times) that clearly matter for the current work.
