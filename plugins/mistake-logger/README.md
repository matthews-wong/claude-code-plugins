# mistake-logger

A Claude Code plugin that preserves mistakes so the agent learns across sessions — modeled on Boris Cherny's practice of writing a lesson into `CLAUDE.md` or a skill when Claude makes a repeated mistake, so the fix persists into future sessions.

Agents forget between sessions; files do not.

## Components

- **`commands/log-lesson.md`** — `/log-lesson` captures what just went wrong and writes a durable rule: a lean line in `CLAUDE.md` for a one-off fact, or a scaffolded skill for a repeatable procedure.
- **`skills/mistake-capture/SKILL.md`** — the decision logic for turning a mistake into a durable rule, with a bias toward keeping `CLAUDE.md` lean. Depth lives in `reference/skill-template.md` and `reference/examples.md`.

## The core rule

Ask: *is this a fact, or a procedure?*

- **Fact / constraint** → one imperative line in `CLAUDE.md`.
- **Repeatable procedure** → a skill under `.claude/skills/<name>/SKILL.md`.

## Usage

Right after a mistake or correction:

```
/log-lesson
```

## License

MIT © Matthews Wong
