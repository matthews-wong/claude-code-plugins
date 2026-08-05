# How to write a good Claude Code plugin

A field guide distilled from Anthropic's skill-authoring guidance and community practice (2026). The short version: **pick the right component, make it single-purpose, and write a description that fires at exactly the right moment.**

## 1. Choose the right component

A plugin can bundle four kinds of things. Reach for the one that matches the job:

| Component | Use it when… | Loads |
| --- | --- | --- |
| **Skill** (`skills/<name>/SKILL.md`) | You want Claude to *know how to do something* and pull that knowledge in **only when relevant** | Name + description always; body on trigger; bundled files on reference |
| **Slash command** (`commands/*.md`) | You want a **repeatable prompt** the user invokes explicitly (`/review`, `/release`) | On invocation |
| **Subagent** (`agents/*.md`) | You want work done in an **isolated context** with its own tools/model (review, exploration) | Spawned on demand |
| **Hook** (`hooks/hooks.json`) | You want something to run **automatically on an event** (before/after a tool, on stop) | On the event |

Rule of thumb: *knowledge* → skill, *action the user triggers* → command, *isolated sub-task* → subagent, *automation* → hook.

## 2. Keep skills lean and single-purpose

- **One capability per skill.** "Generate a Next.js API route with Zod validation and a test" is a good skill; "handle backend stuff" is not.
- **Stay under ~2,000 tokens** in `SKILL.md`. Longer skills eat context without proportional benefit.
- **Be specific and opinionated.** Encode *your* patterns and defaults, not generic advice the model already knows.

## 3. The description is the trigger — write it carefully

At startup Claude loads **only the name and description** of each skill (a few dozen tokens). That description is what decides whether the skill fires.

- Name the **exact situation**: *"Use when converting CSV to JSON"* beats *"handles data."*
- Include **concrete keywords and conditions** that should invoke it.
- A vague description is the **number-one reason a skill fails to fire.**

## 4. Apply progressive disclosure

Don't inline everything. Structure a skill in layers so heavy detail loads only when needed:

```
skills/my-skill/
  SKILL.md            # lean: what it does + when + the core steps
  reference/
    deep-dive.md      # loaded only when SKILL.md references it
    examples.md
```

`SKILL.md` should point to `reference/*.md` for depth. This keeps the always-resident footprint tiny while still giving Claude the full detail on demand.

## 5. Test that it actually fires

1. `/plugin validate .` — checks manifest/marketplace syntax, duplicate names, and path traversal.
2. `/reload-plugins`, then give Claude a task that *should* match the description.
3. Confirm it loads the skill rather than improvising. **If it doesn't fire, sharpen the description** — that's almost always the fix.

## 6. Security: hooks and commands run code

- Hooks execute on your machine. Keep hook scripts **least-privilege and non-blocking** (exit 0 so a hook never wedges a session).
- Never bake secrets into a plugin. Reference env vars.
- Prefer **read-only** subagents (`tools: Read, Grep, Glob`) for review/analysis work.

## 7. Package and version

- A **skill** is for a single capability you're iterating on; wrap it in a **plugin** to distribute it. A plugin can bundle several skills plus commands, agents, hooks, and MCP servers, and installs with one command.
- Set an explicit `version` and bump it on releases, or omit it and let the git SHA drive updates.
- List every plugin in `.claude-plugin/marketplace.json` (use `metadata.pluginRoot` to avoid repeating paths).

## Common mistakes

- ❌ Vague descriptions → the skill never triggers.
- ❌ Kitchen-sink skills → high token cost, poor routing.
- ❌ Inlining reference docs into `SKILL.md` → wasted context budget.
- ❌ Blocking hooks → a failing hook stalls the session.
- ❌ Duplicating what the model already knows → no value over the base model.

## Sources

- [Best Claude Code Plugins & Skills (2026)](https://dev.to/raxxostudios/best-claude-code-skills-plugins-2026-guide-4ak4)
- [Claude Code Skills Best Practices: A Practical Guide (2026)](https://designrevision.com/blog/claude-code-skills-best-practices)
- [Claude Code Skills: Progressive Disclosure Step by Step](https://medium.com/@dan.avila7/claude-code-skills-progressive-disclosure-step-by-step-3ca02a4a9f60)
- [Claude Code plugin & marketplace docs](https://code.claude.com/docs/en/plugin-marketplaces.md)

---

_Part of [claude-code-plugins](https://github.com/matthews-wong/claude-code-plugins) by Matthews Wong._
