---
name: onboarding-guidance
description: Use when the user is new to an unfamiliar repository and needs to get productive fast — mapping the stack, entry points, build/test/run commands, conventions, and gotchas. Delegates to the repo-onboarder subagent via /onboard. Triggers on "onboard me", "get me up to speed on this repo", "how does this codebase work", "explore this repo", "where do I start".
---

# Onboarding guidance

When the user needs a fast, grounded picture of an unfamiliar codebase before working in it, route it through this plugin.

## When this applies

- The user is new to the repo and asks how it is structured or how to build/test/run it.
- A quick map of stack, entry points, conventions, and gotchas is wanted.

## What to do

Run `/onboard`. It dispatches the read-only `repo-onboarder` subagent, which explores the codebase and writes an `ONBOARDING.md` covering stack, entry points, build/test/run, conventions, and gotchas. Point the user at that file.
