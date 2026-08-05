---
name: compliance-check
description: Run a pre-release control checklist against the change set and map findings to SOC 2 / ISO 27001 control categories.
args: "[framework] — optional: soc2, iso27001, or both (default both)"
---

Run a pre-release compliance review. Target framework: `$ARGUMENTS` (default: both SOC 2 and ISO 27001).

Procedure:

1. **Scope the review.** Identify what is shipping — read the diff, changed files, migrations, config, and infra changes. If nothing is staged, ask the user what release or change set to review.

2. **Load the `compliance-checklist` skill** and walk its five control categories: access control, change management, logging & monitoring, encryption, and incident response. For each category, check the relevant items against the actual change set — do not assume a control exists unless there is evidence (code, config, docs, or a stated process).

3. **Map to frameworks.** For each finding, cite the relevant SOC 2 Trust Services Criteria and/or ISO 27001 Annex A control category from the skill's reference files. Load `reference/soc2.md` and/or `reference/iso27001.md` only for the requested framework(s).

4. **Grade each item** as Pass / Gap / N/A / Needs-evidence. Never mark Pass without concrete evidence; use Needs-evidence when the control likely exists but is not visible in the change set.

5. **Output** a checklist table (Category | Control | Status | Evidence/Finding | Framework mapping), then a release-readiness verdict (Go / Go-with-conditions / No-go) with the blocking gaps listed first.

Be rigorous and honest: a compliance check that rubber-stamps is worse than none. Do not fabricate control numbers or audit outcomes; when unsure of an exact mapping, name the category and say the mapping is approximate.
