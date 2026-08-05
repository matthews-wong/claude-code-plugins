---
name: commit
description: Stage-aware helper that composes a Conventional Commits message for the current changes and creates the commit.
args: "[optional short intent hint, e.g. 'fix the login redirect']"
---

Create a git commit whose message follows the Conventional Commits
specification. Apply the `conventional-commits` skill for the exact grammar.

Intent hint from the user: $ARGUMENTS

Steps:

1. Inspect the working tree: run `git status --short` and `git diff --staged`.
   If nothing is staged, run `git diff` and decide with the user's hint what to
   stage; do not stage unrelated changes into one commit.

2. Determine the correct `type` (feat, fix, docs, style, refactor, perf, test,
   build, ci, chore, revert) and an optional `scope` from the files touched.

3. Write a concise, imperative subject (<= 72 chars). Add a body explaining
   *why* when the change is non-trivial. Add a `BREAKING CHANGE:` footer if any
   public contract changed.

4. Show the proposed message to the user, then create the commit with it. Do
   not push. Do not use `--no-verify`. Follow any commit-message rules in the
   project's CLAUDE.md (for example a required Co-Authored-By trailer).

If a commit-message hook rejects or warns, read the warning, correct the
message, and retry.
