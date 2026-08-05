# skills-connector

The flagship plugin for building an agentic **skills library** in Claude Code. Author
well-formed skills, write frontmatter descriptions that route reliably, and connect skills
so they compose instead of collide.

## What it does

- Teaches the anatomy of a skill (`SKILL.md`, frontmatter, `references/`, `scripts/`).
- Shows how to write a `description` that drives routing — stating what AND when.
- Guides when to split a skill and how to reference sibling skills.
- Scaffolds new skills and inventories the ones you already have.

## Components

- **Skill:** `skills-connector` — the authoring-and-connecting reference, applied whenever
  you're building or organizing skills.
- **Command:** `/skill-new <name> — <what/when>` — scaffold a new skill directory with a
  well-formed `SKILL.md`.
- **Command:** `/skill-list` — list project/user/plugin skills, summarize each, and flag
  overlapping or weak descriptions.

## Usage

- `/skill-new sql-migrations — use when writing or ordering Postgres schema migrations`
  scaffolds `.claude/skills/sql-migrations/SKILL.md` with a routing-friendly description.
- `/skill-list` gives you a table of every available skill and where its routing is weak.

## Scopes

Project skills live in `.claude/skills/`, personal skills in `~/.claude/skills/`, and
plugin skills ship inside plugins. Project scope wins for team-shared, repo-specific
capabilities; user scope for personal cross-project ones.

Author: Matthews Wong · License: MIT
