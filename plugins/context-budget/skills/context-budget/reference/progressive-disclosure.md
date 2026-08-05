# Progressive Disclosure (reference)

How skill loading and routing actually work, and how to layer context. Load on demand.

## The loading model

There are three tiers of context, each loaded at a different time:

1. **Always loaded (every turn):** system prompt, tool schemas, and memory files (`CLAUDE.md` at repo root and applicable subdirs, plus the user-global `~/.claude/CLAUDE.md`). This is the expensive tier — spent on every single turn.
2. **Metadata only (until triggered):** for each available skill, only its `name` + `description` are in context — on the order of a few dozen tokens each. This is what routing matches against.
3. **Loaded on demand (when triggered):** when a skill's description matches the task, its `SKILL.md` body loads. Files it references (`reference/*.md`) load only when the skill explicitly reads them.

Progressive disclosure = keep tier 1 tiny, let tiers 2 and 3 carry the depth and pay for themselves only when relevant.

## Why bloat hurts twice

A fat `CLAUDE.md` costs you both ways:
- **Budget:** every token is re-loaded each turn, crowding out the actual task and reducing effective working room.
- **Routing quality:** more always-on text is more noise the model sifts through, which can blur attention and weaken skill/tool selection.

Slimming the always-loaded tier is one of the highest-leverage context-engineering moves.

## Writing a description that routes well

The `description` is the *only* thing the model sees when deciding whether to pull in a skill. Make it earn its place:

- State the **trigger** ("Use when …") and the **task shape** it covers.
- Include concrete **keywords and phrasings** a user would actually type.
- Be specific enough to fire on the right tasks and quiet on the wrong ones. Vague descriptions either never trigger or trigger too often.
- Keep the `SKILL.md` body focused and under ~2000 tokens; move depth to `reference/` files.

Weak: "Helps with data stuff."
Strong: "Classify data fields into public/internal/confidential/PII and recommend handling. Use when reviewing schemas, payloads, or logs for sensitive data. Triggers on 'classify data', 'is this PII', 'sensitive fields'."

## The layering pattern

```
CLAUDE.md (tier 1, always on)
  └─ lean: gotchas, safety rules, non-obvious conventions, skill pointers
Skill SKILL.md (tier 3, on trigger)
  └─ focused workflow + decision heuristic, < ~2000 tokens
Skill reference/*.md (tier 3, on explicit read)
  └─ deep detail, tables, matrices, worked examples
```

Move content down a tier whenever it isn't needed on every turn. Reference this from a lean CLAUDE.md instead of inlining it.

## Applying it to a repo

1. Strip CLAUDE.md to tier-1-worthy content + skill pointers.
2. Turn each "when doing X, do Y" block into a skill with a sharp description.
3. Break any SKILL.md over ~2000 tokens by extracting its heavy sections into `reference/` files it links to.
4. De-duplicate: if two memory files repeat content, keep one source and point to it.
