# agent-kickoff

Turn a big task into a coordinated set of subagents. `/kickoff` decomposes a
task into independent subtasks, launches a subagent for each (agent-to-agent
orchestration), and synthesizes their results into one answer — with explicit
rules for when parallelism helps and when it hurts.

## Components
- `commands/kickoff.md` — `/kickoff [task]` runs the decompose → fan-out →
  synthesize loop.
- `skills/agent-orchestration/SKILL.md` — the reusable decision framework.

## The core idea
Parallel subagents shine for independent, read-heavy investigation and cleanly
partitioned work; they backfire on sequential dependencies, shared-state edits,
and small tasks. When work must edit the same files, isolate it on separate git
worktrees instead of racing.

## Usage
```
/kickoff audit auth, map the data model, and list every public API route
```

Author: Matthews Wong — MIT License.
