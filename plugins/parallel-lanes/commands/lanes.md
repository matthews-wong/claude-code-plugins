---
name: lanes
description: Partition a large task into independent parallel lanes, dispatch each to its own agent or worktree, then merge and synthesize the results.
args: "<task description, or leave blank to use the current goal in context>"
---

You are orchestrating a large task using the parallel-lanes pattern. The user's task is:

$ARGUMENTS

Follow this workflow:

1. Restate the overall goal in one sentence so we agree on scope. If the task
   is genuinely small or inherently sequential, say so and recommend running it
   directly instead of fanning out — do not force parallelism where it adds only
   coordination overhead.

2. Decompose the goal into 2 to 5 independent "lanes." A good lane:
   - Owns a disjoint set of files or a distinct concern, so two lanes rarely
     touch the same lines and merge conflicts stay unlikely.
   - Can be described to a fresh agent with no shared hidden context.
   - Produces a self-contained, reviewable artifact (a diff, a report, a set of
     tests).
   Present the proposed lanes as a short table: lane name, scope, files/areas it
   owns, and expected output.

3. Decide the isolation strategy and state it explicitly:
   - Use the Agent tool to launch one subagent per lane when lanes only need to
     read shared code and write to disjoint paths.
   - Prefer a separate git worktree per lane (isolation "worktree") when lanes
     make overlapping structural changes or need to build/test in isolation.
   Give each lane a crisp, self-sufficient prompt containing only what that lane
   needs. Launch independent lanes in parallel (multiple Agent calls in one
   turn), not one at a time.

4. While lanes run, maintain a short status ledger (lane -> pending/done/failed).
   Do not re-run a lane's work yourself; wait for its report.

5. Merge and synthesize once lanes report back:
   - Reconcile overlaps and resolve any conflicting decisions, naming the
     tradeoff you chose and why.
   - Integrate worktree branches in a deterministic order, running tests after
     each merge so a failure points to a single lane.
   - Produce one unified summary of what changed across all lanes, plus any
     follow-ups that fell between lanes.

Keep the user informed at the decomposition step and the merge step — those are
the two moments where a wrong call is expensive to unwind. Consult the
`parallel-lanes` skill for partitioning heuristics and conflict-avoidance rules.
