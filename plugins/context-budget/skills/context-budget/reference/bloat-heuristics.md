# Bloat Heuristics (reference)

Detailed scoring for auditing always-loaded context. Load on demand.

## Token estimation

Rough estimate: `tokens ≈ words / 0.75` (≈ 1.33 tokens/word for English prose; code and tables run higher). Always label counts as estimates — do not present them as exact. The `estimate-context.sh` helper script bundled with this plugin gives a fast word/line-based estimate per file.

## Section-by-section scoring

For each section of a memory file, ask three questions:

1. **Derivable?** Could Claude obtain this by reading the repo (files, manifests, configs, CI)? If yes → CUT.
2. **Generic?** Is this something a competent model already knows (language idioms, framework basics, universal best practices)? If yes → CUT.
3. **Always relevant?** Is it needed on *every* task, or only some? If only some → move to a skill (load on demand), don't preload.

Only content that is non-derivable, non-generic, and broadly relevant earns a place in CLAUDE.md.

## CUT catalog (with the reason)

| Bloat pattern | Why cut | Where it belongs |
|---------------|---------|------------------|
| Directory / file tree listings | Claude can glob/ls | nowhere; derive live |
| Full dependency lists | in the manifest | manifest |
| Standard build/test/lint commands | in package.json / Makefile / CI | a skill, or derive |
| "Our stack is React + Node + Postgres" narration | inferable from repo | trim to one line if load-bearing |
| Restated framework/library docs | model knows or can fetch | link, don't inline |
| Generic best-practice essays (SOLID, clean code) | already known | cut |
| Long per-feature how-tos | only sometimes relevant | a triggered skill |
| Changelogs / historical notes | not needed per-turn | docs / git history |
| Duplicated content across nested CLAUDE.md files | redundant load | single source + pointer |

## KEEP catalog (with the reason)

| Keep pattern | Why keep |
|--------------|----------|
| Non-obvious gotchas ("the auth service silently caches for 5m") | not visible in code |
| Destructive-action guardrails ("never run migrations against prod DB") | safety, always relevant |
| Project-specific conventions that can't be inferred ("all money in integer cents") | prevents real errors |
| Hard constraints ("Node 18 only; do not use fetch polyfill X") | prevents wasted work |
| Skill pointers ("for deployment, use the `deploy` skill") | enables progressive disclosure |

## Worked example

**Before (always loaded, ~600 tokens):**
```
## Project structure
- src/ contains the app
- src/api/ has the routes
- src/db/ has models
  ... 30 more lines ...
## Dependencies
express, pg, zod, ... (20 lines)
## Commands
npm run build, npm test, npm run lint ...
## Gotcha
The rate limiter uses a shared Redis key; running two dev servers double-counts.
```

**After (lean CLAUDE.md, ~60 tokens):**
```
## Gotchas
- Rate limiter shares one Redis key — two dev servers double-count. Use REDIS_PREFIX to isolate.
- Money is stored in integer cents everywhere; never use floats.

For build/test/deploy specifics, the `dev-workflow` skill has them.
```
The structure, deps, and commands were removed (derivable); only the non-obvious gotcha and a skill pointer remain.

## Reporting format

Produce, per file: estimated current tokens → estimated post-trim tokens, and a KEEP/CUT table (Section | Decision | Reason | Destination). Never delete without showing a diff and confirming.
