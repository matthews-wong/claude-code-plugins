---
name: skill-list
description: List the skills available in this project and user scope and summarize what each one does and when it triggers.
---

Inventory the Claude Code skills available in the current context and summarize them.

## Step 1 — Discover skill locations

Look for `SKILL.md` files in each scope:

- **Project skills:** `.claude/skills/*/SKILL.md` in the current repo.
- **User skills:** `~/.claude/skills/*/SKILL.md`.
- **Plugin skills:** any installed plugin's `skills/*/SKILL.md` (skills contributed by
  enabled plugins).

Use file search to find them; do not assume a fixed list.

## Step 2 — Read each skill's frontmatter

For every `SKILL.md` found, read its YAML frontmatter `description` and its heading/body to
understand what it does and when it fires.

## Step 3 — Summarize as a table

Present one row per skill:

| Skill | Scope | Triggers when… | What it does |
|-------|-------|----------------|--------------|

Keep each summary to a phrase or two. Group by scope (project, user, plugin) if the list
is long.

## Step 4 — Flag issues

Call out, briefly:

- **Overlapping descriptions** — two skills that would compete for the same trigger, which
  causes ambiguous routing.
- **Weak descriptions** — ones missing a clear "when to use", which will under-trigger.
- **Gaps** — obvious capabilities the project seems to want but has no skill for.

Offer to refine any weak description or scaffold a missing skill (see `/skill-new`).
