# SOC 2 Mapping (reference)

SOC 2 is built on the AICPA Trust Services Criteria (TSC). The Security ("Common Criteria", CC) category is mandatory; Availability, Confidentiality, Processing Integrity, and Privacy are optional add-ons. Map checklist findings to the criteria below. These are category-level references, not a substitute for your auditor's control matrix.

## Common Criteria (CC) — Security

- **CC6.1 – Logical access / least privilege.** Access controls restrict who can reach systems and data. → Maps to the *access control* checklist category.
- **CC6.2 – Registration & authorization of users.** User provisioning and de-provisioning. → access control.
- **CC6.3 – Role-based access.** Access based on roles and responsibilities. → access control.
- **CC6.6 – Boundary protection.** Protect against external threats (auth on endpoints, network controls). → access control.
- **CC6.7 – Data in transit / transmission.** Encryption of data moving across boundaries. → encryption.
- **CC6.8 – Malicious software / integrity of code.** Controls over unauthorized/ malicious code. → change management.
- **CC7.1 – Detection of vulnerabilities.** Monitoring for new vulnerabilities and misconfig. → logging & monitoring.
- **CC7.2 – Security event monitoring.** Monitor and detect security events. → logging & monitoring.
- **CC7.3 / CC7.4 – Incident evaluation & response.** Respond to and remediate security incidents. → incident response.
- **CC8.1 – Change management.** Changes to infrastructure, data, and software are authorized, tested, and approved. → change management.

## Confidentiality (optional)

- **C1.1 / C1.2 – Confidential information is identified, protected, and disposed of.** → data handling, encryption, retention.

## Availability (optional)

- **A1.2 – Backups and recovery / environmental protections.** → incident response (backup/restore).

## Usage notes

- Cite the criterion at category level (e.g. "CC6.1 – logical access") rather than inventing sub-points.
- A single checklist gap may map to multiple criteria; list the primary one first.
- SOC 2 evaluates the *operating effectiveness* of controls over a period, not just their existence — flag when a control exists in code but has no evidence of consistent operation.
