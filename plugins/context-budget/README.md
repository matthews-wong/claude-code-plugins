# context-budget

The flagship context-engineering plugin. Keeps always-loaded context **lean** so the token budget goes to the task, not to memory files — by auditing `CLAUDE.md` and skills for bloat and restructuring heavy guidance into on-demand skills via **progressive disclosure**.

## Why it exists

Claude Code loads context in tiers:

- `CLAUDE.md` is loaded **every turn** — expensive real estate.
- Skills cost only their `name` + `description` (~a few dozen tokens) until their description matches the task; only then does the `SKILL.md` body load.
- `reference/*.md` files load only when a skill reads them.

A bloated, always-loaded memory file wastes budget on every turn AND adds noise that degrades routing. This plugin finds that bloat and moves depth down to the tier where it pays for itself.

## Components

- **`/context-audit [path]`** — inventories memory files and skills, estimates token weight, flags bloat (dir listings, dep lists, standard commands, generic advice — anything derivable from the repo), and proposes a lean CLAUDE.md plus on-demand skills. Shows a diff before changing anything.
- **`context-budget` skill** — triggers when a CLAUDE.md feels long, when writing/reviewing skills, or when asked to cut context. Lean body; detailed heuristics in `reference/bloat-heuristics.md` and `reference/progressive-disclosure.md` (the plugin practices what it preaches).
- **SessionStart hook** — `scripts/estimate-context.sh` prints a non-blocking, advisory estimate of always-loaded memory-file weight and nudges toward `/context-audit` when it's heavy. Never edits files; always exits 0.

## Usage

```
/context-audit
/context-audit CLAUDE.md
```

## Notes

Token counts are labeled estimates, never presented as exact. Recommendations are grounded in real Claude Code loading behavior. No content is deleted without showing a diff and confirming.

MIT licensed. Author: Matthews Wong.
