# STRIDE Applicability Matrix & Threat Prompts

## Element-to-category applicability

Not every STRIDE category applies to every element. Use this to focus.

| Element type | S | T | R | I | D | E |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| External entity (user, 3rd-party) | Y | | Y | | | |
| Process (service, function) | Y | Y | Y | Y | Y | Y |
| Data flow (network, IPC) | | Y | | Y | Y | |
| Data store (DB, cache, queue, file) | | Y | Y* | Y | Y | |

\* Repudiation on a data store applies when it holds audit/log data that could be altered or deleted.

## Threat prompts per category

### Spoofing (authentication)
- Weak/absent authentication on an endpoint or service-to-service call.
- Credential stuffing, reused/leaked passwords, no MFA.
- Missing mutual TLS between services; forged JWT/SAML assertions.
- Session fixation, token theft, predictable session IDs.
- DNS/ARP spoofing, phishing of privileged users.

### Tampering (integrity)
- Unvalidated input mutating state (injection, mass assignment, parameter tampering).
- Man-in-the-middle modifying requests without TLS or integrity checks.
- Mutable build/deploy artifacts; unsigned packages or containers.
- Client-side trust (hidden form fields, price on the client, JWT `alg:none`).
- Cache poisoning; race conditions (TOCTOU).

### Repudiation (non-repudiation / accountability)
- No audit log for security-relevant actions (login, permission change, money movement).
- Logs writable/deletable by the acting principal.
- Shared/service accounts obscuring who did what.
- Missing timestamps, no tamper-evident log storage.

### Information disclosure (confidentiality)
- Sensitive data unencrypted in transit or at rest.
- Verbose errors, stack traces, or debug endpoints leaking internals.
- Over-broad API responses (returning full objects, other tenants' data).
- Secrets in code, logs, URLs, or client bundles.
- Insecure Direct Object Reference (IDOR) exposing others' records.
- Metadata leaks (timing, response size, enumeration).

### Denial of service (availability)
- Unbounded work: no rate limits, no pagination, expensive queries on user input.
- Resource exhaustion (memory, connections, file handles), zip/XML bombs, ReDoS.
- Missing timeouts/circuit breakers causing cascading failure.
- Single points of failure; no autoscaling or graceful degradation.

### Elevation of privilege (authorization)
- Missing or client-side-only authorization checks (broken access control).
- Vertical (user→admin) or horizontal (tenant A→tenant B) escalation.
- Confused deputy: a privileged service acting on unvalidated caller input.
- Insecure defaults, over-privileged roles/tokens, container running as root.
- SSRF pivoting to internal services; deserialization RCE.

## Prioritization guidance

Rate Likelihood x Impact. Escalate when a threat: crosses a trust boundary, touches authentication/authorization, exposes regulated data (PII/PCI/PHI), or has no compensating control. Do not fabricate CVSS scores — reason qualitatively unless the user provides data.
