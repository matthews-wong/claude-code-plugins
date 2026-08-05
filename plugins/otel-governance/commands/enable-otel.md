---
name: enable-otel
description: Walk through enabling OpenTelemetry export of Claude Code usage metrics/traces and configuring team spend caps for governance. Team/enterprise-oriented.
args: "<your telemetry backend and any governance goals, optional>"
---

You are helping a team enable OpenTelemetry (OTel) export for Claude Code and set
up spend governance. Context from the user:

$ARGUMENTS

This is a team/enterprise-oriented task: individual developers rarely need it,
but organizations use it to observe usage across many seats and enforce budgets.
Be honest and conceptual — Claude Code supports OTel export and organizational
spend controls, but exact env var names, settings keys, and console options
evolve, so confirm current specifics against the official Claude Code
telemetry/monitoring documentation and the Anthropic Console rather than
asserting flags you are not sure of.

Work through these steps:

1. Clarify the goal and the destination. What does the team want — cost
   visibility, per-user/per-team attribution, usage dashboards, alerting, or hard
   spend caps? Which OTel-compatible backend will receive the data (e.g. an OTLP
   collector feeding Prometheus/Grafana, Honeycomb, Datadog, or another vendor)?

2. Explain the two layers of governance, because they are different mechanisms:
   - **Observability (OTel export)** — Claude Code can emit usage telemetry
     (metrics, and events/traces) via the OpenTelemetry protocol so the team can
     see token usage, cost, and activity in their own backend. This is
     configured through Claude Code's telemetry settings/environment (an enable
     switch plus an OTLP endpoint and protocol, and optionally headers for auth).
   - **Spend caps / budgets** — enforcing a maximum spend is an organizational
     control managed at the account/organization level (in the Anthropic Console
     for API-key-based org usage, and via enterprise/admin plan controls). OTel
     tells you what is being spent; spend caps limit it. Make clear these are
     complementary, not the same setting.

3. For the OTel setup, describe the shape of the configuration without inventing
   exact identifiers:
   - A switch to enable telemetry export.
   - An OTLP exporter endpoint (where to send data) and protocol (e.g.
     HTTP/protobuf or gRPC).
   - Optional authentication headers for the collector/vendor.
   - What signals are exported (usage/cost metrics; activity events) and how to
     confirm data is arriving in the backend.
   Point the user to the official telemetry docs for the precise variable names
   and to their vendor's OTLP ingestion guide for the endpoint format.

4. For spend governance, describe the levers honestly:
   - Organization-level usage limits / budgets configured in the Anthropic
     Console for API usage.
   - Admin/enterprise plan controls for seat and workspace governance.
   - Using the OTel data to build alerts (e.g. notify when weekly spend crosses a
     threshold) as a soft cap complementing any hard limits.

5. Recommend rollout hygiene: start in a staging/pilot workspace, verify
   telemetry lands and attribution is correct, agree on who owns dashboards and
   alerts, document the config as code where possible, and only then roll the
   settings out org-wide. Note privacy/compliance: decide what metadata is
   acceptable to export and scrub anything sensitive.

Close with a short checklist the team can follow, and clearly flag every place
where they must confirm an exact name/option against current official docs.
Consult the `otel-governance` skill for the fuller conceptual reference.
