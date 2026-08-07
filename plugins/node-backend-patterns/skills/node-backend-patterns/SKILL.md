---
name: node-backend-patterns
description: Use when writing or reviewing Node.js backend/server code — Express, Fastify, Koa, or plain http services, route handlers, middleware, controllers, services, or repositories in .js/.ts/.mjs files. Triggers on "Node server", "Express", "Fastify", "middleware", "route handler", "async handler", "env config / environment variables", "structured logging", "graceful shutdown", request validation, and error handling. Provides opinionated layering, boundary-validation, error, config, logging, and lifecycle patterns.
---

# Node.js Backend Patterns

Opinionated defaults for maintainable, resilient Node services.

## Layered architecture (route → service → data)

Keep each layer to one responsibility and let dependencies point inward:

- **Route/controller** — HTTP concerns only: parse & validate input, call a service, map the result to a status code. No business logic, no DB queries.
- **Service** — business rules, orchestration, transactions. Framework-agnostic: no `req`/`res` here, so it stays unit-testable and reusable.
- **Data/repository** — persistence access behind a thin interface you own. Swappable without touching services.

Group files by **feature/domain** (`users/`, `orders/`), each containing its route, service, and repo — not by technical layer folders spread apart.

## Validate at the boundary

Parse and validate every external input (body, params, query, headers) at the route edge *before* it reaches a service. Use a schema library (zod, Joi, or Fastify's JSON Schema). Reject invalid input with `400`/`422` and never let unvalidated data flow inward. Treat validated output as a typed, trusted value. Example in `reference/config-and-error-middleware.md`.

## Centralized async error handling

- Never `try/catch` in every handler and duplicate the response. Route thrown/rejected errors to **one** error-handling middleware (Express) or `setErrorHandler` (Fastify).
- In Express 4, wrap async handlers so rejections reach `next(err)` (an `asyncHandler` wrapper, or Express 5 which forwards automatically). Fastify awaits async handlers natively.
- Throw typed domain errors (e.g. `AppError` with an HTTP status + machine code); the central handler maps them to a consistent JSON error envelope and logs the rest as `500` **without leaking internals or stack traces** to clients.

## Configuration & secrets

- **No secrets in code.** Read all config from environment variables (via `process.env`, `.env` in dev only, or a secret manager in prod). Never commit `.env`.
- **Validate env at startup** with a schema and fail fast if a required var is missing or malformed — a misconfigured process should crash on boot, not midway through a request. Export a single typed `config` object; never scatter `process.env.X` reads through the codebase.

## Structured logging

- Log **structured JSON** (pino or similar), not `console.log` string concatenation. Machine-parseable, queryable, level-aware.
- Attach a **correlation/request id** per request and include it on every log line and error response.
- **Never log secrets or PII** — redact tokens, passwords, auth headers. Pick log level by environment (`debug` in dev, `info`/`warn` in prod).

## Don't block the event loop

- Never use sync FS/crypto calls (`readFileSync`, `pbkdf2Sync`) on the request path. Use async APIs.
- Offload CPU-heavy work (hashing, image processing, large parsing) to a worker thread, a queue, or a separate service. A blocked event loop stalls *every* concurrent request.
- Stream large payloads instead of buffering them entirely in memory.

## Graceful shutdown

Handle `SIGTERM`/`SIGINT`: stop accepting new connections, finish in-flight requests, then close DB pools and other resources before exiting. Add a timeout that force-exits if drain hangs. Pattern in `reference/graceful-shutdown.md`.

## References

- `reference/config-and-error-middleware.md` — env schema + async error middleware.
- `reference/graceful-shutdown.md` — signal handling and clean teardown.
