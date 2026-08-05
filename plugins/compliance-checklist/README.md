# compliance-checklist

Claude Code plugin providing a pre-release control checklist mapped to **SOC 2** (Trust Services Criteria) and **ISO/IEC 27001** (Annex A). Covers five control categories: access control, change management, logging & monitoring, encryption, and incident response.

## Components

- **`/compliance-check [soc2|iso27001|both]`** — runs the checklist against the current change set, grades each control (Pass / Gap / N/A / Needs-evidence), maps findings to framework controls, and gives a Go / No-go verdict.
- **`compliance-checklist` skill** — auto-triggers on release reviews and audit-readiness work. Lean inline checklist; framework detail lives in `reference/soc2.md` and `reference/iso27001.md`, loaded only for the requested framework (progressive disclosure).

## Usage

```
/compliance-check both
/compliance-check soc2
```

## Notes

Control mappings are category-level references to real SOC 2 TSC and ISO 27001:2022 Annex A controls, intended to guide review — not to replace a formal audit or your auditor's control matrix. No control numbers or audit outcomes are fabricated.

MIT licensed. Author: Matthews Wong.
