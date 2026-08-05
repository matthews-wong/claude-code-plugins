---
name: spec
description: Use when a feature or task is fuzzy and worth pinning down before coding — "write a spec", "let's plan this feature", "interview me", "turn this idea into a spec". Interviews you with structured questions about implementation, UI/UX, edge cases, and tradeoffs, then writes a self-contained SPEC.md ending in a verification step.
---

Before writing any code, interview me to turn a rough idea into a precise, self-contained specification. I know things about this feature that you don't — get them out of my head. Don't guess at the hard parts; ask.

Topic for this spec: $ARGUMENTS

## How to run the interview

Use the **AskUserQuestion** tool to ask focused, multiple-choice-style questions with concrete options (always leave room for a free-form answer). Ask in small batches, then dig deeper based on my answers — follow the interesting thread rather than reading a fixed list. Cover, as they apply:

- **Technical implementation** — where this lives, which files/modules/interfaces it touches, data shapes, dependencies, how it integrates with what already exists.
- **UI/UX** — the user's flow, states (loading/empty/error), what happens on the unhappy path.
- **Edge cases** — empty inputs, concurrency, failure and retry, limits, auth/permission boundaries, migration of existing data.
- **Tradeoffs** — the real decisions with more than one defensible answer. Surface the options, name the tension, and get my call. This is the point of the interview; spend your questions here.

Push on the parts that are genuinely hard or ambiguous. If an answer opens a new question, ask it. Stop when the remaining unknowns are small enough that a competent engineer wouldn't have to guess.

## Then write SPEC.md

Write a `SPEC.md` that is **self-contained** — a fresh session with no memory of this conversation could implement it correctly. Include:

1. **Goal** — what we're building and why, in a few sentences.
2. **Scope** — what's in.
3. **Out of scope** — what we are explicitly NOT doing (this prevents scope creep and over-engineering).
4. **Design** — the concrete plan: named files to create/change, function/type/endpoint signatures, data models, and the key decisions we settled (with the reasoning, so the "why" survives).
5. **Edge cases & error handling** — the list we surfaced, and how each is handled.
6. **End-to-end verification** — a concrete final step that proves the whole thing works: the command to run, the flow to exercise, and the observable result that means success.

Consult the **spec-writing** skill for the interview technique and the SPEC.md template.

When SPEC.md is written, tell me to review it and then implement it in a **fresh session** (`/clear` first) — a clean context executing a good spec beats one carrying all the interview back-and-forth.
