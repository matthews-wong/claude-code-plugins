---
name: memory-export
description: Use when the user wants to save or share their memory — back it up, or carry learnings AND instincts to another project or machine in one portable file.
---

The user wants to export the whole memory store (both learnings and instincts) to a
single portable JSON file.

1. Choose an output path. Default to `memory-export.json` in the current directory unless
   the user names one.
2. Run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py export --out <path>
```

The file contains BOTH the learnings and the instincts under one envelope
(`{"kind":"memory-export","version":1,"notes":[...],"instincts":[...]}`).

Tell the user how many learnings and instincts were written and where. Mention they can
bring this file into another project with `/memory-import`.
