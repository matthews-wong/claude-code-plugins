---
name: api-compatibility
description: >
  Use when evaluating whether an API change is backward compatible — diffing
  OpenAPI/Swagger or JSON Schema, deciding breaking vs non-breaking, or picking
  a SemVer bump for an API. Triggers: "breaking change", "backward compatible",
  "API compat", "OpenAPI diff", "schema diff", "will this break clients",
  "oasdiff", "deprecate endpoint", "version bump for API".
---

# API Compatibility

Decide whether a contract change can break existing consumers. The golden rule:
**a change is safe only if every existing valid client request still succeeds and
every existing client can still parse the response.**

## Direction is everything

Required-ness inverts between request and response:

- **Request**: making a field *required* or *adding* a validated constraint is
  BREAKING (old callers omitting it now fail). Making a field *optional* is safe.
- **Response**: *removing* a field or *narrowing* its type is BREAKING (clients
  parsing it break). *Adding* an optional field is safe (tolerant readers).

## Fast classification

BREAKING: removed endpoint/method/field; new required request field; type change
or narrowing; tightened validation; removed response enum value; auth scope
narrowed; changed status code; renamed field.

NON-BREAKING: new endpoint; new optional request field; new optional response
field; loosened validation; previously-required request field made optional;
new response enum value; docs/examples.

The full matrix (with edge cases like `oneOf`/`anyOf`, nullability, arrays,
`additionalProperties`, and format changes) is in
`./reference/compat-rules.md`.

## Preferred tooling

- OpenAPI: `oasdiff breaking base.yaml revision.yaml` — purpose-built, exit code
  signals breaking changes; ideal for CI. Fall back to `openapi-diff`.
- Trust the tool's verdict but still explain each finding in plain terms and add
  a migration path — a raw diff is not guidance.

## Managing an unavoidable break

1. Prefer additive evolution over mutation (add v2 field, keep v1).
2. If you must break: bump the major version, keep the old version running,
   announce a deprecation window, and add `Deprecation`/`Sunset` headers.
3. Never silently reuse a field name with new semantics — that is a hidden break.

## Guardrails

- Do not declare "safe" without checking request vs response direction.
- Whether a response field is consumer-relied is an assumption — state it; when
  unsure, treat removal as breaking.
- SemVer: breaking = major, additive = minor, docs = patch.
