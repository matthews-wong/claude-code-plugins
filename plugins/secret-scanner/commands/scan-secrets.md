---
name: scan-secrets
description: Scan the current working diff for likely secrets (API keys, tokens, private keys, high-entropy strings) using heuristic pattern matching.
---

You are helping the user find secrets that may have been accidentally introduced into their working tree before they commit or share the code.

## What to do

1. Determine the scope of changes to inspect. Prefer the staged and unstaged diff:
   - Run `git diff --staged` and `git diff` to see pending changes.
   - If there is no git repository, or the user asks for a full scan, inspect the relevant working files directly.
2. Run the bundled heuristic scanner to get a fast first pass:
   - `sh "${CLAUDE_PLUGIN_ROOT}/scripts/scan-secrets.sh"`
   - This is a grep-based heuristic. Treat its output as leads, not verdicts.
3. Review the flagged lines yourself. For each finding, judge whether it is:
   - A real secret (a live credential, private key, or token) — highest priority.
   - A placeholder or example (e.g. `AKIAIOSFODNN7EXAMPLE`, `<your-token-here>`, `xxxx`).
   - A false positive (hash of a commit, lockfile integrity string, test fixture).
4. Load the `secret-scanner` skill for the detection patterns, entropy reasoning, and remediation guidance.

## How to report

Group findings by confidence (High / Medium / Low). For each, give the file, line, the pattern that matched, and a one-line recommendation. Be explicit that this is a heuristic safety net and NOT a replacement for a dedicated secret scanner (such as gitleaks, trufflehog, or GitHub secret scanning) or for rotating any credential that may have been exposed.

If a real secret is found, remind the user that removing it from the working tree is not enough once it has been pushed — the credential must be rotated/revoked and history may need to be rewritten.
