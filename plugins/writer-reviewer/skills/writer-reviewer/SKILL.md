---
name: writer-reviewer
description: Use when reviewing a just-implemented change with fresh eyes — checking a diff against a plan/spec/requirements before a PR, running an adversarial or second-pass review, or when one session writes code and another reviews it. Emphasizes flagging only correctness/requirement gaps and avoiding over-engineering, since a gap-seeking reviewer always finds something.
---

# Writer / reviewer split

Code is reviewed better by a context that did not write it. The author's context is anchored on what it *meant* to do; a fresh reviewer sees what the code *actually* does. This skill is the reviewer half of a two-session workflow: one session (or subagent) implements, a separate fresh context reviews the diff against the plan.

## Why fresh context

- The author remembers intent and unconsciously fills gaps the code doesn't actually cover.
- A reviewer with no memory judges the diff on its merits against the written requirements.
- Practically: run the review in a **different Claude session** or delegate to a **subagent** so it reasons in its own context. Don't just ask the same session "now review yourself."

## The review procedure

1. **Anchor on ground truth.** Read the requirements source — SPEC.md, plan, issue, or task description — and get the diff (`git diff` / against the base branch). Review against what was asked, not personal preference.
2. **Walk the diff against each requirement.** Is each one met? Then look for correctness bugs, unhandled edges the requirements imply, security issues, and missing tests for changed behavior.
3. **Report findings that matter**, each with: what, where (file:line), why it breaks correctness or a stated requirement, and the smallest fix.

## The caveat that makes this useful

**A reviewer instructed to find gaps will always find some.** Left unchecked it invents work — speculative features, defensive code for inputs that can't occur, style opinions. That noise buries the real findings and pushes toward over-engineering.

So constrain the reviewer: **flag only gaps that affect correctness or the stated requirements.** If the change meets the requirements, say so and stop — a clean pass is a valid and common result.

See `reference/review-rubric.md` for the severity rubric and the explicit "do not flag" list.

## Do not flag (out of scope by default)
- Features or robustness the spec doesn't ask for.
- Style/naming/formatting the requirements don't specify.
- Hardening for inputs, scale, or failure modes outside stated scope.
- Behavior-preserving refactors and "while you're in here" cleanups.
