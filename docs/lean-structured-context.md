# How plugins create lean, structured context

> The single biggest lever on agent quality isn't the model — it's **what you put in its context window**. Plugins are how you keep that context lean and structured. This is the research behind this marketplace.

## The core tension: your context budget

Claude Code starts each session with a large context window, but a chunk is spent before you type anything: system prompt, environment, every loaded `CLAUDE.md`, and the memory index. **Everything resident costs tokens, and every wasted token is one not spent on your actual task** — and a noisier context also *routes worse*, because the model has more to sift through.

The discipline is **progressive disclosure**: load only what's needed *now*, defer the rest to load on demand.

## Where the tokens go — and how plugins fix it

| Strategy | Resident at startup | When detail loads | Context lost to overhead |
| --- | --- | --- | --- |
| Dump a 2,000-line `CLAUDE.md` | ~8k tokens | always (sits all session) | ~4% of budget, every turn |
| **Lean `CLAUDE.md` + skills** | ~1k tokens | skill body loads only when invoked | **<1% until a skill fires** |
| **Path-scoped rules** | only rules whose paths match | when Claude touches matching files | **0% for unrelated work** |
| **Subagent for a side task** | main unaffected; subagent isolated | in the subagent's own window | **0% in the main context** |
| **Deferred MCP schemas** | tool *names* only (~120 tokens) | schema fetched when the tool is used | **~0% until needed** |

That's the whole game: move cost from *always-resident* to *load-on-demand*.

## The five moves (and which plugins here embody them)

### 1. Skills instead of a bloated `CLAUDE.md`
A skill's `SKILL.md` is **not** loaded at startup — only its one-line description sits in the inventory (a few dozen tokens). The body loads when the description matches the task; bundled `reference/*.md` load only when referenced. So a 500-line checklist costs ~2 tokens until the moment it's actually needed.

→ Every skill in this marketplace uses this. `context-budget` audits your setup for exactly this move: it flags procedures that have crept into `CLAUDE.md` and should become skills.

### 2. Keep `CLAUDE.md` to facts, not procedures
Aim for a lean memory file (well under ~200 lines). Keep the things Claude needs *every* session — build/test commands, non-obvious conventions, **gotchas**, safety rules — and cut everything derivable from the repo (directory listings, dependency lists, standard commands). If a section has grown into a *procedure*, it belongs in a skill.

→ `claude-md-manager` scaffolds a lean file and lints an existing one for derivable bloat.

### 3. Path-scoped rules for local guidance
Instead of one giant memory file, put directory-specific guidance in `.claude/rules/*.md` with a `paths:` frontmatter. The rule loads **only when Claude works with matching files** — zero cost the rest of the time.

```markdown
---
paths: ["src/api/**/*.ts"]
---
All API endpoints must validate input with the shared schema…
```

### 4. Subagents to compartmentalize noise
A side task that would flood the main conversation with logs, search results, or file dumps belongs in a subagent. It runs in its **own** context window and returns only a summary — the intermediate noise never touches your main context.

→ `code-review-agent`, `security-review-agent`, `access-review`, and `repo-onboarder` are read-only subagents for exactly this reason.

### 5. Commands to package repeatable prompts
A slash command turns a long, re-typed instruction into `/name`. Each invocation is a fresh, structured prompt — it doesn't accumulate in the conversation the way pasted instructions do.

→ Most plugins here ship a command as the explicit entry point.

## The flagship: `context-budget`

`/context-audit` puts this research to work on *your* repo: it measures what's resident, flags `CLAUDE.md` content Claude could derive on its own, recommends what to keep (gotchas, safety rules, non-obvious conventions) versus cut, and restructures the rest into skills and path-scoped rules via progressive disclosure. The plugin practices what it preaches — its own `SKILL.md` is lean and defers heuristics to `reference/` files.

## Why it matters (the payoff)

- **More budget for real work** — a lean setup leaves almost the whole window for your task.
- **Better routing** — the model isn't distracted by irrelevant always-on instructions.
- **Lower cost** — fewer resident tokens per turn across a long session.
- **Scales to hundreds of skills** — because each costs ~nothing until it fires.

## Sources

- [Claude Code memory & CLAUDE.md](https://code.claude.com/docs/en/memory.md)
- [Context window management](https://code.claude.com/docs/en/context-window.md)
- [Skills](https://code.claude.com/docs/en/skills.md) · [Subagents](https://code.claude.com/docs/en/sub-agents.md)
- [Progressive disclosure, step by step](https://medium.com/@dan.avila7/claude-code-skills-progressive-disclosure-step-by-step-3ca02a4a9f60)
- [The new rules of context engineering (Anthropic)](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)

---

_Part of [claude-code-plugins](https://github.com/matthews-wong/claude-code-plugins) by Matthews Wong._
