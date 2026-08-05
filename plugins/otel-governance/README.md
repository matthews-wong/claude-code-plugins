# otel-governance

Governance plugin for Claude Code. Enable OpenTelemetry (OTel) export of usage
telemetry and set up organizational spend governance — observability plus cost
control for teams and enterprises.

## Components

- **Command `/enable-otel`** — walks through choosing a telemetry backend,
  enabling OTel export, and configuring spend caps/budgets, distinguishing
  observability from enforcement.
- **Skill `otel-governance`** — conceptual reference: the two layers (OTLP
  export vs. organizational spend controls), the shape of an OTel configuration,
  spend-cap levers, and rollout hygiene.

## Honesty note

Claude Code supports OTel export and Anthropic provides organizational cost
controls, but exact environment variable names, settings keys, and Console
options change over time and by plan. This plugin is deliberately conceptual and
points you to the official Claude Code telemetry/monitoring documentation and the
Anthropic Console for precise, current identifiers rather than asserting flags.

## Scope

Team/enterprise-oriented. Solo developers usually get enough from the built-in
`/context` and account usage views.

Author: Matthews Wong · License: MIT
