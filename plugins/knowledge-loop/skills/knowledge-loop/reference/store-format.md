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

| Field    | Type            | Description                                                              |
|----------|-----------------|--------------------------------------------------------------------------|
| `id`     | string          | Short unique id (12 hex chars) assigned at write time.                   |
| `text`   | string          | The self-contained lesson. Required and non-empty.                       |
| `folder` | string          | Project-relative, POSIX-style folder scope (e.g. `src/auth`; `.` = root).|
| `tags`   | array of string | Optional keywords to aid retrieval (e.g. `["bug","async"]`).             |
| `ts`     | string          | ISO-8601 timestamp with offset, assigned at write time.                  |

### Example line

```json
{"id":"a1b2c3d4e5f6","text":"Token refresh must run before the request retry, not after — retrying first triggers a second 401 and burns the refresh token.","folder":"src/auth","tags":["bug","async","retry"],"ts":"2026-08-07T10:15:00+07:00"}
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
