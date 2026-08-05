---
name: mistake-capture
description: Use when turning a mistake, correction, or repeated error into a durable rule that persists across sessions. Decides whether the lesson belongs as a lean line in CLAUDE.md (one-off fact/constraint) or as a skill (repeatable procedure), and keeps CLAUDE.md lean. Triggers on "preserve this mistake", "log a lesson", "don't repeat this", "add a rule", "when to make a skill vs CLAUDE.md".
---

# Mistake capture

Agents forget between sessions; files do not. When Claude makes a mistake and gets corrected, that correction is lost unless you write it down somewhere that loads into future sessions. This is how the agent "learns" over time (Boris Cherny's preserve-mistakes loop): a corrected mistake becomes a persistent rule.

## The decision: CLAUDE.md line vs. skill

Ask: *is this a fact, or a procedure?*

- **One-off fact or constraint** → one line in `CLAUDE.md`. Examples: "This repo uses pnpm, not npm." "The API base URL lives in `config/env.ts`, never hard-code it." "Run `make fmt` before committing." These are always-on, short, and cheap to keep loaded.
- **Repeatable multi-step procedure** → a **skill**. Examples: "How to add a database migration here." "The release checklist." "How to wire a new feature flag." These are too long for CLAUDE.md and only relevant sometimes — a skill's `description:` trigger loads them on demand.

Rule of thumb: if it fits in one imperative sentence and should apply to every task, it's a CLAUDE.md line. If it has steps, ordering, or conditional branches, it's a skill.

## Keep CLAUDE.md lean

CLAUDE.md loads on every turn, so every line costs context budget on every task. Protect it:

- One line per rule. No paragraphs, no rationale essays — the *why* can be a short clause, not a section.
- Before adding, read the file and check the rule isn't already there or contradicted. Tighten an existing rule instead of adding a near-duplicate.
- Phrase as an imperative: "Always…", "Never…", "Prefer X over Y."
- Put it under the most fitting existing heading; don't invent structure for a single line.
- If CLAUDE.md is getting long, that's a signal to migrate procedures out into skills.

## Writing a good rule

A durable rule is **general, actionable, and specific enough to act on**. Convert the one-time incident into the reusable principle:

- Bad (too specific): "Don't pass `--force` to the deploy script on Tuesday."
- Bad (too vague): "Be more careful with deploys."
- Good: "Never pass `--force` to `deploy.sh` without confirming with the user — it skips the migration guard."

## Choosing the CLAUDE.md scope

- **Project** (`./CLAUDE.md`) — the default. Rules about this codebase, its tooling, its conventions.
- **User** (`~/.claude/CLAUDE.md`) — only for genuinely cross-project preferences. Don't pollute the global file with repo-specific facts.

## Scaffolding a skill from a mistake

When the lesson is a procedure, create `.claude/skills/<kebab-name>/SKILL.md`:

- `description:` must be a precise trigger with concrete keywords so it activates at the right moment.
- Keep the body lean; push long reference material to `reference/*.md`.

See `reference/skill-template.md` for a copy-paste starting point and `reference/examples.md` for worked before/after conversions.
