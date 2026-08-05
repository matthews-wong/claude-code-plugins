# secret-scanner

A heuristic safety net for catching likely secrets — API keys, cloud credentials, tokens, private keys, and high-entropy strings — in your working diff **before** they are committed or shared.

## What it provides

- **`/scan-secrets`** — scans the staged and unstaged diff and reports findings by confidence.
- **`secret-detection` skill** — detection patterns, entropy heuristics, and remediation guidance (progressive disclosure via `reference/`).
- **PreToolUse hook** — runs `scripts/scan-secrets.sh` (POSIX sh, grep-based) as a non-blocking summary before Bash tool calls.

## Important limitations

This is **heuristic** defense-in-depth, not a guarantee. It produces false positives (hashes, UUIDs, lockfile digests) and can miss real secrets. It does **not** replace a dedicated secret scanner such as [gitleaks](https://github.com/gitleaks/gitleaks), [trufflehog](https://github.com/trufflesecurity/trufflehog), or platform-native secret scanning in CI.

If a real credential is found and was ever committed/pushed, **rotate or revoke it** — deleting the line does not undo exposure.

## License

MIT — Matthews Wong
