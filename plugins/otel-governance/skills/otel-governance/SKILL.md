---
name: otel-governance
description: Use when setting up team- or org-level monitoring or cost controls for Claude Code — enable OpenTelemetry (OTel/OTLP) export of usage telemetry to your own backend and configure organizational spend governance (budgets, alerts, spend caps). Team/enterprise-oriented. Covers the observability-vs-enforcement distinction, the shape of OTel configuration, and where to find authoritative specifics. Triggers on wanting usage dashboards across many seats, per-user/per-team cost attribution, budget alerts, or hard spend caps.
---

# OTel Governance

For teams and organizations running Claude Code across many seats, two capabilities
matter for governance: **observing** usage and cost, and **enforcing** spend
limits. They are related but distinct, and this skill keeps them separate.

Important honesty note: Claude Code supports OpenTelemetry export and Anthropic
provides organizational cost controls, but the exact environment variable names,
settings keys, and Console options change over time and by plan. This skill is
conceptual. For precise identifiers, always confirm against the official Claude
Code telemetry/monitoring documentation and the Anthropic Console — do not rely
on invented flag names.

## Two layers, two mechanisms

1. **Observability via OpenTelemetry** — Claude Code can emit usage telemetry
   (metrics such as token counts and cost, and activity events) using the
   OpenTelemetry protocol (OTLP). You point it at your own OTel-compatible
   backend and get dashboards, attribution, and history. This *measures* usage.

2. **Spend governance** — limiting spend is an account/organization control, not
   a telemetry setting. For API-based org usage this lives in the Anthropic
   Console (usage limits/budgets); enterprise and admin plans add seat and
   workspace governance. This *constrains* usage.

Observability tells you what is happening; governance controls it. A mature setup
uses both: OTel for visibility and alerting (a soft cap), plus organizational
limits for hard enforcement.

## Shape of the OTel configuration

Without asserting exact variable names, a Claude Code OTel export configuration
generally involves:

- **An enable switch** that turns telemetry export on.
- **An OTLP exporter endpoint** — the URL of your collector or vendor ingestion
  point.
- **A protocol** — commonly OTLP over HTTP (protobuf) or gRPC; match what your
  collector accepts.
- **Optional headers** — for authenticating to a managed vendor (e.g. an API key
  header).
- **Exported signals** — usage/cost metrics and activity events; consult the docs
  for the exact metric and event names so you can build dashboards against them.

A typical destination is an OpenTelemetry Collector that fans out to a metrics
store (Prometheus/Grafana) and/or a vendor (Honeycomb, Datadog, New Relic, etc.).
The Collector is a good seam: it lets you re-route, sample, or redact centrally
without reconfiguring every developer's client.

## Spend caps and budgets

Levers for constraining spend, from softest to hardest:

- **Alerts on OTel data** — build a rule in your backend to notify (Slack, email,
  PagerDuty) when spend crosses a threshold per day/week/team. Soft cap: it warns
  but does not stop work.
- **Organization usage limits / budgets** — configured in the Anthropic Console
  for API usage; these are the authoritative spend controls for org accounts.
- **Plan/admin governance** — enterprise and admin-plan controls over seats,
  workspaces, and access, which bound spend structurally.

Because the hard controls live in the Console and plan settings (not in a Claude
Code config file), treat spend enforcement as an admin/finance-owned task and
OTel as the engineering-owned visibility layer.

## Rollout hygiene

- **Pilot first.** Enable telemetry in a staging or single-team workspace, verify
  data arrives and per-user/per-team attribution is correct before org-wide
  rollout.
- **Assign ownership.** Name who owns the dashboards, the alert thresholds, and
  the response when a threshold trips.
- **Config as code.** Where the settings live in files/env, check them into your
  configuration management so the setup is reproducible and reviewable.
- **Privacy and compliance.** Decide what metadata is acceptable to export
  (prompt content should generally not be), and redact sensitive fields at the
  Collector. Confirm the export destination meets your data-residency and
  retention requirements.

## When this is (and isn't) worth it

This is team/enterprise-oriented. A solo developer usually gets enough from the
built-in `/context` and account usage views. Reach for OTel governance when: many
people share a budget, finance needs attribution, or leadership wants usage
trends and guardrails. For the exact variable names, metric names, and Console
paths, go to the official Claude Code telemetry documentation and the Anthropic
Console.
