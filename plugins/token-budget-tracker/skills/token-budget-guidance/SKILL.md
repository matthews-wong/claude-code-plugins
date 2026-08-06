---
name: token-budget-guidance
description: Use when a session feels heavy, slow, or near its context limit, or before deciding to /compact or /clear — summarizes what is filling the context window and gives concrete steps to trim it. Points to /token-budget. Triggers on "context is full", "session feels slow", "running out of context", "should I compact or clear", "token budget", "trim context".
---

# Token-budget guidance

When the user's session feels heavy or near its context limit, or they are deciding whether to `/compact` or `/clear`, route it through this plugin.

## When this applies

- The user reports the session is slow, heavy, or near the context limit.
- The user asks what is filling the context window or how to trim it.

## What to do

Run `/token-budget`. It summarizes what is consuming the context window (from `/context`) and gives prioritized, concrete steps to trim it and stay within budget. This plugin also installs a non-blocking hook that periodically nudges the user to check `/context`.
