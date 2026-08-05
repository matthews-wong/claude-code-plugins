---
name: adr-list
description: List existing Architecture Decision Records with their number, title, status, and date.
args: "[optional status filter: proposed | accepted | rejected | deprecated | superseded]"
---

List the Architecture Decision Records in this repository. Apply the
`adr-authoring` skill for the status vocabulary.

Optional status filter: $ARGUMENTS

Steps:

1. Find the ADR directory (`docs/adr/`, `doc/adr/`, `docs/decisions/`, or
   `.harness/adrs/`). If none is found, say so and suggest `/adr-new`.

2. Read each `NNNN-*.md` record and extract its number, title, `Status`, and
   date.

3. If a status filter was given, include only matching records.

4. Present a table sorted by number: `# | Title | Status | Date`. Note any
   superseded records and what supersedes them. Do not modify any files.
