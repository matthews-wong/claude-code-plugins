---
name: review-fresh
description: Use after implementing a change to get a fresh-context adversarial review — "review my diff", "check this against the plan", "did I miss anything", before opening a PR. A reviewer that did NOT write the code checks the diff against the plan/requirements and flags only gaps affecting correctness or stated requirements.
---

Run an adversarial review of the current change with **fresh eyes**. The reviewer must evaluate the code as if it did not write it — judging the diff against the plan and requirements, not against its own memory of intent.

The best way to get true fresh context is to run this in a **separate Claude session** from the one that wrote the code, or to delegate the review to a subagent so it reasons in its own context. Prefer that. Then:

1. **Gather the ground truth.** Get the diff (`git diff`, `git diff --staged`, or the diff against the base branch) and the source of requirements — the SPEC.md, plan, issue, or task description. Review against what was *asked for*, not against what the reviewer would have preferred.

2. **Check the diff against the plan/requirements.** For each stated requirement: is it met? Look for correctness bugs, unhandled error/edge cases that the requirements imply, security issues, missing tests for changed behavior, and places where the implementation quietly diverges from the plan.

3. **Report only gaps that matter.** For each finding: what it is, where (file:line), why it affects correctness or a stated requirement, and the smallest fix.

$ARGUMENTS

## The important caveat

A reviewer told to find gaps will always find some. **Do not over-engineer.** Flag only gaps that affect **correctness or the stated requirements**. Explicitly do NOT raise:

- Speculative "what if" features beyond scope.
- Style/preference nits the requirements don't call for.
- Hardening for inputs or scale the spec doesn't require.
- Refactors that don't change behavior.

If the change correctly meets the requirements, say so plainly and stop. A clean bill of health is a valid — and common — outcome. See the **writer-reviewer** skill for the full rubric and the anti-over-engineering guardrails.
