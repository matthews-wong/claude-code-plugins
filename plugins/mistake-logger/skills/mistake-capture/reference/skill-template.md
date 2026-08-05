# Skill template

Copy this into `.claude/skills/<kebab-name>/SKILL.md` when a mistake turns out to be a repeatable procedure.

```markdown
---
name: <kebab-name>
description: Use when <situation the procedure applies to>. Triggers on "<keyword>", "<keyword>", "<keyword>".
---

# <Human-readable title>

<One or two sentences: what this procedure is for and when it matters.>

## Steps

1. <First step — imperative.>
2. <Next step.>
3. <...>

## Gotchas

- <The specific thing that went wrong last time, stated as a warning.>
```

## Rules for a good `description:`

- Start with "Use when…" and name the concrete situation.
- Include the literal keywords a future request would contain — the trigger is matched against intent, so be explicit.
- Don't describe the mechanics; describe the *moment* the skill should fire.

## When to add `reference/`

- Keep `SKILL.md` under roughly 1500 tokens.
- If the procedure needs long examples, tables, command dumps, or edge-case catalogs, move them into `reference/<topic>.md` and point to them from the body (progressive disclosure). The body stays scannable; the depth loads only if needed.
