---
name: threat-modeling
description: Use when the user asks to "threat model" a feature or system, wants a "security design review", mentions "STRIDE", "attack surface", "trust boundaries", "data flow diagram", or asks "what could go wrong security-wise" with a design. Produces a structured STRIDE threat model with prioritized, mapped mitigations.
---

# STRIDE Threat Modeling

Produce a structured, actionable threat model. Do not guess at the system — anchor every threat to a concrete component, data flow, or trust boundary you can name from the input.

## Method (follow in order)

1. **Scope & assets.** State what is being modeled and list the assets worth protecting (data, credentials, funds, availability, reputation). Note the security objectives (CIA + accountability).
2. **Decompose the system.** Identify external entities, processes, data stores, and data flows. Draw trust boundaries where privilege or trust level changes (internet↔app, app↔DB, service↔service, tenant↔tenant). A data-flow sketch (even ASCII) sharpens the analysis.
3. **Enumerate threats per element with STRIDE.** For each element crossing a trust boundary, walk the six categories. Use the element→category applicability table in `reference/stride-matrix.md` so you don't force irrelevant categories.
4. **Rate each threat.** Assign Likelihood x Impact (Low/Med/High) or a DREAD-style note. Be explicit about assumptions; never invent breach statistics or CVSS numbers.
5. **Map mitigations.** Every High/Medium threat gets at least one concrete mitigation mapped to a control. Pull specifics from `reference/mitigations.md`. Prefer eliminating the threat (design change) over detecting it.
6. **Residual risk & follow-ups.** List threats accepted, deferred, or needing owner decisions.

## Output format

Deliver:
- **Scope & assumptions** (short)
- **Decomposition** (entities, data stores, flows, trust boundaries)
- **Threat table** with columns: ID | Element | STRIDE category | Threat | Likelihood | Impact | Mitigation | Status
- **Prioritized mitigation list** (High first)
- **Open questions** for the design owner

## STRIDE at a glance

| Category | Violates | Question to ask |
|---|---|---|
| **S**poofing | Authentication | Can an actor pretend to be someone/something else? |
| **T**ampering | Integrity | Can data or code be modified in transit or at rest? |
| **R**epudiation | Non-repudiation | Can an actor deny an action with no proof otherwise? |
| **I**nfo disclosure | Confidentiality | Can data leak to an unauthorized party? |
| **D**enial of service | Availability | Can the system be made unavailable or degraded? |
| **E**levation of privilege | Authorization | Can an actor gain rights they should not have? |

## References (load as needed)

- `reference/stride-matrix.md` — element↔category applicability + threat prompts per category.
- `reference/mitigations.md` — canonical control catalog mapped to each STRIDE category.
- `reference/example.md` — a worked mini threat model for a web upload feature.

Keep the model proportional to the risk of the feature. A login flow warrants deep S/E analysis; a static marketing page does not.
