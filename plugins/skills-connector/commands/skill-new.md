---
name: skill-new
description: Scaffold a new skill directory with a well-formed SKILL.md from a name and description.
args: "<skill-name> — <what it does and when to use it>"
---

Scaffold a new Claude Code skill from: $ARGUMENTS

## Step 1 — Parse and validate the inputs

- Derive the **skill name** as kebab-case (lowercase, hyphen-separated). If the user gave
  a title or spaces, convert it. Reject names that aren't a clean single capability.
- Capture the intended **purpose and trigger** from the rest of the input. If the user
  gave only a name with no sense of when it should fire, ask one short question to get the
  trigger — the description depends on it.

## Step 2 — Choose the scope

Ask (or infer from context) where the skill belongs:

- `.claude/skills/<name>/` — project scope, shared with the team via the repo (default).
- `~/.claude/skills/<name>/` — user scope, personal and cross-project.

## Step 3 — Write a routing-friendly description

Craft the frontmatter `description` so it states **what** the skill does and **when** to
use it, in the user's vocabulary, with concrete cues (tasks, verbs, file types, phrasings).
Lead with "Use when …". Keep it to one coherent capability — no unrelated "and". This is
the routing signal, so it matters most.

## Step 4 — Create the files

Create `<scope>/skills/<name>/SKILL.md` with valid YAML frontmatter and a starter body:

```markdown
---
description: <the description from step 3>
---

# <Human Readable Name>

<One-sentence purpose.>

## When to use

- <trigger situation 1>
- <trigger situation 2>

## Steps

1. <first instruction>
2. <second instruction>

## Notes

- <hard rules, constraints, or references to sibling skills by name/path>
```

Fill the placeholders with real, specific content inferred from the user's intent — do not
leave literal angle-bracket placeholders behind. Keep the body skimmable and imperative.

## Step 5 — Confirm

Show the created path and the final SKILL.md. Note that its `description` is what triggers
the skill, and suggest refining it if the trigger phrasing could be sharper.
