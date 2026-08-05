---
name: incident-response
description: >
  Use during or after a production incident/outage: triaging severity, running
  the response, drafting status comms, deciding mitigation, or writing a
  postmortem. Triggers: "incident", "outage", "we're down", "SEV1/SEV2",
  "on-call", "declare an incident", "status update for customers", "postmortem",
  "root cause analysis", "RCA", "action items". For live production impact and
  the retrospective that follows.
---

# Incident Response

Restore service first, learn second, blame never. Optimize for a fast, calm,
well-communicated recovery, then a blameless retrospective that fixes systems.

## Roles (declare early)

- **Incident Commander (IC)** — owns the response, makes calls, delegates. Not
  necessarily the most senior; the coordinator.
- **Communications Lead** — owns internal/external updates on cadence.
- **Operations Lead** — hands on keyboard executing mitigations.
- **Scribe** — keeps the timestamped timeline.

Solo? You are IC + Ops; write the timeline as you go so the postmortem is easy.

## Severity matrix

| SEV | Meaning | Examples | Response |
|-----|---------|----------|----------|
| SEV1 | Critical: major outage / data loss / security breach | Site down, checkout broken, data exposure | All-hands, IC now, updates every 30 min |
| SEV2 | Major: significant degradation, key feature down | High error rate, one region down | Dedicated responders, updates hourly |
| SEV3 | Minor: partial/limited impact, workaround exists | Slow endpoint, non-critical feature | Normal on-call, updates as needed |
| SEV4 | Low: negligible user impact | Cosmetic, internal-only | Ticket, no live response |

When unsure between two levels, pick the higher one; downgrade later.

## Response flow

1. **Detect & declare** — confirm impact, assign severity, open a channel/bridge.
2. **Assemble** — page roles per severity.
3. **Stabilize** — stop the bleeding before diagnosing (see mitigation tree).
4. **Communicate** — first update within minutes; then on cadence.
5. **Resolve** — verify recovery against the original signal.
6. **Learn** — schedule the blameless postmortem within a few days.

## Mitigation decision tree

- Did a recent change cause it? -> **roll back / revert / disable the flag** first.
- Capacity/traffic? -> scale out, add rate limiting, shed non-critical load.
- Dependency down? -> fail over, use cache/degraded mode, circuit-break.
- Data/corruption? -> stop writes, preserve evidence, restore from backup.
- Security? -> contain (isolate, rotate credentials), preserve logs, involve
  security/legal per policy.

Prefer the reversible, fastest-to-safety action. A clean rollback beats a clever
fix under pressure.

## Communications

Cadence by severity above. Templates (internal + external + resolved) live in
`./reference/comms-templates.md`. Rules: factual, blameless, no unfounded ETAs,
always state the next update time.

## Postmortem

Blameless: assume everyone acted reasonably with the information they had. Focus
on contributing systemic factors and prevention. Full scaffold in
`./reference/postmortem-template.md`. Every action item needs an owner and a
due date.

## Guardrails

- Never invent metrics, customer counts, root causes, or ETAs. Mark unknowns.
- Do not name individuals as causes in any artifact.
- Follow the org's real escalation/legal/security policy for breaches — this is
  guidance, not a substitute for it.
