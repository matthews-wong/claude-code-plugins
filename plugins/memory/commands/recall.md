---
name: recall
description: Use when starting work in a folder or on a problem and you want to know what past sessions already learned here. Retrieves and summarizes the most relevant prior learnings from the local memory store via folder-scoped hybrid vector search.
---

You are surfacing relevant prior learnings before diving into work, so you do not
relearn what a past session already figured out.

Run the retrieval subcommand. Pass the current working folder first, and append any
extra query terms (the problem, feature, or file names) to sharpen the hybrid search:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py recall "$(pwd)" <optional query terms>
```

For example, to recall learnings about "auth token refresh":

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py recall "$(pwd)" auth token refresh
```

Then read the ranked results and give the user a short, grouped summary of what applies
to their current task — call out anything that changes how they should proceed. If the
script prints nothing, the store is empty or has no relevant match; say so plainly and
suggest capturing learnings with `/learn` as work progresses.
