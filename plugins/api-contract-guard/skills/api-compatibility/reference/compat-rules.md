# Backward-compatibility rule matrix

"Safe" = existing valid clients keep working without changes.

## Endpoints / operations

| Change | Verdict |
|---|---|
| Add new path or operation | Non-breaking |
| Remove path / operation / method | Breaking |
| Change path template (rename param, alter route) | Breaking |
| Change success status code (200 -> 201) | Breaking |
| Add a new 2xx alongside existing | Usually breaking (clients switch on code) |

## Request parameters and body fields

| Change | Verdict |
|---|---|
| Add optional field/param | Non-breaking |
| Add required field/param | Breaking |
| Make required field optional | Non-breaking |
| Make optional field required | Breaking |
| Remove a field the server accepted | Non-breaking to strict senders, but breaking if clients relied on echo; treat removal of *accepted* input as generally safe, removal of *documented* behavior as breaking |
| Tighten validation (add pattern, raise minLength, lower maximum) | Breaking |
| Loosen validation (widen range, drop pattern) | Non-breaking |
| Add enum value the server now validates against (request) | Breaking for allow-lists only if it *removes* a value; adding is usually safe unless it changes handling |
| Remove enum value from request allow-list | Breaking |

## Response fields

| Change | Verdict |
|---|---|
| Add optional field | Non-breaking (tolerant readers) |
| Add field inside required object | Non-breaking |
| Remove field | Breaking |
| Make response field newly optional / nullable | Breaking (clients expected it present/non-null) |
| Narrow type (string -> number, wider -> subset) | Breaking |
| Widen type in a way clients can't parse | Breaking |
| Add enum value to response | Breaking if clients exhaustively switch; commonly treated as breaking for closed enums, safe for open ones — state the assumption |
| Remove enum value from response | Non-breaking to parsers, but a behavior change |

## Types, formats, structure

- Type change (e.g. `integer` -> `string`): Breaking.
- Format change (`date` -> `date-time`, `int32` -> `int64` narrowing): Breaking
  if it narrows; widening `int32` -> `int64` in a response can break fixed-width
  clients.
- Nullability: adding `nullable: true` to a response field is Breaking; removing
  it (never null now) is safe.
- Arrays: changing item type follows the field rules above; adding `maxItems`
  is Breaking.
- `additionalProperties`: `true` -> `false` is Breaking (previously-accepted
  extra props now rejected).
- `oneOf`/`anyOf`: removing a branch is Breaking; adding a branch to a response
  union is Breaking for exhaustive clients; adding to a request union is safe.
- `required` array: adding a name is Breaking for requests; removing a name is
  Breaking for responses.

## Auth and headers

- Narrowing an OAuth scope or adding a new required scope: Breaking.
- Adding a new required request header: Breaking.
- Removing a response header clients read: Breaking.

## SemVer mapping

- Any breaking change -> MAJOR version bump + deprecation window.
- Additive/optional-only -> MINOR.
- Docs, examples, descriptions -> PATCH.

## Tooling notes

- `oasdiff breaking base revision` exits non-zero on breaking changes — good CI
  gate. `oasdiff changelog` lists everything with severity.
- `openapi-diff` (Atlassian/OpenAPITools) gives an incompatible/compatible flag.
- For pure JSON Schema, there is no universal tool; apply this matrix per
  keyword. JSON Schema draft differences (2019-09 vs 2020-12) can themselves
  change validation semantics — confirm both specs use the same draft.
