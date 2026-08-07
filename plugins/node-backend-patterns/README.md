# node-backend-patterns

A skill-first Claude Code plugin for opinionated Node.js backend patterns.

Auto-invokes when you write or review Node/Express/Fastify server code — route handlers, middleware, services, config, logging, and process lifecycle.

## What it encourages

- Layered architecture: route → service → data, grouped by feature
- Validate every external input at the boundary (zod/schema)
- Centralized async error handling with a consistent error envelope
- Env-based config validated at startup; no secrets in code
- Structured JSON logging with a per-request correlation id
- Never block the event loop; graceful shutdown on `SIGTERM`/`SIGINT`

## Contents

- `skills/node-backend-patterns/SKILL.md` — lean guidance and decision rules
- `skills/node-backend-patterns/reference/config-and-error-middleware.md` — env schema + async error middleware
- `skills/node-backend-patterns/reference/graceful-shutdown.md` — logging + clean teardown

## License

MIT © Matthews Wong
