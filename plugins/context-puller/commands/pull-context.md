---
name: pull-context
description: Use before starting a non-trivial task — pulls repo context (README, docs, ADRs, related modules, git history) into a short working brief so you act on facts, not guesses. Triggers on 'get me up to speed', 'brief before I start', 'pull context'.
args: "[task description or area of the codebase to focus on]"
---

You are preparing to work on the following task: **$ARGUMENTS**

Before writing any code, build a working brief so you start grounded in this
repository rather than guessing. Follow the `context-pull` skill for the full
method. In short:

1. **Locate the primary docs.** Read the root `README.md`, then scan `docs/`,
   `CLAUDE.md`, and any `.harness/readiness.md` or `ADR`/`adr` directories.
2. **Find the code that matters for this task.** Use glob and grep to identify
   the modules, entry points, and tests most related to `$ARGUMENTS`. Read the
   few files that are clearly central; skim the rest.
3. **Pull recent history.** Run `git log --oneline -20` and, when a specific
   area is named, `git log --oneline -10 -- <path>` to see how it has changed
   recently and who touched it.
4. **Note conventions and constraints.** Naming, layering, testing approach,
   and any gotchas called out in docs or comments.

Then produce a concise **Working Brief** with these sections:

- **Goal** — one or two sentences restating the task in repo terms.
- **Relevant files** — bullet list of paths with a one-line role for each.
- **How it fits together** — a short paragraph on the data/control flow.
- **Conventions to honor** — style, testing, and architectural rules observed.
- **Recent activity** — notable commits touching this area.
- **Open questions / risks** — anything ambiguous or likely to bite.

Keep it under roughly one page. Do not start implementing yet — the brief is the
deliverable. If the user agrees the brief is accurate, offer to seed the durable
parts (conventions, architecture notes) into `CLAUDE.md` so future sessions
inherit the grounding.
