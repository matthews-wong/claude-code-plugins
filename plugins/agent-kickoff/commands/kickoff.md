---
name: kickoff
description: Decompose a task into independent subtasks, kick off a subagent for each, and synthesize their results into one answer.
args: "[the task to decompose and orchestrate]"
---

Orchestrate this task by fanning it out to subagents: **$ARGUMENTS**

Follow the `agent-orchestration` skill for the decision rules. Proceed like this:

1. **Decide whether to parallelize.** Only fan out if the task splits into parts
   that are genuinely independent (no part needs another's output) and each part
   is substantial enough to justify its own agent. If the work is inherently
   sequential, small, or the parts share heavy state, do it yourself in one
   thread and say why — do not manufacture parallelism.

2. **Decompose.** Break the task into a small number of self-contained subtasks
   (usually 2-4). For each, write a crisp brief: the objective, the inputs/paths
   it needs, and the exact shape of the result you want back. Independent briefs
   are what make fan-out safe.

3. **Kick off subagents.** Launch one subagent per subtask using the Agent tool.
   Issue the independent launches in a single message so they run concurrently.
   Choose a read-only/explorer agent for investigation and a general-purpose
   agent for work that must edit files. Give each only the context it needs.

4. **Synthesize.** When the subagents report back, reconcile their findings:
   resolve conflicts, remove duplication, and merge into one coherent result.
   The subagents' raw output is not shown to the user — you are responsible for
   relaying what matters and for the final integrated answer.

5. **Guard against contention.** If two subtasks would edit the same files,
   do not run them in parallel — sequence them, or isolate them on separate git
   worktrees, to avoid conflicting writes.

Report: the decomposition you chose (and why), which parts ran in parallel, and
the synthesized result.
