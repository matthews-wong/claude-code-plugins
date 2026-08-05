# Worked example: `conventional-commit-writer`

This directory is a **complete, correct skill you can copy** as a starting template — not a
live skill of the `skills-connector` plugin. It sits under `reference/` deliberately so it
is not discovered and loaded as its own skill.

## What it demonstrates

- A `description` written as a **trigger** — leads with "Use when…", names concrete cues
  ("commit message", "conventional commit", a commitlint failure) so it routes reliably.
- A **lean body** that leads with the procedure and states hard rules explicitly.
- **Progressive disclosure** — the exhaustive type table lives in
  `reference/commit-types.md` and is pointed to from the body, so it loads only on demand.

## Structure

```
conventional-commit-writer/     (copy this as skills/conventional-commit-writer/)
  SKILL.md
  reference/
    commit-types.md
```

## To reuse it

1. Copy this folder to `.claude/skills/conventional-commit-writer/` (project scope) or
   `~/.claude/skills/conventional-commit-writer/` (user scope).
2. Adjust the `description` and rules to your team's convention.
3. Run `/reload-plugins` (or restart), then fire-test it with a real commit request.
