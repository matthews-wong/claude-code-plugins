---
name: instinct-add
description: Use when the user states a durable rule the agent should always follow in this repo or globally (e.g. "always run make test before committing", "never edit generated files") and wants it remembered as an instinct.
---

The user wants to record a durable, learned rule (an "instinct") that the agent should follow going forward.

1. Read the rule the user described. Rephrase it as ONE concise, imperative sentence (e.g. "Always run `make test` before committing.").
2. Decide the scope: `global` if it applies everywhere, or the specific folder path it is scoped to.
3. Infer 1-3 short tags (e.g. `testing`, `git`) if helpful.
4. Run the CLI:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py add --rule "<the rule>" --scope <global|folder> --tags <a,b>
```

If a near-duplicate already exists in the same scope, the tool reinforces it (support and confidence rise) instead of creating a duplicate. Report to the user whether the instinct was newly added or reinforced, and show its confidence.
