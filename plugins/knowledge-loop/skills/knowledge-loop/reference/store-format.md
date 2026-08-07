# Store format

The knowledge store is a single append-only file at the project root:

```
.claude/knowledge/notes.jsonl
```

It is **JSON Lines** — one JSON object per line. Each line is one learning note.
`store.py` creates the directory and file on first write and appends one line per note.
`retrieve.py` reads the file and silently skips any blank or malformed line, so a partial
write can never break retrieval.

## Note schema

| Field          | Type            | Description                                                                    |
|----------------|-----------------|--------------------------------------------------------------------------------|
| `id`           | string          | Short unique id (12 hex chars) assigned at write time.                         |
| `text`         | string          | The self-contained lesson. Required and non-empty.                             |
| `folder`       | string          | Project-relative, POSIX-style folder scope (e.g. `src/auth`; `.` = root).      |
| `tags`         | array of string | Optional keywords to aid retrieval (e.g. `["bug","async"]`).                   |
| `ts`           | string          | ISO-8601 timestamp with offset; set at write time and refreshed on merge.      |
| `kind`         | string          | `episodic` (what happened) or `semantic` (a reusable principle). Default `episodic`. |
| `importance`   | number          | Relative weight; default `1.0`. Bumped when near-duplicates merge.             |
| `access_count` | integer         | How many times the note has been surfaced by retrieval; default `0`.           |
| `last_used`    | string          | ISO-8601 timestamp of the last time retrieval surfaced the note. Optional.     |

### Backward compatibility

The last four fields (`kind`, `importance`, `access_count`, `last_used`) were added after
the original format. **Older notes may lack them** and that is fine — every reader defaults
them (`kind = episodic`, `importance = 1.0`, `access_count = 0`, recency neutral when `ts`
is absent). An existing store keeps working unchanged; notes gain the fields the next time
they are merged or their access is bumped.

### Example line

```json
{"id":"a1b2c3d4e5f6","text":"Token refresh must run before the request retry, not after — retrying first triggers a second 401 and burns the refresh token.","folder":"src/auth","tags":["bug","async","retry"],"ts":"2026-08-07T10:15:00+07:00","kind":"semantic","importance":1.5,"access_count":3,"last_used":"2026-08-07T11:00:00+07:00"}
```

## Privacy and gitignore

The store is **local to the machine** — it is written under `.claude/knowledge/` and is
never uploaded anywhere by this plugin. Treat it as working notes, not shared source.

- **Add `.claude/knowledge/` to your `.gitignore`.** Learnings can contain
  environment-specific details, internal reasoning, or paths you would not want in the
  repo history.
- **Never store secrets** — no credentials, tokens, or keys. Notes are plain text meant to
  be read back verbatim into a future session's context.
- If you *do* want to share curated learnings with a team, promote them deliberately into
  committed docs rather than committing the raw store.
