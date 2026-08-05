# writer-reviewer

A fresh-context, adversarial review step. After you implement, a reviewer that did **not** write the code checks the diff against the plan.

Packages two practices from Anthropic's *Claude Code best practices* guide: "**Run multiple Claude sessions**" and "**Add an adversarial review step**." Fresh context reviews code it didn't write, so it evaluates what the code actually does rather than what it was meant to do.

## What's inside

- `commands/review-fresh.md` — `/review-fresh` gathers the diff and the requirements (SPEC/plan/issue) and reviews the change against them, ideally in a separate session or subagent for true fresh context.
- `skills/writer-reviewer/` — the writer/reviewer workflow, with a severity rubric and an over-engineering guardrail under `reference/`.

## The key caveat

A reviewer told to find gaps will always find some. This plugin instructs the reviewer to flag **only** gaps that affect correctness or stated requirements — and to avoid over-engineering. A clean pass is a valid, common outcome.

## Usage

```
/review-fresh check the diff against SPEC.md before I open the PR
```
