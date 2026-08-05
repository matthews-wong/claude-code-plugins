---
name: spec-writing
description: Use when turning a fuzzy feature request into an implementable spec by interviewing the user first — planning a feature, writing a SPEC.md or design doc, or eliciting requirements before coding. Covers the interview technique (structured questions on implementation, UI/UX, edge cases, tradeoffs) and a self-contained SPEC.md template that ends in a verification step.
---

# Spec writing by interview

Good specs come from getting knowledge out of the user's head, not from guessing. The user knows the constraints, the history, and which tradeoffs they care about. Your job is to interview them into a spec so complete that a fresh session with no memory of the conversation could implement it correctly.

## The two phases

**1. Interview.** Ask, don't assume. Use the AskUserQuestion tool for focused questions with concrete options plus room to write freely. Ask in small batches and let each answer steer the next question — dig into the hard parts rather than marching through a checklist.

Cover four areas as they apply:
- **Technical implementation** — files/modules touched, interfaces, data shapes, dependencies, integration with existing code.
- **UI/UX** — user flow, states (loading/empty/error), the unhappy path.
- **Edge cases** — empty input, concurrency, failure/retry, limits, auth boundaries, data migration.
- **Tradeoffs** — decisions with more than one defensible answer. This is where interview time pays off: surface the options, name the tension, get the user's call.

Stop when the remaining unknowns are small enough that a competent engineer wouldn't have to guess.

**2. Write SPEC.md.** Self-contained. Names concrete files and interfaces. States what's out of scope. Ends with a real end-to-end verification step. See `reference/spec-template.md` for the full template and `reference/interview-questions.md` for a question bank by area.

## Key principles

- **Don't guess the hard parts — ask.** A wrong assumption at spec time costs far more than a question.
- **Out of scope is a first-class section.** Naming what you're *not* building prevents scope creep and over-engineering.
- **Preserve the "why".** Record the reasoning behind settled tradeoffs so it survives into implementation.
- **Every spec ends in verification.** A concrete command + flow + observable success result, so "done" is provable.
- **Then execute in a fresh session.** Once SPEC.md is written and reviewed, `/clear` and implement from the spec. A clean context executing a good spec outperforms one dragging the whole interview along.

## Detailed references

- `reference/spec-template.md` — the SPEC.md section-by-section template.
- `reference/interview-questions.md` — a bank of probing questions per area.
