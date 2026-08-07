---
name: rest-api-design
description: Use when designing, building, or reviewing a REST API or HTTP endpoint — defining routes/paths, choosing HTTP methods and status codes, shaping request/response bodies and error responses, adding pagination, versioning an API, or handling idempotency. Triggers on "REST", "API", "endpoint", "route", "HTTP status code", "pagination", "API versioning", "error response", "idempotent", and on OpenAPI/Swagger specs and controller/router files. Provides opinionated resource-oriented design conventions.
---

# REST API Design

Opinionated conventions for resource-oriented HTTP APIs that are predictable, consistent, and safe to evolve.

## Resource naming

- Paths are **nouns**, not verbs. The HTTP method is the verb. `POST /orders`, not `POST /createOrder`.
- Use **plural** collection names: `/users`, `/users/{id}`, `/users/{id}/orders`.
- **kebab-case** multi-word segments: `/purchase-orders`, not `/purchaseOrders` or `/purchase_orders`.
- Nest to show ownership one level deep; beyond that, prefer query filters. `/users/{id}/orders` is fine; `/users/{id}/orders/{oid}/items/{iid}/tax` is not — expose `/order-items/{iid}`.
- Actions that aren't CRUD map to a sub-resource or a state field, not a verb path: prefer `POST /orders/{id}/refunds` or `PATCH /orders/{id}` with `{ "status": "cancelled" }` over `POST /orders/{id}/cancel`.
- Filtering, sorting, pagination live in the **query string**: `GET /orders?status=open&sort=-created_at&page[size]=20`.

## HTTP methods & idempotency

- `GET` (safe, cacheable), `POST` (create/non-idempotent), `PUT` (full replace, **idempotent**), `PATCH` (partial update), `DELETE` (**idempotent**).
- `PUT` and `DELETE` must be idempotent: repeating the call yields the same end state. A second `DELETE` of a gone resource returns `404` (or `204`), never a new side effect.
- Make `POST` creates safe to retry with an **`Idempotency-Key`** request header: store the key + result, and replay the stored response on a repeat.

## Status codes — use the specific one

Return the most precise code; never `200` for everything. Full table in `reference/status-codes.md`.

- `200` OK · `201` Created (+ `Location` header) · `202` Accepted (async) · `204` No Content (empty body, e.g. DELETE).
- `400` malformed · `401` unauthenticated · `403` authenticated-but-forbidden · `404` not found · `409` conflict · `422` semantic validation failure · `429` rate limited.
- `500` unexpected · `503` down/overloaded. Never leak stack traces to clients.

## Consistent error envelope

Every error shares one shape so clients parse once. Include a stable machine `code`, a human `message`, and field-level `details` where relevant:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request body failed validation.",
    "details": [{ "field": "email", "issue": "must be a valid email address" }],
    "request_id": "req_01HZY..."
  }
}
```

Success and error responses must be distinguishable without guessing. See `reference/endpoint-examples.md`.

## Pagination

- Default and **cap** page size (e.g. default 20, max 100) — never return an unbounded list.
- Prefer **cursor/keyset** pagination for large or high-write datasets; offset pagination drifts and slows at depth.
- Return pagination metadata consistently (`next_cursor`, `has_more`, or `total` when cheap to compute).

## Versioning & validation

- Version in the **URL path**: `/v1/orders`. It is explicit, cache-friendly, and unambiguous in logs. Bump the major version only for breaking changes; add fields backward-compatibly within a version.
- **Validate at the edge**: reject unknown/invalid input at the boundary with `400`/`422` before any business logic runs. Validate types, required fields, and ranges; fail with the error envelope above.

## References

- `reference/status-codes.md` — when to use each status code.
- `reference/endpoint-examples.md` — worked request/response examples.
