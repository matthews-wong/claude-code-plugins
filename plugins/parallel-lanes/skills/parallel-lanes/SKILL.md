---
description: How to split a large task into independent parallel lanes run by separate agents or git worktrees, partition work to avoid merge conflicts, and merge the results back into one coherent whole. Use when a task is large enough to benefit from fan-out orchestration.
---

# Parallel Lanes

A "lane" is an independent slice of a larger task that a separate agent (or a
separate git worktree) can execute end to end without coordinating mid-flight
with the other lanes. Fanning out into lanes trades a little planning and merge
overhead for wall-clock speed and cleaner separation of concerns. It pays off
only when the work is genuinely parallelizable.

## When to fan out

Fan out when:
- The task spans several roughly independent areas (e.g. distinct modules,
  services, or document sections).
- Each slice is large enough that the coordination cost is small relative to the
  work saved.
- Slices can be described to a fresh agent with a self-contained prompt.

Do not fan out when:
- The task is small, or one step's output is the next step's input (inherently
  sequential).
- Every slice edits the same core files — you would just be manufacturing merge
  conflicts.
- The decomposition itself is the hard part and needs a human decision first.

## Partitioning to avoid conflicts

The single most important rule: **give each lane a disjoint write set.** Two
lanes may freely read the same code, but they should almost never write the same
files.

Practical partitioning strategies, in rough order of safety:
1. **By directory / module** — lane A owns `src/auth/`, lane B owns
   `src/billing/`. Cleanest when the codebase is already modular.
2. **By file type / layer** — one lane writes migrations, another writes API
   handlers, another writes tests. Works when layers are thin and stable.
3. **By concern across files** — e.g. "rename symbol X everywhere" is a single
   lane, not something to split, because its write set is inherently spread out.
4. **By artifact** — research/report tasks split naturally by section or source.

For shared-surface changes (a common interface, a config file, a shared type),
do not split them across lanes. Either assign the shared file to exactly one
lane that the others depend on, or make the shared edit yourself first and then
fan out the dependent work.

## Isolation: agents vs worktrees

- **Subagents (Agent tool)**: cheapest. Best when lanes read shared code and
  write to disjoint paths in the same working tree. Launch independent lanes in
  parallel by issuing multiple Agent calls in a single turn. Each agent's tool
  output stays out of your context; you keep only its final report.
- **Git worktrees (isolation: "worktree")**: stronger. Each lane gets its own
  checkout and branch, so lanes can build, test, and make overlapping structural
  edits without stepping on each other. Merge branches back deterministically.
  Choose this when lanes need to run the app/tests independently or when write
  sets cannot be perfectly disjoint.

## Writing a good lane prompt

Each lane prompt must be self-sufficient — the lane agent does not see your
conversation. Include: the lane's goal, its exact scope and file ownership, the
interfaces/contracts it must honor at the boundary with other lanes, and the
exact shape of the output you expect back (a diff, a list of changed files, a
report). Explicitly tell the lane what is out of scope so it does not wander into
another lane's write set.

## The merge / synthesis step

Fan-out is only half the pattern; the synthesis is what makes it correct.
1. Collect each lane's report. Keep a ledger of lane -> status.
2. For worktrees, merge branches one at a time in dependency order, running the
   test suite after each merge so any failure is attributable to a single lane.
3. Reconcile boundary decisions: if two lanes made incompatible choices at a
   shared seam, pick one, state the tradeoff, and fix the other.
4. Sweep for gaps that fell between lanes — the integration wiring, cross-cutting
   docs, an end-to-end test that no single lane owned.
5. Produce one unified summary describing the whole change, not five disconnected
   ones.

## Anti-patterns

- Splitting a sequential dependency chain into "parallel" lanes that actually
  block on each other.
- Overlapping write sets — the fastest route to painful merge conflicts.
- Over-decomposing a small task so coordination cost dwarfs the work.
- Skipping synthesis and handing the user five raw lane outputs to reconcile
  themselves.
