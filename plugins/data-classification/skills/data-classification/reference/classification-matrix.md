# Classification Matrix (reference)

Detailed rules for the `data-classification` skill. Load on demand.

## Tier definitions

### public
Data intentionally available to anyone. No confidentiality obligation.
Examples: published product names, public GitHub repo URLs, marketing content, public API version numbers, opaque public identifiers not linkable to a person.

### internal
Operational data restricted to the organization but not damaging if leaked.
Examples: internal ticket/issue IDs, non-sensitive service names, feature-flag names, build numbers, internal dashboards URLs, non-secret configuration.

### confidential
Business-sensitive data causing material harm, access escalation, or legal exposure if disclosed.
Examples: API keys, tokens, passwords, private keys, connection strings, encryption keys, financial statements, unreleased roadmaps, contracts, vulnerability details, security configuration, pricing models.

### PII (personal data)
Any data relating to an identified or identifiable natural person.

**Direct identifiers:** full name, email, phone, postal address, government ID (SSN/passport/national ID), driver's license, username tied to a real person, photo/face.

**Indirect / quasi-identifiers:** IP address, device ID, cookie ID, precise geolocation, date of birth, employer + job title combos.

**Sensitive PII (strictest handling):** health/medical data, biometric data, genetic data, financial account numbers, payment card data (PCI scope), racial/ethnic/religious/political/sexual-orientation data, precise location history, children's data.

## Field-name keyword map (heuristic, verify semantics)

- PII: `name`, `first_name`, `last_name`, `email`, `phone`, `mobile`, `address`, `street`, `zip`, `postcode`, `dob`, `birth`, `ssn`, `nin`, `passport`, `national_id`, `ip`, `ip_addr`, `geo`, `lat`, `lng`, `location`, `device_id`, `user_agent`, `photo`, `avatar_upload`.
- Sensitive PII: `health`, `diagnosis`, `medical`, `biometric`, `fingerprint`, `card`, `pan`, `cvv`, `iban`, `account_number`, `routing`, `salary`, `religion`, `ethnicity`.
- Confidential/secret: `password`, `passwd`, `secret`, `token`, `api_key`, `apikey`, `private_key`, `client_secret`, `connection_string`, `dsn`, `credential`, `session`, `refresh_token`.

Keyword match is a signal, not a verdict — confirm with the field's actual meaning and usage.

## Controls matrix

| Control | internal | confidential | PII | sensitive PII |
|---------|----------|--------------|-----|---------------|
| Encrypt in transit (TLS) | yes | yes | yes | yes |
| Encrypt at rest | recommended | yes | yes | yes (field-level) |
| Tokenize / pseudonymize | no | where feasible | recommended | yes |
| Mask in logs | n/a | never log raw | yes | yes (or never log) |
| Retention limit | as needed | minimize | defined limit | shortest viable |
| Access control | RBAC | least-privilege | least-privilege + audit | least-privilege + audit + justification |
| Minimization review | optional | yes | yes | yes (collect only if required) |
| Right-to-erasure support | n/a | n/a | yes | yes |

## Decision tie-breakers

- Both confidential and PII → apply PII handling plus secret-handling (never log, never commit).
- Ambiguous free-text field that may contain PII (e.g. `notes`, `comment`, `description`) → treat as potential PII; recommend masking in logs and a scanning control.
- Derived/aggregated data that can re-identify individuals → treat as PII.
- Hashed PII (e.g. email hash) → still PII if reversible or linkable; recommend salted, non-reversible transforms and document the purpose.

## Reporting guidance

For each field report: Field | Tier | Rationale | Required Handling. End with risk-ranked action items and an explicit "needs human decision" list for anything ambiguous. Do not cite specific laws unless the repository declares the applicable regime.
