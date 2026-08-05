---
name: pr-standards
description: Enterprise pull request review standards. Use when reviewing a pull request or merge request to check description quality, linked issue/ticket, change size, test coverage, and scope discipline, and to produce a checklist verdict.
---

# PR Standards

Evaluate a pull request against five enterprise criteria and return a checklist
verdict. Judge intent and risk, not style preferences.

## The five criteria

1. **Clear description** — Explains *why* the change exists, what it does, and
   how it was verified. A title-only or empty body fails.
2. **Linked issue / ticket** — References a tracking item (for example
   `#123`, `JIRA-456`, or a `Closes:`/`Refs:` footer). Trivial hotfixes may
   note the incident instead.
3. **Reasonable size** — Small enough to review well. Use the heuristics in
   `reference/size-heuristics.md`. Flag large diffs and suggest splitting.
4. **Tests included** — New behavior or bug fixes ship with tests, or the
   author gives an explicit, credible reason why not.
5. **No unrelated changes** — Every file in the diff serves the stated purpose.
   Drive-by refactors, formatting churn, or dependency bumps mixed into a
   feature PR fail scope discipline.

## Output format

Emit exactly this checklist, one line per criterion, then the verdict:

```
PR Governance Review
- [ ] Clear description — <pass/fail + one-line reason>
- [ ] Linked issue/ticket — <pass/fail + one-line reason>
- [ ] Reasonable size — <pass/fail + one-line reason>
- [ ] Tests included — <pass/fail + one-line reason>
- [ ] No unrelated changes — <pass/fail + one-line reason>

Verdict: <APPROVE | APPROVE WITH COMMENTS | REQUEST CHANGES>
Follow-ups:
- <concrete action, or "none">
```

Check the box (`[x]`) only when the criterion passes. Map the verdict from the
rules in `reference/verdict-rubric.md`.

## Reference

- `reference/size-heuristics.md` — size thresholds and splitting advice.
- `reference/verdict-rubric.md` — how criteria map to the final verdict.
