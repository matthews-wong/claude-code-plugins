---
description: Use when authoring, structuring, or connecting Claude Code skills — writing a SKILL.md, crafting the frontmatter description that drives routing, deciding when to split one skill into several, referencing other skills, and organizing a coherent agentic skills library. The reference for building skills that reliably trigger and compose.
---

# Skills Connector

Skills are model-invoked capabilities: a folder with a `SKILL.md` whose YAML frontmatter
`description` is what Claude reads to decide, on its own, whether to load the skill for the
current task. Get the description right and the skill fires when it should; get the body
right and it actually helps once loaded.

## Anatomy of a skill

```
skills/
  <skill-name>/
    SKILL.md            # required: frontmatter + instructions
    references/         # optional: deeper docs loaded on demand
    scripts/            # optional: helper scripts the skill can run
```

`SKILL.md` frontmatter:

```yaml
---
description: <what it does + WHEN to use it — this drives routing>
---
```

- `description` is **required** and is the single most important field — it is the routing
  signal. Everything below the frontmatter is the instruction body loaded only after the
  skill triggers.
- Keep the folder name kebab-case and matching the skill's identity.
- Optional supporting files (`references/`, `scripts/`) keep the main body lean; point to
  them from the body so they load only when needed (progressive disclosure).

## Writing a description that routes correctly

The description is a trigger, not a title. It must answer **what** the skill does and,
critically, **when** to use it — in the user's vocabulary.

- Lead with the trigger conditions: "Use when the user wants to …".
- Include concrete cues: the tasks, file types, verbs, and phrasings that should fire it.
- Be specific enough not to over-trigger, broad enough to catch real phrasings.
- Write in third person about the situation, not first person about yourself.

Weak: `description: Helps with database stuff.`

Strong: `description: Use when writing, reviewing, or optimizing SQL queries or schema
migrations for Postgres — covers indexing, query plans, and safe migration ordering.`

## Writing the body

- Start with the core procedure or checklist; put the highest-value guidance first.
- Prefer imperative, skimmable instructions over prose. Use headings, short lists, and
  small examples.
- State hard rules explicitly (safety constraints, must/never).
- Keep it focused — a skill is one coherent capability, not a manual.
- Offload depth to `references/` and heavy logic to `scripts/`; mention them by path.

## When to split a skill

Split when one skill starts serving two different trigger situations or grows past a
single coherent capability. Signs you should split:

- The description needs "and" to cover unrelated situations.
- Parts of the body are only relevant to some invocations.
- Two distinct user intents would each want only half the file.

Prefer several tightly-scoped skills over one sprawling one — narrow descriptions route
more reliably and load less irrelevant context.

## Connecting skills to each other

Skills compose into a library. To connect them:

- **Reference by name and path.** From one skill's body, point to a sibling: "For the
  migration ordering rules, use the `sql-migrations` skill." Claude can then load it.
- **Keep responsibilities non-overlapping.** Overlapping descriptions cause ambiguous
  routing; give each skill a clear lane and let them hand off.
- **Establish a hub for shared conventions.** A single "standards" skill others reference
  avoids duplicating rules across many files (DRY).
- **Layer scope deliberately.** Personal skills live in `~/.claude/skills/`, project
  skills in `.claude/skills/`, and plugin skills ship inside a plugin. Project scope wins
  for team-shared, repo-specific capability; user scope for personal cross-project ones.

## Quality checklist before shipping a skill

- [ ] Folder is kebab-case; `SKILL.md` present with valid YAML frontmatter.
- [ ] `description` states what AND when, in the user's words, with concrete cues.
- [ ] One coherent capability — no unrelated "and".
- [ ] Body is skimmable, imperative, and leads with the highest-value guidance.
- [ ] Hard rules stated explicitly; depth offloaded to `references/`.
- [ ] References to sibling skills use their name/path; no overlapping lanes.
