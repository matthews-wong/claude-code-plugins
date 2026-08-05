---
name: api-compat
description: Diff an API schema against its baseline and classify breaking vs non-breaking changes.
args: "<baseline-spec> <candidate-spec> (paths or git refs; e.g. openapi.yaml@main openapi.yaml)"
---

Check backward compatibility between two versions of an API contract.

Inputs: a baseline (old/published) spec and a candidate (new/proposed) spec.
These may be OpenAPI (YAML/JSON) or plain JSON Schema. If the user gives git
refs (e.g. `openapi.yaml@main`), retrieve each version with `git show`.

Procedure:

1. Load both specs. If a purpose-built diff tool is available, prefer it and
   report its verdict, but still explain the findings:
   - OpenAPI: `oasdiff breaking <baseline> <candidate>` (best-in-class), or
     `openapi-diff`.
   - Otherwise diff structurally yourself using the rules below.

2. Classify every difference. Load the skill `api-compatibility` and its
   `./reference/compat-rules.md` for the full rule set. Core rules:

   BREAKING (consumers can break):
   - Removed endpoint / path / operation, or removed HTTP method.
   - Removed response field that clients may rely on.
   - New **required** request field or parameter (server now rejects old calls).
   - Type narrowing (string -> enum subset, int -> smaller range, widening to
     stricter format), or a changed type.
   - Removed enum value from a response; added enum value to a request the server
     validates.
   - Tightened validation (new `minLength`, smaller `maximum`, `required` added).
   - Changed default that alters behavior; renamed field (= remove + add).
   - Removed or narrowed auth scope; changed success status code.

   NON-BREAKING (safe/additive):
   - New endpoint or new optional request field.
   - New **optional** response field.
   - New enum value in a response; loosened validation.
   - Newly optional (previously required) request field.
   - Documentation/description/example changes.

3. Produce a report:
   - Verdict line: COMPATIBLE or BREAKING.
   - A table of changes grouped by severity (Breaking / Non-breaking), each with
     the JSON path/endpoint and a one-line why.
   - For each breaking change, a migration suggestion (version bump, deprecation
     window, additive alternative).

4. Recommend a SemVer action: breaking -> major bump + deprecation plan;
   additive-only -> minor; docs-only -> patch.

Be precise about JSON pointers. Do not guess whether a field is consumer-relied;
state the assumption. Never call a change safe without checking the request vs
response direction — required-ness flips meaning between the two.
