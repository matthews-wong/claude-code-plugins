# Entropy heuristics for unknown strings

When a string has no recognizable provider prefix, entropy plus context is the fallback signal. Entropy alone is noisy — always confirm with surrounding context.

## Shannon entropy intuition

Shannon entropy measures unpredictability per character (in bits). Random-looking credentials pack more entropy than English prose or code identifiers.

Rough thresholds (per-character Shannon entropy):
- English text / normal identifiers: ~1.0-3.5 bits/char.
- Base64 / hex secrets: ~4.0-6.0 bits/char.

A practical rule: flag string literals **20+ characters** long with entropy above ~4.0 bits/char (base64) or ~3.0 (hex), especially when assigned to a secret-named variable.

## Context multipliers

Raise confidence when the high-entropy value is:
- Assigned to a key named `secret`, `token`, `key`, `password`, `credential`.
- On a newly added (`+`) diff line.
- In a `.env`, config, or CI workflow file.
- Adjacent to a provider name (aws, stripe, github).

Lower confidence when it is:
- A commit SHA (40 hex) or short SHA.
- A lockfile integrity hash (`sha512-…`, `sha1-…`) in `package-lock.json`, `yarn.lock`, `Cargo.lock`.
- A UUID (`8-4-4-4-12` hex layout).
- A content hash, asset fingerprint, or snapshot digest.
- Inside a test fixture clearly labeled as fake.

## Why not rely on entropy alone

High entropy produces many false positives (hashes, IDs, minified code) and misses low-entropy-but-real secrets (short PINs, dictionary passphrases). Use it as one input to triage, not the sole verdict.
