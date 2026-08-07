# Instinct record schema

Instincts are stored in `.claude/instincts/instincts.jsonl` (relative to the
project directory). The store is JSON Lines: one JSON object per line, created
on first write. Resolution of the project directory prefers
`$CLAUDE_PROJECT_DIR`, falling back to the current working directory.

## Fields

| field        | type              | meaning |
|--------------|-------------------|---------|
| `id`         | string            | Stable 12-char hex identifier, assigned once at creation. |
| `rule`       | string            | The learned rule as one concise imperative sentence. |
| `scope`      | string            | `"global"` (applies everywhere) or a folder path the rule is scoped to. |
| `tags`       | array of strings  | Short free-form labels (e.g. `testing`, `git`). Merged on reinforcement. |
| `confidence` | number (0, 1)     | Derived from `support`: `1 - 0.5 ** support`. |
| `support`    | integer >= 1      | Number of times the rule has been observed/reinforced. |
| `created`    | string (ISO 8601) | UTC timestamp of first creation. Never changes. |
| `updated`    | string (ISO 8601) | UTC timestamp of the most recent add/reinforce. |

## Example line

```json
{"confidence": 0.75, "created": "2026-08-08T09:00:00Z", "id": "a1b2c3d4e5f6", "rule": "Always run `make test` before committing.", "scope": "global", "support": 2, "tags": ["testing", "git"], "updated": "2026-08-08T09:30:00Z"}
```

## Portable export format

`export` wraps the records in an envelope so importers can validate what they
are reading:

```json
{
  "kind": "instincts-export",
  "version": 1,
  "exported": "2026-08-08T09:30:00Z",
  "instincts": [ /* array of instinct records as above */ ]
}
```

`import` accepts either this envelope or a bare array of records, and merges
each record using the same similarity-based dedup/reinforce rule as `add`.
