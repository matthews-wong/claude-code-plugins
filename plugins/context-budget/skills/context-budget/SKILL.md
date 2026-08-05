---
name: context-budget
description: Audit and slim CLAUDE.md and skills for token bloat, and restructure guidance via progressive disclosure. Use when a CLAUDE.md or memory file feels long, when writing or reviewing SKILL.md files, when the user asks to reduce context, cut bloat, improve routing, or apply progressive disclosure. Triggers on "CLAUDE.md too long", "context bloat", "trim context", "token budget", "progressive disclosure", "lean context", "skill not triggering".
---

# Context Budget

Keep always-loaded context small so the budget goes to work, not to memory files. Move depth into skills that load on demand.

## The core mechanics (why this matters)

- **CLAUDE.md is loaded every turn.** Every token in it is spent continuously and can crowd out task tokens and blur routing. Treat it as expensive real estate.
- **Skills are cheap until used.** Claude sees only a skill's `name` + `description` (~a few dozen tokens) until the description matches the task; only then is the `SKILL.md` body loaded. This is progressive disclosure.
- **SKILL.md should stay under ~2000 tokens.** Push detail into `reference/*.md` files the skill links to and reads on demand.
- A bloated, always-loaded memory file wastes budget AND degrades routing (more noise for the model to match against).

## KEEP vs CUT (the heuristic)

**KEEP in CLAUDE.md** (non-derivable, always-relevant):
- Gotchas and footguns that aren't visible from the code.
- Safety rules and destructive-action guardrails.
- Project-specific conventions that cannot be inferred by reading the repo.
- One-line pointers to skills ("for X, the `foo` skill covers it").

**CUT from CLAUDE.md** (derivable or generic — Claude can get it from the repo or already knows it):
- Directory/file trees and file listings — Claude can `ls`/glob.
- Dependency lists — they're in the manifest.
- Standard build/test/lint commands — discoverable from package.json / Makefile / CI.
- Restating framework or language docs, or generic best practices.
- Long onboarding prose better placed in a skill.

Rule of thumb: *if Claude could derive it by looking at the repo, don't preload it.*

## Restructure via progressive disclosure

1. Lean CLAUDE.md = KEEP content + skill pointers only.
2. Task-specific / heavy guidance → a skill (loads on trigger).
3. Deep reference detail → `reference/*.md` under the skill (loads only when the skill reads it).

This skill applies the principle to itself: the detailed heuristics live in references, not here.

## References (load on demand)

- `reference/bloat-heuristics.md` — full CUT/KEEP catalog, section-by-section scoring, token estimation, and worked before/after examples.
- `reference/progressive-disclosure.md` — how skill routing and loading actually work, writing high-signal descriptions, and the CLAUDE.md → skill → reference layering pattern.
