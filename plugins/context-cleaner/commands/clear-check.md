---
name: clear-check
description: Use when a session feels stuck, bloated, or off the rails — repeated failed corrections, jumping between unrelated tasks, endless exploration with no progress, or "why isn't this working". Diagnoses the session anti-pattern and recommends /clear or /compact plus a sharper re-prompt that folds in what was learned.
---

Diagnose the health of the current session and recommend whether to keep going, `/compact`, or `/clear` and restart with a better prompt.

$ARGUMENTS

Look back over how this session has actually gone and check it against the common failure patterns:

1. **Kitchen-sink session** — the conversation has covered several unrelated tasks, so the context is now full of stale, irrelevant history that dilutes attention and wastes tokens.
2. **Correcting over and over** — I've corrected the same thing roughly twice or more and it still isn't right. Continuing to patch usually digs deeper; the accumulated back-and-forth is now part of the problem.
3. **Infinite exploration** — lots of searching/reading with no convergence, context filling up while the actual task stalls.

Name which pattern (if any) fits, and give a concrete recommendation:

- **Between unrelated tasks → `/clear`.** Start the next task with a clean context so nothing stale bleeds in.
- **After ~2 failed corrections → `/clear` and re-prompt.** Don't keep patching. Extract what we *learned* about why it failed, then write a fresh, sharper prompt that states the goal and bakes in those learnings from the start. Draft that re-prompt for me.
- **Long-but-coherent single task running low on room → `/compact`.** Preserve the thread while reclaiming context.
- **Investigation ballooning the context → scope it to a subagent.** Delegate the search so only the conclusion returns to this session, not the raw exploration.

If the session is healthy and on-task, say so and recommend continuing — don't clear for its own sake. When you recommend `/clear` with a re-prompt, write the ready-to-paste re-prompt. Consult the **context-hygiene** skill for the full pattern catalog and re-prompt recipe.
