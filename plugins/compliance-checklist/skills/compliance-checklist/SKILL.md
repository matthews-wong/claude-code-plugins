---
name: compliance-checklist
description: Pre-release security & compliance control checklist mapped to SOC 2 and ISO 27001. Use when preparing a release, doing a go/no-go review, an audit-readiness pass, or when the user mentions SOC 2, ISO 27001, access control, change management, audit logging, encryption, or incident response. Triggers on "compliance check", "pre-release review", "SOC 2", "ISO 27001", "audit readiness", "control gap".
---

# Compliance Checklist

A lean, framework-mapped control checklist for pre-release reviews. Grade each item **Pass / Gap / N/A / Needs-evidence** — never Pass without evidence.

## Five control categories

### 1. Access control
- Least-privilege enforced; no wildcard/admin defaults.
- Auth required on every non-public endpoint; authz checked server-side.
- No hardcoded credentials; secrets from a manager/env, not the repo.
- MFA / SSO for privileged access where applicable.

### 2. Change management
- Change went through PR review and CI checks.
- Migrations are reversible or have a documented rollback.
- Release is versioned and traceable to an approved change.
- No direct-to-production changes bypassing the pipeline.

### 3. Logging & monitoring
- Security-relevant events logged (authn, authz failures, admin actions).
- Logs exclude secrets and raw PII (masked/tokenized).
- Logs are tamper-resistant and retained per policy.
- Alerting exists for anomalies / failures.

### 4. Encryption
- TLS for all data in transit.
- Sensitive data encrypted at rest.
- Keys managed by a KMS; no keys in the repo; rotation defined.
- Strong, current algorithms (no MD5/SHA1 for security, no weak ciphers).

### 5. Incident response
- On-call / escalation path defined.
- Runbook exists for this component's likely failures.
- Breach/incident notification process referenced.
- Backups exist and restore is tested.

## How to use

Walk each category against the actual change set. Cite evidence for every Pass. Rank gaps by risk and give a Go / Go-with-conditions / No-go verdict.

## Framework mapping (progressive disclosure)

For SOC 2 Trust Services Criteria mappings, read `reference/soc2.md`. For ISO 27001 Annex A control mappings, read `reference/iso27001.md`. Load only the framework you need. These references give the control identifiers; do not invent numbers not listed there.
