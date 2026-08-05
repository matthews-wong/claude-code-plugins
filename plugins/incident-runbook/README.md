# incident-runbook

A calm, structured guide for production incidents — from the first alert to the
blameless postmortem.

## Components

- **`/incident [phase]`** — drives the response through `triage`, `comms`,
  `mitigate`, and `postmortem` (defaults to triage).
- **Skill: incident-response** — severity matrix, roles, response flow, and a
  mitigation decision tree. Templates in
  `skills/incident-response/reference/`:
  - `comms-templates.md` — internal/external/resolved status updates.
  - `postmortem-template.md` — blameless postmortem scaffold.

## Principles

Restore service first, learn second, blame never. Stop the bleeding before
diagnosing; communicate on a cadence matched to severity; write postmortems that
fix systems, not people. The plugin never invents metrics, causes, or ETAs — it
marks unknowns as unknown and defers to your org's real escalation, security, and
legal policies.

Author: Matthews Wong · License: MIT
