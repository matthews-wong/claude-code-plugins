# Secret patterns reference

Recognizable credential shapes. Prefixes are the strongest signal; combine with length and charset to reduce noise. These patterns are illustrative, not exhaustive — providers change formats over time.

## Cloud providers

- **AWS Access Key ID**: `AKIA`, `ASIA`, `AGPA`, `AIDA` followed by 16 uppercase alphanumerics (e.g. `AKIA[0-9A-Z]{16}`). The example key `AKIAIOSFODNN7EXAMPLE` is a documented placeholder.
- **AWS Secret Access Key**: 40-char base64-ish string; low signal alone — flag when near an access key or `aws_secret_access_key`.
- **Google API key**: `AIza[0-9A-Za-z_\-]{35}`.
- **Google OAuth**: strings ending in `.apps.googleusercontent.com`.
- **Azure**: connection strings containing `AccountKey=` or `SharedAccessKey=`.

## Git hosting & CI tokens

- **GitHub**: `ghp_` (classic PAT), `gho_`, `ghu_`, `ghs_`, `ghr_`, and fine-grained `github_pat_` followed by base62.
- **GitLab**: `glpat-` followed by 20 chars.
- **Slack**: `xox[baprs]-` tokens; `xapp-` app tokens.

## SaaS API keys

- **Stripe**: `sk_live_`, `rk_live_` (live — high severity), `sk_test_`, `pk_test_` (test mode — lower).
- **OpenAI / Anthropic style**: `sk-` prefixed keys.
- **SendGrid**: `SG.` followed by two base64 segments.
- **Twilio**: `SK` + 32 hex; account SID `AC` + 32 hex.
- **npm**: `npm_` followed by 36 chars.
- **PyPI**: `pypi-` tokens.

## Private keys and certs

- PEM blocks: `-----BEGIN RSA PRIVATE KEY-----`, `-----BEGIN OPENSSH PRIVATE KEY-----`, `-----BEGIN EC PRIVATE KEY-----`, `-----BEGIN PRIVATE KEY-----`, `-----BEGIN PGP PRIVATE KEY BLOCK-----`.
- `.pem`, `.key`, `.p12`, `.pfx`, `id_rsa`, `id_ed25519` files by name.

## Generic credential assignments

Flag assignments where a secret-named key gets a non-empty, non-placeholder literal:
`(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret)\s*[:=]\s*["'][^"']{8,}["']`

## Connection strings / URLs with inline credentials

`(postgres|postgresql|mysql|mongodb|redis|amqp)://[^:@/]+:[^@/]+@` — password embedded in a URL.
