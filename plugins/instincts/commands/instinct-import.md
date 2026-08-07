---
name: instinct-import
description: Use when the user wants to bring instincts in from a file — restoring a backup, or carrying learned rules from another project or teammate into this repo.
---

The user wants to merge instincts from a portable JSON file into this project's store.

1. Confirm the input file path (ask only if it is ambiguous).
2. Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py import --in <path>
```

Merging follows the same dedup rule as adding: a rule that closely matches an existing one in the same scope reinforces it rather than duplicating. Report how many instincts were added versus reinforced.
