---
name: simplification-guidance
description: Use when the user wants to simplify or clean up recently-written code without changing behavior — remove dead code, reduce indirection, prefer deleting lines over adding. Delegates to the code-simplifier subagent via /simplify. Triggers on "simplify", "clean this up", "reduce indirection", "remove dead code", "make it simpler".
---

# Simplification guidance

When the user wants the code that was just written or changed made simpler — as a finishing pass after a feature or fix — route it through this plugin.

## When this applies

- The user asks to simplify, clean up, or reduce indirection in recent changes.
- A behavior-preserving cleanup of the working diff is wanted before review or commit.

## What to do

Run `/simplify`. It dispatches the `code-simplifier` subagent, which reviews the recently-changed code and applies behavior-preserving simplifications, favoring deleting lines over adding them. This is a quality cleanup, not a bug hunt — use the code-review capability for correctness.
