---
name: instinct-export
description: Use when the user wants to save or share their instincts — back them up, or carry learned rules to another project or machine.
---

The user wants to export their instincts to a portable JSON file.

1. Choose an output path. Default to `instincts-export.json` in the current directory unless the user names one.
2. Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/instincts.py export --out <path>
```

Tell the user how many instincts were written and where. Mention they can bring this file into another project with `/instinct-import`.
