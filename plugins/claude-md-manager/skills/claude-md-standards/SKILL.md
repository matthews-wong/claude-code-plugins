---
name: claude-md-standards
description: Use when creating, reviewing, or editing a CLAUDE.md (or nested CLAUDE.md) file. Defines what belongs in project memory versus what is derivable bloat — high-value build/test commands, conventions, gotchas, and safety rules — and how to keep it lean and skimmable.
---

# CLAUDE.md Standards

`CLAUDE.md` is persistent project memory Claude Code loads as context. Its value is
inversely related to its length: it should carry only what Claude cannot cheaply discover
by reading the repo, and nothing it can. Every line costs context budget on every session.

## The core test

For each candidate line ask: **could Claude derive this by reading the code?** If yes,
cut it. If it saves real time or prevents a real mistake, keep it.

## What belongs

- **Commands** — exact build/test/lint/run invocations, especially non-obvious ones: how
  to run a single test, required env vars, the actual dev command.
- **Conventions** — project-specific choices not obvious at a glance (naming, module
  boundaries, error handling, commit style). Brief.
- **Gotchas** — non-obvious constraints and footguns: "don't touch X because Y",
  load-bearing quirks, generated files not to edit by hand.
- **Safety rules** — hard "never do this" boundaries (prod migrations, secrets, deleting
  data) that must hold regardless of task.
- **Architecture orientation** — a few sentences on where major pieces live, only where
  the layout is not self-evident.

## What does not belong

- Full dependency lists, file trees, or version numbers the tooling already reports.
- Generic engineering best practices that apply to every project.
- Long prose re-explaining code the code already makes clear.
- Stale commands or conventions that no longer match the repo.
- Vague, unactionable guidance ("be careful", "write good code").

## Structure

- Short sections with bullet lists; a developer should skim it in about a minute.
- Lead with commands, then conventions, then gotchas, then safety.
- Nested `CLAUDE.md` files can live in subdirectories for area-specific context; keep each
  scoped to its directory and non-duplicative of the root.
- Prefer editing the existing file over rewriting; preserve high-value content.

## Layering with global memory

User-level `~/.claude/CLAUDE.md` holds cross-project personal rules. Project `CLAUDE.md`
should not duplicate those — capture only what's specific to this repo. When in doubt,
push universal rules up to user scope and keep the project file about the project.

## Review loop

When linting an existing file, cross-check every command and convention against the actual
repo, flag derivable/generic/stale/bloated/vague lines with a concrete action each, and
note any missing high-value context before proposing the trimmed version.
