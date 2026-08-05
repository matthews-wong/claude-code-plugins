# Review rubric

Use to keep the review focused on what matters and to resist the reviewer's built-in bias toward finding (and inventing) problems.

## Severity — what to flag

| Severity | Definition | Flag? |
|----------|------------|-------|
| Blocker | Incorrect behavior, data loss, security hole, or a stated requirement not met. | Always |
| Major | Unhandled error/edge case the requirements imply; changed behavior with no test. | Yes |
| Minor | Real but low-impact within scope (e.g., a confusing name in new public API). | Only if quick and clearly worthwhile |
| Noise | Style, preference, speculative feature, out-of-scope hardening. | Never |

## The over-engineering guardrail

A gap-seeking reviewer always finds "gaps." Before writing a finding, pass it through:

1. Does this break **correctness** or violate a **stated requirement**? If no → do not flag.
2. Is the input/condition it guards against actually **reachable** given the spec? If no → do not flag.
3. Am I proposing **new scope** (a feature, an abstraction, extra config)? If yes → do not flag.
4. Would I be **rewriting working code to my taste**? If yes → do not flag.

Only findings that survive all four are worth raising.

## Finding format

```
[Blocker|Major|Minor] <one-line summary>
  where:  <file:line>
  why:    <how it breaks correctness or a stated requirement>
  fix:    <smallest change that resolves it>
```

## Report shape

- Lead with the verdict: **PASS** (meets requirements) or **CHANGES NEEDED**.
- Then the findings, highest severity first.
- If PASS with no blockers/majors, say so in one line and stop — do not pad with minors and noise to look thorough.
