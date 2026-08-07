# Endpoint examples

Worked examples applying the conventions. Base path is versioned: `/v1`.

## Collection + item CRUD

```
GET    /v1/orders            -> 200  list (paginated)
POST   /v1/orders            -> 201  create (+ Location: /v1/orders/{id})
GET    /v1/orders/{id}       -> 200  fetch one   | 404 if missing
PUT    /v1/orders/{id}       -> 200  full replace (idempotent) | 404
PATCH  /v1/orders/{id}       -> 200  partial update
DELETE /v1/orders/{id}       -> 204  no content (idempotent)   | 404
```

## Create — request & response

Request:

```http
POST /v1/orders HTTP/1.1
Content-Type: application/json
Idempotency-Key: 2f8a...c1

{ "customer_id": "cus_123", "items": [{ "sku": "ABC", "qty": 2 }] }
```

Response:

```http
HTTP/1.1 201 Created
Location: /v1/orders/ord_789

{
  "data": {
    "id": "ord_789",
    "customer_id": "cus_123",
    "status": "pending",
    "items": [{ "sku": "ABC", "qty": 2 }],
    "created_at": "2026-08-07T09:30:00Z"
  }
}
```

Retrying with the same `Idempotency-Key` replays this exact response instead of creating a second order.

## Validation failure (422) — consistent envelope

```http
HTTP/1.1 422 Unprocessable Entity

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more fields are invalid.",
    "details": [
      { "field": "items[0].qty", "issue": "must be >= 1" },
      { "field": "customer_id", "issue": "is required" }
    ],
    "request_id": "req_01HZY..."
  }
}
```

## Cursor pagination

Request:

```
GET /v1/orders?status=open&sort=-created_at&page[size]=20&page[cursor]=eyJpZCI6...
```

Response:

```json
{
  "data": [ /* ...up to 20 orders... */ ],
  "page": {
    "next_cursor": "eyJpZCI6Im9yZF83ODkifQ==",
    "has_more": true
  }
}
```

Rules applied: `page[size]` capped server-side at 100; opaque cursor encodes the keyset position; omit `next_cursor` (or return `null`) when `has_more` is false.

## Sub-resource for a non-CRUD action

Prefer a resource over a verb path:

```
POST /v1/orders/{id}/refunds     -> 201  creates a refund (a real resource)
```

not:

```
POST /v1/orders/{id}/refund      # verb in path — avoid
```

## Filtering & sorting conventions

- Filter by field equality: `?status=open&customer_id=cus_123`
- Sort with a leading `-` for descending: `?sort=-created_at,name`
- Keep query params `snake_case` or `kebab-case` — consistent with your path style — and documented.
