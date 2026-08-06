# Worked Example: User Avatar Upload Feature

A compact model showing the expected shape of output.

## Scope & assumptions
- Feature: authenticated users upload an avatar image; it is stored in object storage and served publicly via CDN.
- Assets: user account integrity, other users' data, service availability, storage cost.
- Assumption: users authenticate via existing OIDC; uploads go through the app API.

## Decomposition
- External entity: Browser (user).
- Process: Upload API service.
- Data store: Object storage bucket; metadata row in Postgres.
- Data flows: Browser → API (HTTPS); API → bucket; CDN → Browser.
- Trust boundaries: Internet ↔ API; API ↔ storage.

```
[Browser] --https--> [Upload API] --> [Object Storage] --> [CDN] --> [Browser]
                          |
                          v
                     [Postgres meta]
```

## Threat table

| ID | Element | STRIDE | Threat | Likelihood | Impact | Mitigation | Status |
|----|---------|--------|--------|------------|--------|------------|--------|
| T1 | Upload API | Tampering | Malicious file (SVG with script, polyglot) stored and served | Med | High | Validate MIME + magic bytes; re-encode to PNG/JPEG; serve from cookieless domain; `Content-Disposition` | Open |
| T2 | Upload API | DoS | Huge/many uploads exhaust storage and bandwidth | Med | Med | Max file size, per-user rate limit, quota | Open |
| T3 | Object storage | Info disclosure | Bucket misconfig exposes all objects / other data | Low | High | Least-privilege bucket policy; only avatar prefix public; block public listing | Open |
| T4 | Upload API | Elevation/IDOR | User overwrites another user's avatar by guessing ID | Med | Med | Derive storage key from authenticated user ID, not client input | Open |
| T5 | Data flow | Info disclosure | EXIF GPS metadata leaks user location | Med | Med | Strip metadata on re-encode | Open |

## Prioritized mitigations
1. T1 re-encode + strict type validation (High).
2. T3 bucket least-privilege (High).
3. T2 size/rate limits; T4 server-derived keys; T5 EXIF strip (Med).

## Open questions
- Should avatars be public at all, or served via signed URLs?
- Is there an antivirus/content-scanning step available?
