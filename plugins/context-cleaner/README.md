# context-cleaner

Keeps Claude Code sessions healthy by recognizing when context has gone bad and recommending the right reset.

Packages "**Manage your session**" and "**Avoid common failure patterns**" from Anthropic's *Claude Code best practices* guide. Context is a limited shared resource; a polluted session reasons worse, and knowing when to `/clear`, `/compact`, or delegate is a core skill.

## What's inside

- `commands/clear-check.md` — `/clear-check` diagnoses the current session against the three failure patterns and recommends keep-going / `/compact` / `/clear` + re-prompt, drafting the re-prompt when a reset is warranted.
- `skills/context-hygiene/` — the pattern catalog and re-prompt recipe, with detailed symptoms and worked before/after examples under `reference/`.

## The three patterns

1. **Kitchen-sink session** — unrelated tasks piled into one context → `/clear` between tasks.
2. **Correcting over and over** — after ~2 failed corrections, stop patching → `/clear` and re-prompt with what you learned.
3. **Infinite exploration** — endless searching → scope it to a subagent, or `/compact` a long coherent task.

## Usage

```
/clear-check we've been going in circles on this bug for a while
```
