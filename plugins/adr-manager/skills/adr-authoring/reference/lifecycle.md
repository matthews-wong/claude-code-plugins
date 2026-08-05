# ADR Status Lifecycle

| Status | Meaning |
|--------|---------|
| `Proposed` | Drafted, under discussion, not yet binding. |
| `Accepted` | Agreed and in force. The record becomes immutable. |
| `Rejected` | Considered and declined. Kept for the historical trail. |
| `Deprecated` | No longer recommended but not replaced by a specific ADR. |
| `Superseded by NNNN` | Replaced by a newer decision; link the successor. |

## Rules

- Once `Accepted`, do not edit the Decision or Context. Corrections happen in a
  new superseding ADR.
- When superseding, update the old record's status to `Superseded by NNNN` and
  the new record's Context to reference the one it replaces.
- Keep rejected and deprecated records in place — the value of an ADR log is the
  history, including paths not taken.
