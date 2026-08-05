# spec-writer

Interview-first specification writing. Instead of guessing at a fuzzy feature, Claude interviews you and writes a spec precise enough to hand to a fresh session.

Packages the "**Let Claude interview you**" practice from Anthropic's *Claude Code best practices* guide: the user holds knowledge Claude can't infer, so eliciting it up front produces far better plans than one-shot guessing.

## What's inside

- `commands/spec.md` — `/spec` runs a structured interview (via the AskUserQuestion tool) about implementation, UI/UX, edge cases, and tradeoffs, then writes a self-contained `SPEC.md` that names files/interfaces, states what's out of scope, and ends with an end-to-end verification step.
- `skills/spec-writing/` — the interview technique and SPEC.md template, with a question bank and template under `reference/`.

## Usage

```
/spec a rate limiter for the public API
```

Answer the questions, review the generated `SPEC.md`, then — as the guide recommends — `/clear` and implement it in a **fresh session**. A clean context executing a good spec beats one carrying the whole interview.
