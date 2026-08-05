#!/bin/sh
# worktree.sh — create, list, or remove a git worktree for isolated agent work.
# POSIX sh. Usage:
#   worktree.sh add <branch>      create ../<repo>-<branch> on new branch <branch>
#   worktree.sh list              list all worktrees
#   worktree.sh remove <branch>   remove the worktree for <branch>
set -eu

die() {
  echo "worktree.sh: $1" >&2
  exit 1
}

# Ensure we are inside a git repository and operate from its top level.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "not inside a git repository"
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
repo_name=$(basename "$repo_root")

cmd=${1:-}
[ -n "$cmd" ] || die "usage: worktree.sh {add <branch>|list|remove <branch>}"

case "$cmd" in
  add)
    branch=${2:-}
    [ -n "$branch" ] || die "usage: worktree.sh add <branch>"
    if git show-ref --verify --quiet "refs/heads/$branch"; then
      die "branch '$branch' already exists; choose another name"
    fi
    # Sibling directory so the isolated checkout never nests in the main tree.
    target="../${repo_name}-${branch}"
    if [ -e "$target" ]; then
      die "path '$target' already exists"
    fi
    git worktree add "$target" -b "$branch"
    echo "created worktree at: $target (branch: $branch)"
    echo "cd into it to work in isolation."
    ;;
  list)
    git worktree list
    ;;
  remove)
    branch=${2:-}
    [ -n "$branch" ] || die "usage: worktree.sh remove <branch>"
    target="../${repo_name}-${branch}"
    [ -d "$target" ] || die "no worktree found at '$target'"
    git worktree remove "$target"
    echo "removed worktree: $target"
    echo "note: branch '$branch' is kept; delete it with 'git branch -d $branch' if no longer needed."
    ;;
  *)
    die "unknown command '$cmd'; use add, list, or remove"
    ;;
esac
