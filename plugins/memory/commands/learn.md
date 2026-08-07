---
name: learn
description: Use when you just solved a tricky bug, hit a non-obvious gotcha, or made a notable decision and want the next agent to inherit that knowledge. Distills the lesson into concise, folder-scoped learnings and appends them to the local memory store.
---

You are recording durable learnings into the folder-scoped memory store so future
sessions start smarter. (`learn` is an alias of `remember`.)

Look back over what just happened this session (the problem, the fix, the decision,
the surprise) and distill it into **1 to 3 concise, self-contained notes**. Each note
must stand on its own months from now with no session context.

Guidance for a good note:
- **One durable insight per note.** Split unrelated lessons into separate notes.
- **Name the folder and the problem.** Say where it applies and what triggered it, then
  the lesson and the fix or decision. Prefer the specific over the generic.
- **Keep it short** — one to three sentences. No transcript, no code dumps, no secrets.
- Skip the trivial and the obvious; capture only what would save a future agent time.

For each note, choose:
- `--text`: the self-contained lesson.
- `--folder`: the project-relative folder the lesson is about (e.g. `src/auth`). Default
  to the folder you were working in. Use `.` for repo-wide lessons.
- `--tags`: a few comma-separated keywords (e.g. `bug,async,retry`) to aid retrieval.
- `--kind` (optional): `semantic` for a reusable principle; default `episodic`.
- `--confidence` (optional): `0.0`–`1.0` (default `0.5`); higher for a well-verified lesson.

Then append each note by running (once per note):

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py learn --text "the lesson" --folder "src/auth" --tags "bug,async"
```

If the user gave the lesson explicitly, record that instead of inferring. After storing,
briefly confirm what you saved. If nothing genuinely worth remembering happened, say so
and store nothing.
