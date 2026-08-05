# token-budget-tracker

Cost and governance plugin for Claude Code. A lightweight, non-blocking reminder
to stay aware of your session's token budget, plus a command to summarize usage
and suggest where to trim context.

## Components

- **Hook (`SessionStart`)** — runs `scripts/token-report.sh`, which prints a
  short nudge to check `/context` and `/token-budget`. It makes no network
  calls, mutates nothing, and always exits 0, so it can never block a session.
- **Command `/token-budget`** — summarizes what is filling the context window
  (based on Claude Code's built-in `/context`) and gives prioritized trimming
  suggestions.

## How it works

On session start the hook emits a friendly reminder. The authoritative usage
data comes from Claude Code's own `/context` command — this plugin surfaces
awareness and hygiene advice rather than inventing token counts.

Optional: set `TOKEN_BUDGET_HINT` in your environment to customize the budget
note shown by the hook.

## Usage

```
/token-budget
```

Author: Matthews Wong · License: MIT
