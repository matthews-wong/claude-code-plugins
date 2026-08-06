# threat-modeling

A skill-first Claude Code plugin that runs a **STRIDE** threat model on a feature or design.

## What it does
Auto-invokes when you ask to "threat model" something, request a "security design review", or mention "STRIDE", "attack surface", or "trust boundaries". It decomposes the system, enumerates threats across Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, and Elevation of privilege, rates them, and maps concrete mitigations.

## Structure
- `skills/threat-modeling/SKILL.md` — lean method and output format.
- `skills/threat-modeling/reference/stride-matrix.md` — applicability matrix + per-category threat prompts.
- `skills/threat-modeling/reference/mitigations.md` — control catalog mapped to STRIDE.
- `skills/threat-modeling/reference/example.md` — worked mini model.

## Usage
Describe the feature or paste a design/data-flow, then ask for a threat model. The skill activates automatically.

## License
MIT © Matthews Wong
