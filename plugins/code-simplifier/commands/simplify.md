---
name: simplify
description: Use when you want to simplify the code that was just written or changed — invoke after finishing a feature or fix to clean up the working diff. Triggers on "simplify", "clean this up", "reduce indirection", "remove dead code", "make it simpler".
---

Run a simplification pass over the code that was recently changed in this session.

1. Determine the working diff. Run `git diff` and `git diff --staged` to see uncommitted changes. If the repo is clean or not a git repo, use the files most recently edited in this session as the target set.
2. Delegate to the `code-simplifier` subagent to simplify those changed files. Its mandate: make the code simpler without changing behavior, preferring to delete lines over adding them.
3. Focus only on recently-changed code — do not refactor unrelated parts of the codebase.

Priorities for the pass:
- Delete dead code, unused imports/variables/params, and commented-out blocks.
- Inline single-use indirection and remove speculative generality (YAGNI).
- Flatten nested control flow with early returns where it reads more clearly.
- Prefer removing lines to adding them — deletion is the strongest simplification.

Constraints:
- Preserve exact observable behavior. If you find a real bug, report it rather than silently fixing it.
- Keep edits minimal, reviewable, and in the existing style.

When done, summarize what was simplified, the net line delta (aim for negative), and anything intentionally left as-is.
