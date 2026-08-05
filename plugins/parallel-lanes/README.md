# parallel-lanes

Orchestration plugin for Claude Code. Fan a large task into independent
"lanes," run each in its own subagent or git worktree, then merge and
synthesize the results into one coherent change.

## Components

- **Command `/lanes`** — decompose a task into 2–5 independent lanes, dispatch
  them in parallel, and drive the merge/synthesis step.
- **Skill `parallel-lanes`** — partitioning heuristics, conflict-avoidance
  rules (disjoint write sets), agent-vs-worktree isolation guidance, and how to
  merge lane outputs back together.

## Usage

```
/lanes migrate the auth, billing, and notifications modules to the new logger
```

Or run `/lanes` with no argument to operate on the current goal in context.

## When to use

Reach for this when a task spans several roughly independent areas and is large
enough that coordination overhead is small relative to the parallel speedup.
Skip it for small or inherently sequential work.

Author: Matthews Wong · License: MIT
