# Mitigation Catalog (mapped to STRIDE)

Prefer controls that *eliminate* a threat by design over those that only detect it. Map each threat to at least one concrete control below.

## Spoofing → strong authentication
- Enforce MFA for privileged and remote access.
- Use standard, vetted auth (OIDC/OAuth2, SAML); never hand-roll crypto or auth.
- Mutual TLS or signed tokens for service-to-service calls; validate `iss`, `aud`, `exp`, and signature (`alg` pinned).
- Short-lived, rotated credentials; secrets in a manager (Vault, KMS, cloud secret store).
- Rate-limit and lock out on failed auth; monitor credential-stuffing patterns.

## Tampering → integrity controls
- TLS 1.2+ everywhere; HSTS for browsers.
- Server-side validation and canonicalization of all input; parameterized queries / prepared statements.
- Sign and verify artifacts (Sigstore/cosign, package signing); immutable, digest-pinned images.
- Integrity checks (HMAC/checksums) on stored or transmitted critical data.
- Optimistic locking / idempotency keys to defeat races and replay.

## Repudiation → auditability
- Structured, append-only audit logs for security-relevant events (who, what, when, from where, outcome).
- Ship logs to a store the acting principal cannot modify (separate account/WORM/SIEM).
- Synchronized, trusted timestamps; correlation IDs across services.
- Avoid shared accounts; attribute actions to individual identities.

## Information disclosure → confidentiality controls
- Encrypt in transit (TLS) and at rest (KMS-managed keys); classify data and apply least exposure.
- Return only the fields the caller needs; enforce per-tenant/per-user scoping on every read (defeat IDOR).
- Generic error messages to clients; detailed errors only to server logs.
- Keep secrets out of code, URLs, client bundles, and logs; scan for leaked secrets in CI.
- Disable directory listing, debug endpoints, and verbose headers in production.

## Denial of service → availability controls
- Rate limiting and quotas per identity/IP; request size and pagination limits.
- Timeouts, retries with backoff + jitter, circuit breakers, bulkheads.
- Bounded resource use; guard against ReDoS, zip/XML bombs, unbounded recursion.
- Autoscaling, load shedding, and graceful degradation; CDN/WAF for edge absorption.

## Elevation of privilege → authorization controls
- Enforce authorization server-side on every request; deny by default.
- Least privilege for roles, tokens, service accounts, and infra IAM.
- Object-level checks (does *this* subject own *this* resource?) to stop horizontal escalation.
- Validate all inputs a privileged component acts on (avoid confused deputy); block SSRF via allowlists and metadata-endpoint protection.
- Run workloads as non-root with dropped capabilities; safe deserialization (allowlist types).

## Cross-cutting
- Secure defaults; fail closed. Defense in depth — never rely on a single control.
- Threat-model again when trust boundaries, data sensitivity, or the tech stack changes.
