---
name: code-review-guidance
description: Use when the user asks to review code, a diff, or a PR for bugs, edge cases, and quality — delegates to the code-reviewer subagent via /code-review. Triggers on "review my code", "review this diff", "check before I commit", "look over my changes", "code review".
---

# Code review guidance

When the user wants their working changes reviewed for bugs, edge cases, and quality — before a commit, before opening a PR, or before handing off to a human — route it through this plugin.

## When this applies

- The user asks to review a diff, uncommitted changes, or a specific git range.
- A self-review pass is wanted after implementing a feature or fix.

## What to do

Run `/code-review` (optionally with a git ref or range like `main` or `HEAD~3`; defaults to the working diff). It dispatches the read-only `code-reviewer` subagent, which reports concise findings grouped by severity. Relay the findings.
