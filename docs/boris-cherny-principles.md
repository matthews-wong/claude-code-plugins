# The Boris Cherny playbook (and how this marketplace maps to it)

> Research notes on how **Boris Cherny** — creator and head of Claude Code at Anthropic (ex-Meta Principal Engineer, author of *Programming TypeScript*) — actually uses Claude Code, and how the plugins here operationalize his practices. Sources are linked throughout; quotes are attributed to their reporting.

## Why he's worth studying

Cherny built the tool, and his team ships **20–30 PRs a day** by running several Claude instances in parallel. Nearly all of his advice follows from **one constraint** stated in the official guide: *"Claude's context window fills up fast, and performance degrades as it fills."* Everything below is a tactic for spending that budget well — which is exactly what this marketplace's plugins automate.

## The practices — and the plugins that embody them

### 1. Give Claude a way to verify its work (his #1 lever)
> *"Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."* — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

A feedback loop is reported to **2–3× the quality** of the result. Ways to gate the "stop": in-prompt checks, a `/goal` condition re-checked every turn, a **Stop hook** that blocks until a script passes, or a **verification subagent** that grades the work in a fresh context.

→ **Plugins:** `verify-before-review` (Stop hook), `test-guardian` / `test-coverage-gate` (PostToolUse), `e2e-verifier`, `code-review-agent`, `security-review-agent` (fresh-context reviewers).

### 2. Explore → Plan → Code → Commit
> *"Separate research and planning from implementation to avoid solving the wrong problem."*

Cherny starts in **plan mode**, iterates on the plan, then lets Claude one-shot the implementation. (Skip the plan when you could describe the diff in one sentence.)

→ **Plugins:** `plan-mode-helper`, `context-puller` (ground the exploration first).

### 3. Treat CLAUDE.md like code — and preserve mistakes
His team keeps a `CLAUDE.md` in git documenting mistakes, style, design, and PR conventions. The guide's test for every line: *"Would removing this cause Claude to make mistakes? If not, cut it."* Bloated memory files cause Claude to **ignore** real instructions. And when Claude repeats a mistake, he has it **write the lesson into CLAUDE.md or a skill** so the fix persists across sessions.

→ **Plugins:** `claude-md-manager` (scaffold + lint for bloat), `context-budget` (audit resident context), **`mistake-logger`** (capture a lesson into CLAUDE.md or a skill), and the whole [lean-context](./lean-structured-context.md) approach.

### 4. Anything you do more than once a day → a skill or command
His team has skills for everything from BigQuery analytics to code review to tech-debt analysis. Skills load only their one-line description until invoked, so they add capability without bloating context.

→ This is the entire premise of the marketplace — 40+ skills/commands packaging repeatable workflows.

### 5. Subagents as his everyday automation
Cherny runs subagents like **`code-simplifier`** (simplifies the code after Claude is done) and **`verify-app`** (detailed end-to-end testing). He thinks of subagents as automating the most common workflows — and, crucially, they run in a **separate context** so investigation/review doesn't pollute the main window.

→ **Plugins:** **`code-simplifier`** (his actual subagent), `repo-onboarder`, `access-review`, plus the review agents above.

### 6. Parallelism: many Claudes, isolated checkouts
He runs ~5 locally and 5–10 on the web, **numbering tabs**, each a **separate git checkout** so edits don't collide — plus Writer/Reviewer patterns where a fresh context reviews code it didn't write.

→ **Plugins:** `worktree-isolation`, `parallel-lanes`, `agent-kickoff`, `loop-runner`, `routine-scheduler`.

### 7. Adversarial review before "done"
> *"Have a subagent review the diff in a fresh context and report gaps."* — with the caveat to flag only correctness/requirement gaps and **avoid over-engineering**.

→ **Plugins:** `code-review-agent`, `security-review-agent`, `pr-governance`, `senior-standards`.

## His engineering principles (from the bottom of his CLAUDE.md)

Three rules he holds his team to (as reported):

1. **Make every change as simple as possible** — minimal code; *if you can delete lines instead of adding them, do that.*
2. **Find root causes** — no temporary fixes or band-aids; hold to senior-developer standards.
3. **Only touch what's necessary** — no side effects; don't introduce new bugs while fixing old ones.

→ Encoded directly in the **`senior-standards`** plugin (and applied by `code-simplifier` and the review agents).

## His adoption principles (for teams)

From his appearance on *Lenny's Podcast* (reported by Business Insider): *"What's better than doing something? Having Claude do it,"* **"underfunding things a little bit"** to force reliance on the tools, and encouraging people to **go faster** by having Claude do more. On cost: *"Start by just giving engineers as many tokens as possible,"* and optimize cost **after** you've built something successful — the same "control cost after PMF" idea in his [five stages of AI adoption](https://www.explainx.ai/blog/boris-cherny-steps-ai-adoption-claude-code-july-2026).

→ **Plugins:** `cost-controller`, `token-budget-tracker`, `otel-governance`, `auto-mode-setup`, `permission-optimizer`.

## Common failure patterns he warns about

Kitchen-sink sessions, correcting-over-and-over, the over-specified CLAUDE.md, the trust-then-verify gap, and infinite exploration — each with a fix (`/clear`, prune CLAUDE.md, always verify, scope with subagents). This marketplace turns those fixes into installable guardrails.

## Sources

- [Claude Code: best practices for agentic coding](https://code.claude.com/docs/en/best-practices) (Anthropic / Cherny's team) — the primary, authoritative guide
- [Head of Claude Code: what happens after coding is solved](https://www.lennysnewsletter.com/p/head-of-claude-code) (Lenny's Newsletter)
- [Building Claude Code with Boris Cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny) (The Pragmatic Engineer)
- [The Neuron: Claude Code's creators explain agent loops](https://www.theneuron.ai/explainer-articles/claude-code-creators-boris-cherny-and-cat-wu-explain-how-to-use-agent-loops/)
- [10 Claude Code tips from creator Boris Cherny](https://www.jitendrazaa.com/blog/others/tips/10-claude-code-tips-from-the-creator-boris-cherny-february/)
- [Boris Cherny's five stages of AI adoption](https://www.explainx.ai/blog/boris-cherny-steps-ai-adoption-claude-code-july-2026) (explainX)

> Quotes are attributed to the reporting that published them; where a principle is paraphrased from secondhand coverage, it's presented as such.

---

_Part of [claude-code-plugins](https://github.com/matthews-wong/claude-code-plugins) by Matthews Wong._
