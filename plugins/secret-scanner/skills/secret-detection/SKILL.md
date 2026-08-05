---
name: secret-detection
description: Detect likely secrets (API keys, cloud credentials, tokens, private keys, high-entropy strings) in code and diffs, triage findings by confidence, and guide safe remediation. Use when scanning a diff for credentials or reviewing a secret-scan result.
---

# Secret detection

A heuristic safety net for catching credentials before they are committed or shared. This is defense-in-depth, not a guarantee. Always pair it with a dedicated scanner (gitleaks, trufflehog, GitHub/GitLab secret scanning) in CI.

## Core method

1. Scope to the diff first. Newly added lines (`+` in `git diff`) are where fresh secrets appear.
2. Match against known credential shapes (see `reference/patterns.md`).
3. For strings without a known prefix, fall back to entropy and context reasoning (see `reference/entropy.md`).
4. Triage each hit: real secret, placeholder/example, or false positive.
5. Recommend remediation — and for anything already pushed, rotation is mandatory.

## Triage confidence

- **High**: recognizable provider prefix + correct length/charset (e.g. `AKIA…`, `ghp_…`, `sk-…`, `-----BEGIN … PRIVATE KEY-----`).
- **Medium**: assignment to a secret-named variable (`password`, `secret`, `token`, `api_key`) with a non-trivial literal value.
- **Low**: high-entropy string with no context; often a hash, UUID, or lockfile digest — verify before alarming.

## Known false positives

Commit SHAs, lockfile integrity hashes (`sha512-…`), UUIDs, base64 test fixtures, and documented example keys (AWS `EXAMPLE` keys, Stripe test keys `sk_test_…`). Do not treat these as live secrets, but do note test-mode keys.

## Remediation (state plainly)

- Remove the secret from the working tree and replace with an env var or secret manager reference.
- If it was ever committed or pushed: **rotate/revoke the credential** — deletion does not undo exposure.
- History rewriting (`git filter-repo`, BFG) may be needed for already-committed secrets, coordinated with the team.

## References (load on demand)

- `reference/patterns.md` — provider-specific regex patterns and prefixes.
- `reference/entropy.md` — entropy heuristics and thresholds for unknown strings.
