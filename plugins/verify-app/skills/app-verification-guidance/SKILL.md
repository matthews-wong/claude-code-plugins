---
name: app-verification-guidance
description: Use when the user wants to confirm a change actually works end to end — run the app or build, exercise the happy path and key flows, and get PASS/FAIL with real captured evidence. Delegates to the verify-app subagent via /verify-app. Triggers on "verify the app", "prove it works", "run the happy path", "did the build pass", "confirm it works before I'm done".
---

# App-verification guidance

When the user wants proof that a change actually works end to end — not just a bare assertion of success — route it through this plugin.

## When this applies

- After implementing a feature or fix, before declaring a task done.
- The user asks to verify, confirm it works, run the app, or run the happy path.

## What to do

Run `/verify-app`. It dispatches the `verify-app` subagent, which runs the app or build, exercises real flows (happy path plus a key edge case), captures the actual output as evidence, and reports PASS or FAIL. Never report success without the captured evidence it returns.
