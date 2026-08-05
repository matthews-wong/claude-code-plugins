# worktree-isolation

Run parallel agents without merge chaos. This plugin manages `git worktree`
checkouts so each agent works in its own directory on its own branch, backed by
the same repository, then merges back through normal review.

## Components
- `commands/worktree.md` — `/worktree add|list|remove <branch>`.
- `scripts/worktree.sh` — POSIX sh helper wrapping `git worktree` with safety
  checks (must be in a repo, refuses existing branches/paths, sibling paths only).
- `skills/worktree-isolation/SKILL.md` — when and why to isolate parallel writers.

## Core command
```
git worktree add ../<repo>-<branch> -b <branch>
```
A worktree is a second working directory on its own branch sharing one object
store — lighter than a clone, and the clean way to keep concurrent agents from
overwriting each other's files.

## Usage
```
/worktree add feature-auth
/worktree list
/worktree remove feature-auth
```

Author: Matthews Wong — MIT License.
