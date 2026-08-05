---
name: data-classification
description: Classify data fields into public/internal/confidential/PII tiers and recommend handling controls. Use when reviewing schemas, database models, migrations, API payloads, config, or log statements for sensitive data; when the user asks to classify data, find or flag PII, or decide encryption/retention/minimization for a field. Triggers on "classify data", "is this PII", "sensitive fields", "data handling", "should we log this".
---

# Data Classification

Assign every data field a sensitivity tier and the handling it requires. Be conservative: when a field could fit two tiers, pick the stricter one.

## The four tiers (summary)

- **public** — intended for open disclosure; no harm if exposed (marketing copy, public IDs, published docs).
- **internal** — not secret but not for outsiders; low harm if leaked (internal ticket IDs, non-sensitive config, feature flags).
- **confidential** — business-sensitive; real harm if leaked (secrets/keys/tokens, financials, source-controlled credentials, contracts, security config).
- **PII** — identifies or relates to a person (name, email, phone, address, government ID, IP, precise location, biometric, health, financial-personal). Sensitive-PII subsets (health, government ID, financial account) get the strictest handling.

A field can be both **confidential and PII** — apply PII handling as the floor.

## Fast heuristic

1. Does the value identify or describe a person? → **PII**.
2. Would leaking it harm the business or grant access? → **confidential**.
3. Is it internal-only operational data? → **internal**.
4. Is it safe to publish? → **public**.

## Handling by tier (baseline)

| Tier | Encryption | Retention | Logging | Access |
|------|-----------|-----------|---------|--------|
| public | optional | as needed | ok | open |
| internal | in transit | as needed | ok, no secrets | employees |
| confidential | at rest + in transit | minimize | never log raw | least-privilege |
| PII | at rest + in transit | minimize + defined limit | mask/tokenize only | least-privilege + audit |

## Common failure to flag

- PII or secrets written to logs, error messages, analytics, or URLs.
- Credentials committed to the repo or embedded in config.
- Collecting PII with no stated purpose (violates minimization).

## Going deeper

For the full tier definitions, field-name keyword map, sensitive-PII subcategories, and a per-tier controls matrix, read `reference/classification-matrix.md`. Load it only when you need the detailed rules — the summary above covers most decisions.
