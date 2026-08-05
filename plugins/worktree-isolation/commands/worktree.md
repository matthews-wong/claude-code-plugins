---
name: worktree
description: Use when parallel or agent work needs an isolated checkout — create, list, or remove a git worktree (sibling directory on its own branch) so edits never collide with the main working tree.
args: "[add <branch> | list | remove <branch>]"
---

Manage git worktrees for isolated agent work. Arguments: `$ARGUMENTS`

A git worktree is a second working directory backed by the same repository,
checked out to its own branch. It lets a separate agent (or a parallel task)
build and edit in isolation without touching the main checkout — the antidote to
two agents fighting over the same files. See the `worktree-isolation` skill for
the reasoning.

Use the bundled helper script at `${CLAUDE_PLUGIN_ROOT}/scripts/worktree.sh`,
which wraps the raw git commands safely. Interpret `$ARGUMENTS`:

- **add `<branch>`** — create a new worktree on a new branch:
  ```
  sh "${CLAUDE_PLUGIN_ROOT}/scripts/worktree.sh" add <branch>
  ```
  This runs `git worktree add ../<repo>-<branch> -b <branch>` from the repo root,
  creating a sibling directory so the isolated checkout never nests inside the
  original.

- **list** — show all worktrees for this repo:
  ```
  sh "${CLAUDE_PLUGIN_ROOT}/scripts/worktree.sh" list
  ```

- **remove `<branch>`** — tear down a worktree when its work is merged or
  abandoned:
  ```
  sh "${CLAUDE_PLUGIN_ROOT}/scripts/worktree.sh" remove <branch>
  ```

Before acting:
- Confirm the current directory is inside a git repository.
- For `add`, make sure the branch name does not already exist; if it does,
  suggest a different name rather than clobbering it.
- Never create a worktree path inside the repo working tree — always a sibling.

After acting, report the worktree path so the user (or a subagent) can `cd` into
it. When multiple agents run in parallel, give each its own worktree and merge
the branches back through normal review once each finishes.
