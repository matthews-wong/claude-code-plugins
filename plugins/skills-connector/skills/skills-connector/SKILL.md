---
description: Use when authoring, structuring, or debugging Claude Code skills — writing a SKILL.md, crafting the frontmatter description that drives model routing, fixing a skill that isn't triggering when it should, deciding when to split one skill into several, referencing sibling skills, or organizing a coherent agentic skills library. The reference for building skills that reliably trigger and compose.
---

# Skills Connector

Skills are model-invoked capabilities: a folder with a `SKILL.md` whose YAML frontmatter
`description` is what Claude reads to decide, on its own, whether to load the skill for the
current task. Get the description right and the skill fires when it should; get the body
right and it actually helps once loaded.

This skill practices what it teaches: the body below stays lean, and the depth lives in
`reference/` files loaded only when you need them (progressive disclosure).

## The one rule that matters most

A **vague description is the #1 reason a skill fails to fire.** The description is a
trigger, not a title — it must say **what** the skill does and, critically, **when** to use
it, in the user's own vocabulary, with concrete cues (tasks, verbs, file types, phrasings).

Weak: `Helps with database stuff.`
Strong: `Use when writing, reviewing, or optimizing SQL queries or schema migrations for
Postgres — covers indexing, query plans, and safe migration ordering.`

See `reference/descriptions.md` for a full BAD-vs-GOOD table and the rewrite recipe.

## Anatomy of a skill

```
skills/
  <skill-name>/
    SKILL.md        # required: YAML frontmatter (name, description) + instruction body
    reference/      # optional: deeper docs, loaded on demand
    scripts/        # optional: helper scripts the skill can run
```

`description` is the only required frontmatter field and the single most important one — it
is the routing signal. Everything below the frontmatter is loaded only after the skill
triggers. Keep the folder name kebab-case and matching the skill's identity.

See `reference/skill-anatomy.md` for the exact frontmatter fields plus a minimal and a
fuller worked structure.

## Writing the body

- Lead with the core procedure or checklist; put the highest-value guidance first.
- Prefer imperative, skimmable instructions over prose — headings, short lists, small
  examples.
- State hard rules explicitly (must/never, safety constraints).
- Keep it focused: one coherent capability, not a manual. Offload depth to `reference/` and
  heavy logic to `scripts/`, and point to them by path so they load only when needed.

## When to split a skill

Split when one skill starts serving two different trigger situations or grows past a single
coherent capability. Signs: the description needs "and" to cover unrelated situations; parts
of the body only apply to some invocations; two distinct user intents each want half the
file. Prefer several tightly-scoped skills over one sprawling one — narrow descriptions
route more reliably and load less irrelevant context.

## Connecting skills to each other

Skills compose into a library:

- **Reference by name and path** — from one body, point to a sibling: "For migration
  ordering, use the `sql-migrations` skill."
- **Keep responsibilities non-overlapping** — overlapping descriptions cause ambiguous
  routing; give each skill a clear lane.
- **Establish a hub** — one "standards" skill others reference avoids duplicating rules.
- **Layer scope deliberately** — personal skills in `~/.claude/skills/`, project skills in
  `.claude/skills/`, plugin skills ship inside a plugin. Project scope wins for team-shared,
  repo-specific capability; user scope for personal cross-project ones.

## Before you ship

Run the full pre-ship checklist in `reference/authoring-checklist.md` — single purpose,
description as a trigger, lean SKILL.md, depth in `reference/`, `/plugin validate`, and a
`/reload-plugins` fire test.

## A complete example to copy

`reference/worked-example/` is a full, correct `conventional-commit-writer` skill —
frontmatter, body, and a bundled reference file — you can copy as a starting template.
