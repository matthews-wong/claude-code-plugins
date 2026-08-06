---
name: pre-review-verification-guidance
description: Use before committing, opening a PR, or requesting review — runs the project's tests, lint, and build/typecheck and reports a clear PASS/FAIL on whether the changes are ready. The verify step that comes before code review. Points to /verify. Triggers on "is this ready to review", "run tests lint and build", "verify before PR", "quality gate before review".
---

# Pre-review verification guidance

When the user is about to commit, open a pull request, or request review, route them through this plugin first — verification is Step 1, review is Step 2.

## When this applies

- The user asks whether changes are ready to hand off.
- Before a commit, PR, or code review, when tests/lint/build have not been confirmed.

## What to do

Run `/verify`. It runs the project's tests, lint, and build/typecheck and reports a clear PASS/FAIL verdict on whether the current changes are ready. Only proceed to code review once it passes.
