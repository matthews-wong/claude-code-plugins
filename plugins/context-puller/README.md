# context-puller

Gather the right context before you act. This plugin runs a bounded discovery
pass over a repository — README, `docs/`, ADRs, the modules related to your
task, and recent git history — and distills it into a short **Working Brief** so
the agent starts grounded instead of guessing.

## Components
- `commands/pull-context.md` — `/pull-context [task]` builds the brief.
- `skills/context-pull/SKILL.md` — the reusable gathering-and-summarizing method.

## Usage
```
/pull-context add rate limiting to the public API
```
The command produces a one-page brief (goal, relevant files, how it fits
together, conventions, recent activity, risks) and can seed the durable parts
into `CLAUDE.md`.

Author: Matthews Wong — MIT License.
