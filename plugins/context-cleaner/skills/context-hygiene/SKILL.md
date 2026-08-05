---
name: context-hygiene
description: Use when a Claude Code session is bloated, stuck, or drifting — repeated failed corrections, mixing unrelated tasks in one session, exploration that never converges, or deciding between /clear, /compact, and subagents. Helps recognize the failure pattern and re-prompt with a clean context that incorporates what was learned.
---

# Context hygiene

Context is a limited, shared resource. A session that carries stale history, repeated failed attempts, or unrelated tasks reasons worse — attention is diluted and the model anchors on dead ends. Managing the session deliberately beats fighting a polluted one.

## Recognize the failure pattern

**Kitchen-sink session.** One session has drifted across several unrelated tasks. The history is now mostly irrelevant to whatever is current, burning tokens and diluting focus.
→ `/clear` between unrelated tasks. Each task deserves a clean context.

**Correcting over and over.** You've corrected the same behavior about twice and it's still wrong. Each correction adds contradictory, failure-laden context that makes the next attempt worse, not better — a doom loop.
→ After ~2 failed corrections, **stop patching**. `/clear` and re-prompt from scratch, folding in what you learned about *why* it failed. See the re-prompt recipe below.

**Infinite exploration.** Endless searching and reading, no convergence, context filling while the task stalls.
→ Scope the investigation to a **subagent** so only the conclusion returns to the main session — not the raw file dumps. If it's one long but coherent task low on room, `/compact` instead.

## The tools

- **`/clear`** — wipe the context and start fresh. Use between unrelated tasks and after repeated failed corrections. The default reset.
- **`/compact`** — summarize and condense the current context while preserving the thread. Use for a single long, coherent task that's running low on room but is going well.
- **Subagents** — delegate investigations/searches; the subagent burns its own context and returns just the answer, keeping the main session lean.

## The re-prompt recipe (after failed corrections)

Don't just retry. Before clearing, extract the learnings, then write one clean prompt:

1. **Goal** — state the outcome plainly, as if for the first time.
2. **Constraints & context** — the facts that matter (files, interfaces, environment).
3. **What we learned** — the specific dead ends and the reason each failed ("X doesn't work because Y; the real cause is Z").
4. **The approach to take** — direct it toward the path the failures pointed to.

`/clear`, paste the re-prompt, and start clean with all the hard-won knowledge and none of the doom-loop baggage.

See `reference/patterns.md` for detailed symptoms, triggers, and worked before/after re-prompt examples.
