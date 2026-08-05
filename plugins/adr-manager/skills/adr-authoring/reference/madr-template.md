# MADR Template (Annotated) with Example

The Markdown Architecture Decision Record (MADR) format, trimmed to the fields
most teams use. Copy the template and delete guidance in angle brackets.

## Template

```markdown
# NNNN. <Short present-tense title of the decision>

- Status: <Proposed | Accepted | Rejected | Deprecated | Superseded by NNNN>
- Date: <YYYY-MM-DD when last updated>
- Deciders: <people or roles who made or must approve the call>

## Context

<Describe the problem and the forces: requirements, constraints, quality
attributes at stake, and assumptions. State why the status quo is insufficient.>

## Decision

<State the decision in active voice: "We will adopt X." Be specific about scope
and boundaries.>

## Consequences

<List outcomes honestly:
- Good: what improves.
- Bad: what we accept as a cost or new risk.
- Neutral: follow-on work this creates.>

## Considered Options

- <Option A> — <why chosen or rejected>
- <Option B> — <trade-off>
- <Option C> — <trade-off>
```

## Filled example

```markdown
# 0007. Adopt PostgreSQL for the ledger service

- Status: Accepted
- Date: 2026-08-05
- Deciders: Platform Guild

## Context

The ledger needs strong transactional guarantees and ad-hoc reporting. The
existing document store cannot express multi-row invariants without application
locks, which have caused two reconciliation incidents.

## Decision

We will use PostgreSQL 16 as the system of record for the ledger service,
using serializable transactions for balance-affecting writes.

## Consequences

- Good: ACID guarantees remove application-level locking; SQL enables reporting.
- Bad: introduces a new operational dependency the team must learn to run.
- Neutral: requires a migration plan from the current store.

## Considered Options

- PostgreSQL — chosen; mature, transactional, well understood.
- Keep the document store with app-level locks — rejected; incident-prone.
- CockroachDB — deferred; stronger scaling but higher operational cost now.
```
