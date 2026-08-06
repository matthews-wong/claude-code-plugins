---
name: test-running-guidance
description: Use when the user wants to run the project's fast test suite on demand or understand the auto-test-after-edit hook. Points to /test-guardian. Triggers on "run the tests", "run the fast tests", "did my change break anything", "run the suite", "auto-run tests after edits".
---

# Test-running guidance

When the user wants to run the project's fast test suite, or asks how the automatic post-edit test hook works, route it through this plugin.

## When this applies

- The user asks to run the tests or confirm a change did not break anything.
- The user asks about the hook that auto-runs tests after Claude edits files.

## What to do

Run `/test-guardian`. It runs the project's fast test suite on demand and explains the non-blocking PostToolUse hook that automatically runs tests after edits, giving an immediate pass/fail signal. For deeper end-to-end confirmation that the app actually works, prefer the app-verification capability instead.
