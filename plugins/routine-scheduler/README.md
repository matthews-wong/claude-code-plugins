# routine-scheduler

Orchestration plugin for Claude Code. Define scheduled routines — cron-style
cloud agents that run a task on a recurring cadence without a human starting the
session.

## Components

- **Command `/schedule-routine`** — walks through defining a routine's contract,
  cadence, guardrails, and self-contained task prompt, then registers it via
  Claude Code's native scheduling capability.
- **Skill `routine-scheduler`** — what makes a routine reliable (unambiguous,
  idempotent, bounded, read-biased, fail-safe), cadence selection, and worked
  examples for nightly PR triage and weekly dependency-update checks.

## Usage

```
/schedule-routine triage new PRs every night at 3am and label them
```

## How scheduling really works

Claude Code manages scheduled cloud agents through a native routines capability
(the `schedule` skill / scheduled-agents interface). This plugin drives that
capability rather than inventing cron plumbing. For version-specific options,
see the official Claude Code documentation.

Author: Matthews Wong · License: MIT
