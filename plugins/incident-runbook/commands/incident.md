---
name: incident
description: Drive an incident: triage severity, draft comms, guide mitigation, and scaffold a postmortem.
args: "[phase] (optional: triage | comms | mitigate | postmortem; defaults to triage)"
---

Act as the incident response guide. Load the skill `incident-response` for the
severity matrix, comms cadence, and templates. Work through the phase requested
(or start at triage).

## triage (default)

1. Establish facts fast: what is the observed impact, since when, what changed
   recently (deploys, config, dependencies, traffic)?
2. Assign a severity using the SEV matrix from the skill. State the reasoning.
3. Name the roles needed: Incident Commander (IC), Communications Lead,
   Operations/Ops Lead, Scribe. For a solo responder, note which hats to wear.
4. Recommend whether to declare a formal incident and open a channel/bridge.

## comms

1. Draft an internal status update and (if customer-facing) an external one,
   using the templates in `./reference/comms-templates.md`.
2. State the update cadence for the severity (e.g. SEV1 every 30 min).
3. Keep language factual: known impact, what is being done, next update time.
   No speculation on root cause, no blame, no fabricated ETAs.

## mitigate

1. Prioritize **stopping the bleeding** over root cause: roll back, feature-flag
   off, scale, fail over, shed load.
2. Walk the mitigation decision tree in the skill. Capture each action with a
   timestamp for the timeline.
3. Verify recovery against the original impact signal before declaring resolved.

## postmortem

1. Generate a blameless postmortem scaffold from
   `./reference/postmortem-template.md`, pre-filled with anything known from the
   session (timeline events, severity, impact).
2. Enforce blameless framing: describe systems and decisions given the
   information available at the time, never individuals at fault.
3. Ensure every action item has an owner, a due date, and is concrete and
   verifiable.

Throughout: keep a running, timestamped timeline. Be calm, concrete, and honest
about uncertainty. Do not invent metrics, causes, or customer numbers — mark
unknowns as unknown.
