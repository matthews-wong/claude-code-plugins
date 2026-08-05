# Pre-ship authoring checklist

Run this before you consider a skill done. Each item maps to a common reason skills either
fail to fire or fail to help once loaded.

## Scope and identity

- [ ] **Single purpose.** The skill is one coherent capability. If describing it needs an
      unrelated "and", split it into two skills.
- [ ] **Folder is kebab-case** and names the capability; `name` (if set) matches.

## Routing

- [ ] **The description is a trigger, not a title.** It leads with `Use when …` and states
      what AND when. (See `descriptions.md`.)
- [ ] **Concrete keywords present** — the verbs, file types, tools, and error phrasings a
      user would actually type appear in the description.
- [ ] **No overlap** with a sibling skill's trigger, which would cause ambiguous routing.

## Body and progressive disclosure

- [ ] **SKILL.md is lean** — it leads with the highest-value procedure and stays skimmable
      (imperative headings, short lists), not a wall of prose.
- [ ] **Heavy detail lives in `reference/`** (and heavy logic in `scripts/`), pointed to
      from the body by relative path so it loads only on demand.
- [ ] **Hard rules are explicit** — must/never and safety constraints are stated, not
      implied.

## Validation and fire test

- [ ] **Valid frontmatter** — YAML between `---` fences, `description` present.
- [ ] **`/plugin validate`** passes (for skills shipped in a plugin) — confirms the
      manifest, frontmatter, and structure are well-formed.
- [ ] **Fire test after `/reload-plugins`** — reload, then phrase a request the way a real
      user would and confirm the skill actually triggers. If it doesn't fire, the
      description is almost always the cause (see `descriptions.md`), not the body.
- [ ] **Helpful once loaded** — walk the body as if following it cold; it should be
      sufficient to do the task without the missing context living only in your head.

## Connection (for a library of skills)

- [ ] **Sibling references use name/path**, so hand-offs actually resolve.
- [ ] **Shared conventions are centralized** in a hub skill rather than duplicated.
