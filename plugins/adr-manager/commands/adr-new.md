---
name: adr-new
description: Create a new Architecture Decision Record from the MADR-style template with the next sequential number.
args: "<short decision title, e.g. 'Adopt PostgreSQL for the ledger'>"
---

Create a new Architecture Decision Record. Apply the `adr-authoring` skill for
the template and conventions.

Decision title: $ARGUMENTS

Steps:

1. Locate the ADR directory. Use `docs/adr/` if it exists; otherwise check
   `doc/adr/`, `docs/decisions/`, or `.harness/adrs/`. If none exists, create
   `docs/adr/` and tell the user where records will live.

2. Determine the next sequential number by scanning existing `NNNN-*.md` files
   (zero-padded to 4 digits, starting at `0001`).

3. Derive a kebab-case slug from the title and create
   `NNNN-<slug>.md` populated from the MADR template in the skill. Fill
   Status as `Proposed` and today's date. Draft the Context, Decision, and
   Consequences from the current conversation and repository context, marking
   unknowns with `TODO` rather than inventing facts.

4. Report the created file path and a one-line summary. Do not commit.
