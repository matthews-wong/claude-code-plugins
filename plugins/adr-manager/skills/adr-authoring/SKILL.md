---
name: adr-authoring
description: MADR-style Architecture Decision Record conventions. Use when creating, updating, or listing ADRs to apply the standard template, numbering, and status lifecycle.
---

# ADR Authoring

An Architecture Decision Record captures one significant, hard-to-reverse
decision: its context, the choice made, and the consequences.

## Conventions

- **File name**: `NNNN-kebab-title.md`, zero-padded to 4 digits, sequential
  from `0001`. Numbers are never reused.
- **Location**: `docs/adr/` by default.
- **One decision per record.** Records are immutable once accepted; to change a
  decision, write a new ADR that supersedes the old one.

## Status lifecycle

`Proposed` -> `Accepted` -> `Deprecated` or `Superseded by NNNN`.
A proposal may also be `Rejected`. See `reference/lifecycle.md` for the rules.

## Template (MADR-style)

```markdown
# NNNN. <Title>

- Status: Proposed
- Date: YYYY-MM-DD
- Deciders: <names or roles>

## Context

<The forces at play: problem, constraints, drivers. Why a decision is needed.>

## Decision

<The choice made, stated in active voice: "We will ...">

## Consequences

<Positive, negative, and neutral outcomes. What becomes easier or harder.>

## Considered Options

- <Option A> — <trade-off>
- <Option B> — <trade-off>
```

The full annotated template with an example lives in
`reference/madr-template.md`.

## Principles

- Record the *why*, not a tutorial. Keep it to what a future maintainer needs.
- Do not fabricate deciders, dates, or rationale; mark unknowns as `TODO`.
