---
name: context-audit
description: Audit CLAUDE.md and skills for bloat and restructure them into a lean core plus on-demand skills (progressive disclosure).
args: "[path] — optional CLAUDE.md or skills dir to audit (default: repo CLAUDE.md and .claude/skills)"
---

Audit this project's always-loaded context for bloat and propose a leaner, progressively-disclosed structure. Target: `$ARGUMENTS` (default: the repo's `CLAUDE.md`, any nested `CLAUDE.md`, and skill `SKILL.md` files under `.claude/skills/`).

Load the `context-budget` skill first — it holds the principles and points to the detailed heuristics.

Procedure:

1. **Inventory.** Find every always-loaded memory file (`CLAUDE.md` at repo root and subdirs, `~/.claude/CLAUDE.md` if in scope) and each `SKILL.md`. Estimate the token weight of each (roughly words / 0.75).

2. **Flag bloat.** For each memory file, classify every section as KEEP or CUT using the skill's heuristics. CUT candidates: directory/file listings, dependency lists, standard build/test commands, restating framework docs, generic best-practices Claude already knows, anything derivable by reading the repo. KEEP: non-obvious gotchas, safety/destructive-action rules, project-specific conventions that can't be inferred, and pointers to skills.

3. **Check skills.** Flag any `SKILL.md` over ~2000 tokens or with a vague `description`. The description must contain a precise trigger + keywords (that is what routing sees). Recommend moving depth into `reference/*.md`.

4. **Restructure via progressive disclosure.** Propose: (a) a lean CLAUDE.md keeping only KEEP content plus one-line skill pointers; (b) task-specific/heavy guidance relocated into skills that load on demand; (c) deep detail pushed into `reference/` files each skill links to.

5. **Output** a report: current vs. estimated post-trim token weight per file; a KEEP/CUT table with rationale per section; and the concrete restructure plan. Offer to apply it (rewrite CLAUDE.md, create/split skills) — but never delete content without showing the diff and asking first.

Ground every recommendation in real routing behavior: skills cost only name+description (~a few dozen tokens) until triggered, while everything in CLAUDE.md is loaded on every turn and spends budget continuously. Do not fabricate token counts — label them as estimates.
