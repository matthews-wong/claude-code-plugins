---
name: agent-orchestration
description: Use when a task is large enough to split across multiple subagents. Explains how to decompose a task into independent subtasks, kick off a subagent per subtask (agent-to-agent orchestration), synthesize the results, and — critically — when parallel subagents help versus when they hurt. Triggers on "orchestrate", "fan out", "parallel agents", "split this across agents", "kick off subagents".
---

# Agent Orchestration

A lead agent can delegate to subagents, each running in its own context window,
and then combine their results. Done well this covers more ground and keeps the
lead's context clean. Done carelessly it burns tokens and produces conflicting
work. This skill is about choosing well.

## When parallel subagents HELP

- **Independent, read-heavy investigation.** Several questions that don't depend
  on each other — "audit the auth layer", "map the data model", "list the API
  routes" — each explored in its own agent, keeping thousands of lines of file
  reads out of the lead context. This is the strongest case.
- **Breadth with clean boundaries.** Work that partitions cleanly by directory,
  package, or concern, where each part's output is a self-contained report.
- **Isolatable edits.** Parallel edits are safe only when the subtasks touch
  disjoint files (ideally on separate git worktrees). See the
  `worktree-isolation` skill.

## When parallel subagents HURT

- **Sequential dependencies.** If B needs A's output, running them together just
  makes B guess. Sequence them instead.
- **Shared mutable state / same files.** Concurrent agents editing the same
  files produce merge chaos and lost writes.
- **Small or cheap tasks.** Spin-up, briefing, and synthesis overhead can exceed
  the work itself. One thread is faster.
- **Judgment requiring the whole picture.** Design decisions and cross-cutting
  refactors need one mind holding all the context, not fragments.

## The loop

1. **Decompose** into a small number (2-4) of self-contained subtasks. Each gets
   a brief: objective, required inputs/paths, and the exact result shape wanted.
2. **Assign the right agent** per subtask — read-only explorer for investigation,
   general-purpose for work that edits files. Give each only what it needs.
3. **Launch independent subtasks together** (multiple Agent calls in one message)
   so they run concurrently; sequence the dependent ones.
4. **Synthesize.** Reconcile conflicts, dedupe, and merge into one coherent
   result. The lead owns the final answer; subagent raw output is not shown to
   the user, so relay what matters.

## Guardrails

- Prefer the simplest structure that works — one capable agent beats a crowd of
  confused ones.
- Cap fan-out width; a few focused agents beat a swarm.
- Make result shapes explicit so synthesis is mechanical, not archaeological.
- Never parallelize writes to shared files without worktree isolation.
