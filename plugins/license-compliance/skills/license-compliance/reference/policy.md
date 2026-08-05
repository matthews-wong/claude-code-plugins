# Allowlist / denylist policy model

A license policy classifies each SPDX identifier into an action. Tailor it to how the software is delivered — obligations differ between an internal tool, a distributed binary, and a hosted SaaS.

## Actions

- **Allow** — no review needed.
- **Flag / review** — permitted only with a documented decision and sometimes obligations to satisfy (attribution, NOTICE, source offer).
- **Deny** — not permitted without an explicit, senior/legal sign-off or a commercial license.

## Default policy (proprietary, distributed software)

Adjust to your context; make assumptions explicit when the project has no stated policy.

**Allow (permissive):**
`MIT`, `BSD-2-Clause`, `BSD-3-Clause`, `Apache-2.0`, `ISC`, `Unlicense`, `CC0-1.0`, `Zlib`, `BSL-1.0`, `Python-2.0`

> Apache-2.0 is allowed but carries a NOTICE-file and patent-termination clause — preserve NOTICE and attributions.

**Flag (weak copyleft — usually OK with care):**
`MPL-2.0`, `LGPL-2.1-*`, `LGPL-3.0-*`, `EPL-2.0`, `CDDL-1.0`

> Weak copyleft reciprocates at file/library scope; dynamic linking and keeping modifications separate usually preserves your proprietary code, but confirm per case.

**Deny in proprietary distribution (strong copyleft):**
`GPL-2.0-*`, `GPL-3.0-*`, `AGPL-3.0-*`, `SSPL-1.0`

> Strong copyleft can require releasing your combined work's source. **AGPL** extends this to network/SaaS use even without distributing binaries — treat as deny for hosted services.

**Always block until resolved:**
`UNKNOWN`, `NOASSERTION`, custom/proprietary "all rights reserved", and any license whose text you cannot obtain.

## Context modifiers

- **SaaS / hosted only, no distribution**: GPL (non-Affero) obligations may not trigger on mere hosting, but **AGPL does** — keep AGPL denied. Still document the reasoning.
- **Internal-only tooling, never distributed**: copyleft risk is lower, but policies often stay strict to avoid future distribution surprises.
- **Shipping to customers / on-prem / mobile app**: strictest interpretation — distribution triggers most copyleft obligations.

## Decision record

Every "flag" that is accepted and every "deny" that is overridden needs: dependency + version, SPDX id, delivery context, rationale, approver, and review date. This is the artifact auditors and acquirers ask for.

## Not legal advice

This model supports an engineering/compliance decision. For genuine legal questions — dual-license interpretation, patent clauses, combined-work analysis — involve counsel.
