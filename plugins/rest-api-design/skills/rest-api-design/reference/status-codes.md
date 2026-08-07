# HTTP status codes — when to use each

Pick the most specific code. The class (2xx/4xx/5xx) tells the client who is responsible.

## 2xx — success

| Code | Name | Use when |
|------|------|----------|
| 200 | OK | Successful `GET`, or `PUT`/`PATCH` returning the updated resource. |
| 201 | Created | Resource created by `POST`/`PUT`. Include a `Location` header pointing to it. |
| 202 | Accepted | Request accepted for async processing; work not yet done. Return a status URL. |
| 204 | No Content | Success with no body — typically `DELETE`, or a `PUT` that returns nothing. |

## 3xx — redirection

| Code | Name | Use when |
|------|------|----------|
| 301 | Moved Permanently | Resource permanently at a new URL (e.g. after restructuring). |
| 304 | Not Modified | Conditional `GET` (`If-None-Match`/`ETag`) and the client's copy is current. |

## 4xx — client error

| Code | Name | Use when |
|------|------|----------|
| 400 | Bad Request | Malformed syntax, unparseable body, missing required param. |
| 401 | Unauthorized | No/invalid credentials. (Means *unauthenticated*.) |
| 403 | Forbidden | Authenticated but not permitted. Do not use `404` to hide unless leakage matters. |
| 404 | Not Found | Resource does not exist (or is hidden from this caller). |
| 405 | Method Not Allowed | Path exists but method isn't supported. Include an `Allow` header. |
| 409 | Conflict | State conflict — duplicate unique key, edit conflict, version mismatch. |
| 410 | Gone | Resource existed but is permanently removed. |
| 415 | Unsupported Media Type | `Content-Type` the endpoint can't accept. |
| 422 | Unprocessable Entity | Syntactically valid but semantically invalid (business/validation rules). |
| 428 | Precondition Required | Server requires a conditional request (e.g. `If-Match`) to prevent lost updates. |
| 429 | Too Many Requests | Rate/quota exceeded. Include `Retry-After`. |

## 5xx — server error

| Code | Name | Use when |
|------|------|----------|
| 500 | Internal Server Error | Unexpected server fault. Log with a `request_id`; never leak internals. |
| 502 | Bad Gateway | Invalid response from an upstream dependency. |
| 503 | Service Unavailable | Down, overloaded, or in maintenance. Include `Retry-After`. |
| 504 | Gateway Timeout | Upstream dependency timed out. |

## 400 vs 422

- `400` — the server could not understand the request (bad JSON, wrong types, missing field).
- `422` — the request was understood but violates a business/validation rule (e.g. `end_date` before `start_date`, email already registered).

Be consistent across the whole API: pick one convention and document it.
