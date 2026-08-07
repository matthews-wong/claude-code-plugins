# rest-api-design

A skill-first Claude Code plugin for opinionated REST API design.

Auto-invokes when you design or review HTTP endpoints — routes, methods, status codes, error shapes, pagination, idempotency, and versioning.

## What it encourages

- Resource-oriented, noun-based, kebab-case paths (no verbs in URLs)
- The most specific HTTP status code, not `200` for everything
- One consistent error envelope across the whole API
- Bounded, cursor-first pagination
- Idempotent `PUT`/`DELETE` and retry-safe `POST` via `Idempotency-Key`
- URL path versioning and validation at the edge

## Contents

- `skills/rest-api-design/SKILL.md` — lean conventions and decision rules
- `skills/rest-api-design/reference/status-codes.md` — when to use each status code
- `skills/rest-api-design/reference/endpoint-examples.md` — worked request/response examples

## License

MIT © Matthews Wong
