---
name: learn
description: Use when you just solved a tricky bug, hit a non-obvious gotcha, or made a notable decision and want the next agent to inherit that knowledge. Distills the lesson into concise, folder-scoped notes and appends them to the local knowledge store.
---

You are recording durable learnings into the folder-scoped knowledge store so future
sessions start smarter.

Look back over what just happened in this session (the problem, the fix, the decision,
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
- `--confidence` (optional): how trustworthy the lesson is, `0.0`–`1.0` (default `0.5`).
  Pass a higher value (e.g. `0.8`) for a well-verified lesson; leave the default for a hunch.
  Confidence rises automatically as a lesson is corroborated (re-recorded) or reused.

Then append each note by running (once per note):

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/store.py" --text "the lesson" --folder "src/auth" --tags "bug,async"
```

If the user gave the lesson explicitly (an argument to the command), record that instead
of inferring. After storing, briefly confirm what you saved. If nothing genuinely worth
remembering happened, say so and store nothing.
