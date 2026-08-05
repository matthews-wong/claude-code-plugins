# Blameless postmortem template

Principle: everyone acted reasonably given what they knew at the time. Analyze
systems and decisions, not people. The goal is prevention, not attribution.

```markdown
# Postmortem: <incident title>

- **Date of incident:** <date>
- **Authors:** <names>
- **Status:** Draft | In review | Final
- **Severity:** SEV<n>
- **Duration:** <start UTC> - <end UTC> (<total>)

## Summary
Two or three sentences: what happened, the user impact, and how it was resolved.

## Impact
- Users affected: <count or %, or [unknown]>
- Services/features affected: <list>
- Business impact: <errors, failed transactions, SLA/SLO breach — facts only>

## Timeline (UTC)
| Time | Event |
|------|-------|
| <ts> | <detection: how we found out> |
| <ts> | <declared SEV<n>, IC assigned> |
| <ts> | <key diagnostic / mitigation action> |
| <ts> | <mitigation applied> |
| <ts> | <recovery verified / resolved> |

## Root cause / contributing factors
Describe the systemic and technical factors that combined to cause the incident.
Prefer "the deploy pipeline allowed X" over "person did X." Use the 5 Whys or a
causal chain. Distinguish trigger from underlying cause.

## Detection
How was it detected? Alert, customer report, or manual? Time to detect. Could a
signal have caught it sooner?

## Response
What went well; what was slow or confusing. Communication effectiveness.

## What went well
- <e.g. rollback was fast and clean>

## What went poorly
- <e.g. no alert on this error class>

## Where we got lucky
- <e.g. off-peak traffic limited impact>

## Action items
| Action | Type (prevent/detect/mitigate) | Owner | Due | Tracking |
|--------|-------------------------------|-------|-----|----------|
| <concrete, verifiable action> | prevent | <name> | <date> | <ticket> |

## Lessons learned
Durable takeaways that outlive this specific incident.
```

## Facilitation notes

- Keep language neutral and blameless throughout, including the timeline.
- Every action item must be specific, owned, dated, and tracked — no "we should
  probably" items.
- Prioritize action items that prevent recurrence or improve detection over
  one-off fixes already completed.
- Schedule the review within a few days while memory is fresh; circulate the
  draft first.
