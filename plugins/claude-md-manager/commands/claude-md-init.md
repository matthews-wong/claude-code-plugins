---
name: claude-md-init
description: Scaffold a strong, lean project CLAUDE.md — build/test commands, conventions, gotchas, and safety rules — without content Claude can already derive from the repo.
---

Create a focused `CLAUDE.md` at the project root that gives Claude Code the context it
cannot cheaply discover on its own.

## Step 1 — Learn the project first

Inspect the repo before writing: package manifests and lockfiles, scripts, CI config,
existing docs, directory layout, test setup, linter/formatter config. Extract the real
commands and conventions rather than guessing.

## Step 2 — Write only high-value, non-derivable content

A good CLAUDE.md is lean. Include things that save Claude time or prevent mistakes; omit
anything it can trivially read from the code.

Include:

- **Build / test / lint commands** — the exact invocations, especially non-obvious ones
  (how to run a single test, the real dev server command, required env setup).
- **Conventions** — project-specific choices not obvious from a glance (naming, module
  boundaries, error-handling patterns, commit style) — briefly.
- **Gotchas** — non-obvious constraints, footguns, load-bearing quirks, "don't touch X
  because Y".
- **Safety rules** — what must never happen (e.g. never run migrations against prod,
  never commit secrets, never edit generated files).
- **Architecture orientation** — a few sentences on where major pieces live, only where
  the layout isn't self-evident.

Omit (derivable or bloat):

- Restating the full dependency list, file tree, or language versions the tooling reports.
- Generic best practices that apply to every project.
- Long prose explanations of code that the code already makes clear.

## Step 3 — Keep it lean and skimmable

Use short sections and bullet lists. Aim for something a developer reads in a minute.
Every line should earn its place — if it's derivable or generic, cut it.

## Step 4 — Write and confirm

If a `CLAUDE.md` already exists, do not overwrite blindly — offer to merge, and suggest
running `/claude-md-lint` on the result. Show the drafted file and confirm before writing.

Suggested skeleton:

```markdown
# <Project Name>

## Commands
- Build: ...
- Test: ...            # and how to run a single test
- Lint/format: ...
- Dev/run: ...

## Conventions
- ...

## Gotchas
- ...

## Safety
- Never ...
```
