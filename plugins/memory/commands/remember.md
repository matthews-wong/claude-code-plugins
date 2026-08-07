---
name: remember
description: Use when you solved a tricky bug, hit a non-obvious gotcha, worked around a quirk, or made a design decision worth keeping — record it as a concise, folder-scoped learning the next agent will inherit.
---

You are recording a durable learning into the folder-scoped memory store so future
sessions start smarter.

Distill what just happened into **1 to 3 concise, self-contained notes**. Each note
must stand on its own months from now with no session context.

Guidance for a good note:
- **One durable insight per note.** Split unrelated lessons into separate notes.
- **Name the folder and the problem**, then the lesson and the fix or decision.
- **Keep it short** — one to three sentences. No transcript, no code dumps, no secrets.
- Skip the trivial; capture only what would save a future agent time.

For each note choose:
- `--text`: the self-contained lesson.
- `--folder`: the project-relative folder it is about (e.g. `src/auth`); `.` for repo-wide.
- `--tags`: a few comma-separated keywords to aid retrieval.
- `--kind` (optional): `semantic` for a reusable principle, else `episodic` (default).
- `--confidence` (optional): `0.0`–`1.0` (default `0.5`); pass higher for a verified lesson.

Then run (once per note):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py remember --text "the lesson" --folder "src/auth" --tags "bug,async"
```

Near-duplicates in the same folder are merged automatically (importance and confidence
rise) instead of cluttering the store. After storing, briefly confirm what you saved.
