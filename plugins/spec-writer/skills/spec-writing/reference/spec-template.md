# SPEC.md template

Write the spec so a fresh session with no memory of the interview could implement it correctly. Fill every section; delete a section only if it genuinely does not apply.

```markdown
# SPEC: <feature name>

## Goal
<What we're building and why, in 2–4 sentences. The problem it solves.>

## Scope
<Bulleted list of what IS included in this piece of work.>

## Out of scope
<Bulleted list of what we are explicitly NOT doing. Prevents scope creep and
over-engineering. Include things that were considered and deliberately deferred.>

## Design
<The concrete plan. Be specific enough to implement without new decisions.>

- Files to create: <path — responsibility>
- Files to change: <path — what changes>
- Interfaces / signatures:
    <function, type, endpoint, or CLI signatures — the actual shapes>
- Data model: <schemas, tables, message formats>
- Key decisions (with reasoning):
    - <decision> — chosen because <why>; alternative <X> rejected because <Y>.

## Edge cases & error handling
<Each edge case surfaced during the interview, and how it is handled.>
- <case> → <behavior>

## End-to-end verification
<A concrete final step that proves the whole feature works.>
- Command(s) to run: <exact command>
- Flow to exercise: <the happy path, step by step>
- Observable success: <what output/state means it worked>
```

## Quality bar

- Someone could implement this without asking you a question.
- Every named file has a clear responsibility.
- Every settled tradeoff records *why*, not just *what*.
- The verification step is runnable and its success is observable — not "make sure it works."
