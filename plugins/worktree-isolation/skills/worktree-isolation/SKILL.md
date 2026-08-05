---
name: worktree-isolation
description: Use when running multiple agents or parallel tasks that would otherwise edit the same working tree. Explains how to give each agent its own git worktree (a separate checkout on its own branch backed by one repository) so parallel work stays isolated and merges back cleanly instead of colliding. Triggers on "worktree", "isolate the agents", "run agents in parallel without conflicts", "separate checkouts".
---

# Worktree Isolation

`git worktree` lets one repository have several working directories at once, each
checked out to its own branch but sharing the same object store and history. This
is the clean way to run parallel agents: give each its own worktree so their
edits never land in the same files at the same time.

## Why it beats sharing one checkout

- **No write contention.** Two agents editing the same working tree overwrite
  each other and corrupt in-progress work. Separate worktrees make edits disjoint
  by construction.
- **Cheap and local.** Worktrees share the repo's objects, so creating one is far
  lighter than a full clone, and branches merge back through normal review.
- **Clean mental model.** One branch = one agent = one directory. Easy to reason
  about, easy to throw away.

## Workflow

1. **One worktree per parallel unit of work.** Before fanning out agents that
   will edit files, create a worktree per agent on its own branch:
   ```
   git worktree add ../<repo>-<branch> -b <branch>
   ```
   Put it in a **sibling** directory, never nested inside the main tree.
2. **Point each agent at its worktree.** Each agent `cd`s into its directory and
   works there. Reads and edits stay contained.
3. **Merge back through review.** When an agent finishes, commit on its branch
   and merge (or open a PR). Conflicts surface at merge time — the normal,
   reviewable place — not as silent mid-flight overwrites.
4. **Tear down when done:**
   ```
   git worktree remove ../<repo>-<branch>
   ```
   Then delete the branch if it is no longer needed.

The bundled `scripts/worktree.sh` wraps add/list/remove with safety checks
(must be inside a repo, refuses existing branches/paths, always uses a sibling
path).

## When NOT to bother

- Purely read-only parallel agents don't touch files — they don't need worktrees.
- A single sequential task doesn't either; the overhead isn't worth it.
- Reach for isolation specifically when parallel agents will **write**.

Pairs naturally with the `agent-orchestration` skill: orchestrate the fan-out,
isolate the writers.
