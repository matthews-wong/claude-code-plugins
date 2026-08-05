---
description: Use before any non-trivial code change — a refactor, new feature, migration, or multi-file edit. Investigate the affected code first, produce a concise implementation plan (files to change, approach, risks, test strategy), get the user's confirmation, then execute. Prevents premature edits and surprise blast radius on risky work.
---

# Plan First

For anything beyond a trivial one-liner, plan before you edit. A short plan up front
catches wrong assumptions, exposes blast radius, and gives the user a cheap point to
course-correct before code is written.

## When to plan first

- Multi-file changes, refactors, new features, or migrations.
- Anything touching shared/core code, public APIs, or config.
- Work where the approach is non-obvious or has real trade-offs.
- Anything irreversible or wide-reaching.

Skip the ceremony for genuinely trivial edits (a typo, a rename in one spot) — planning
there is just friction. Use judgment.

## The workflow

1. **Investigate first.** Read the affected files, understand current behavior, existing
   conventions, callers, and tests. Never plan against a codebase you haven't looked at.
2. **Write a concise plan.** Skimmable, not a wall of text. Sections:
   - **Goal** — one sentence: what and why.
   - **Files to change** — each path + one line on the change.
   - **Approach** — ordered steps; note key decisions and rejected alternatives.
   - **Risks** — breakage, edge cases, irreversible/wide-reaching effects.
   - **Test strategy** — tests to add/run and manual checks; a bug fix gets a test that
     fails before and passes after.
3. **Confirm.** Ask the user to approve or adjust. Do not edit until they approve. Revise
   and re-confirm if they push back.
4. **Execute as agreed.** Implement the approved plan. If a risk materializes or an
   assumption proves wrong mid-way, pause and surface it instead of silently improvising.
5. **Verify.** Run the test strategy and report results honestly, including anything still
   failing or skipped.

## Principles

- Prefer the smallest change that satisfies the requirement (KISS, YAGNI).
- Match the conventions already in the code over your own preferences.
- Make the plan a decision aid for the user, not a formality — surface the real choices.
- This pairs naturally with Claude Code's plan mode (`permissions.defaultMode: "plan"`),
  which enforces read/plan-only until you approve.
