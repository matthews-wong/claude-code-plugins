# code-review-agent

A dedicated code-review subagent plus a slash command to invoke it. It reviews
your **working git diff** for bugs, edge cases, and quality issues and reports
concise, actionable findings — the "Step 2: review" that follows "Step 1: verify."

## What it installs

- **Subagent `code-reviewer`** (`agents/code-reviewer.md`) — a read-only reviewer
  (tools: Read, Grep, Glob, Bash) that gathers the diff via `git`, reads the
  surrounding code for context, and reports findings grouped by severity.
- **Command `/code-review`** — delegates the review to the subagent and presents
  its findings. Accepts an optional git range argument.

## How to use

- Run `/code-review` to review the current working changes (staged + unstaged),
  falling back to the last commit if the tree is clean.
- Run `/code-review main` (or any ref/range) to review a specific range.

Because the reviewer runs as a separate subagent with its own context window, the
review does not clutter your main conversation, and it uses only read tools so it
never modifies your code.

## Notes

- The subagent uses `git` via the Bash tool to obtain the diff; run it inside a git
  repository.
- Reviews are advisory — Claude reports findings; addressing them is a separate,
  explicit step.
