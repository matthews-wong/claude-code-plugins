# Store schemas

The unified store lives in ONE directory at the project root:

```
.claude/memory/
├── notes.jsonl       # learnings (episodic + semantic)
└── instincts.jsonl   # promoted, durable rules
```

Both files are **JSON Lines** — one JSON object per line, created on first write. Readers
skip any blank or malformed line, so a partial write can never break the session. The
project directory resolves from `$CLAUDE_PROJECT_DIR`, falling back to the current dir.

## Learning (note) schema — `notes.jsonl`

| Field          | Type            | Description                                                                    |
|----------------|-----------------|--------------------------------------------------------------------------------|
| `id`           | string          | Short unique id (12 hex chars) assigned at write time.                         |
| `text`         | string          | The self-contained lesson. Required and non-empty.                             |
| `folder`       | string          | Project-relative, POSIX-style folder scope (e.g. `src/auth`; `.` = root).      |
| `tags`         | array of string | Optional keywords to aid retrieval (e.g. `["bug","async"]`).                   |
| `ts`           | string          | ISO-8601 timestamp with offset; set at write time and refreshed on merge.      |
| `kind`         | string          | `episodic` (what happened) or `semantic` (a reusable principle). Default `episodic`. |
| `importance`   | number          | Relative weight; default `1.0`. Bumped when near-duplicates merge.             |
| `confidence`   | number          | Trustworthiness, `0.0`–`1.0`; default `0.5`. Rises on corroboration/reuse.     |
| `access_count` | integer         | How many times retrieval surfaced the note; default `0`.                       |
| `last_used`    | string          | ISO-8601 timestamp of the last time retrieval surfaced the note. Optional.     |

### Example line

```json
{"id":"a1b2c3d4e5f6","text":"Token refresh must run before the request retry, not after — retrying first triggers a second 401 and burns the refresh token.","folder":"src/auth","tags":["bug","async","retry"],"ts":"2026-08-07T10:15:00+07:00","kind":"semantic","importance":1.5,"confidence":0.83,"access_count":3,"last_used":"2026-08-07T11:00:00+07:00"}
```

## Instinct (rule) schema — `instincts.jsonl`

| Field        | Type              | Meaning |
|--------------|-------------------|---------|
| `id`         | string            | Stable 12-char hex identifier, assigned once at creation. |
| `rule`       | string            | The learned rule as one concise imperative sentence. |
| `scope`      | string            | `"global"` (applies everywhere) or a project-relative folder path. |
| `tags`       | array of strings  | Short free-form labels. Merged on reinforcement. |
| `confidence` | number (0, 1)     | Derived from `support`: `1 - 0.5 ** support`. |
| `support`    | integer ≥ 1       | Number of times the rule has been observed/reinforced. |
| `created`    | string (ISO 8601) | UTC timestamp of first creation. Never changes. |
| `updated`    | string (ISO 8601) | UTC timestamp of the most recent add/reinforce. |

### Example line

```json
{"confidence": 0.75, "created": "2026-08-08T09:00:00Z", "id": "a1b2c3d4e5f6", "rule": "Always run `make test` before committing.", "scope": "global", "support": 2, "tags": ["testing", "git"], "updated": "2026-08-08T09:30:00Z"}
```

## Portable export envelope

`export` wraps BOTH stores in one envelope so importers can validate what they read:

```json
{
  "kind": "memory-export",
  "version": 1,
  "exported": "2026-08-08T09:30:00Z",
  "notes":     [ /* array of learning records as above */ ],
  "instincts": [ /* array of instinct records as above */ ]
}
```

`import` accepts this envelope. It also accepts a **bare array** of instinct records
(a legacy instincts-only export), treating them as instincts. Learnings merge per folder
(cosine ≥ 0.85 dedup); instincts reinforce per scope (Jaccard ≥ 0.8).

## Backward compatibility

The newer note fields (`kind`, `importance`, `confidence`, `access_count`, `last_used`)
were added after the original format. Older notes may lack them and that is fine — every
reader defaults them (`kind = episodic`, `importance = 1.0`, `confidence = 0.5`,
`access_count = 0`, recency neutral when `ts` is absent).

## Privacy and gitignore

The store is **local to the machine** — it is written under `.claude/memory/` and is never
uploaded anywhere by this plugin. Treat it as working notes, not shared source.

- **Add `.claude/memory/` to your `.gitignore`.** Learnings can contain
  environment-specific details, internal reasoning, or paths you would not want in history.
- **Never store secrets** — no credentials, tokens, or keys. Records are plain text meant
  to be read back verbatim into a future session's context.
- To share curated memory with a team, use `/memory-export` deliberately rather than
  committing the raw store.
