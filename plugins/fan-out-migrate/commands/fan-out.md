---
name: fan-out
description: Use for a repetitive change that spans many files — a mechanical migration, codemod, rename, API/import update, or lint fix applied "across the codebase", "to every file", "in bulk". Generates a task list to a file, then loops a scoped headless `claude -p` per file, testing on 2–3 first before running at scale.
---

Apply a repetitive, largely mechanical change across many files by fanning out one scoped Claude invocation per file, rather than trying to do the whole sweep in a single conversation.

The change to fan out: $ARGUMENTS

Follow the guide's steps:

1. **Generate the task list to a file.** Identify every file that needs the change (Glob/Grep for the pattern) and write the paths — one per line — to `files.txt`. Keeping the worklist in a file, not in context, is what makes this scale.

2. **Write a precise per-file prompt.** One clear instruction describing the exact transformation to apply to a single file, self-contained enough to run headlessly with no conversation history. Ambiguity multiplies across every file, so be specific about what changes and what must NOT.

3. **Scope the tools tightly.** Each headless run gets only the tools it needs via `--allowedTools` — typically `"Edit,Bash(git commit *)"` so a run can edit its file and commit, and nothing else. Least privilege per iteration.

4. **Test on 2–3 files first.** Run the loop against a short `files.txt` of a few representative files. Inspect the diffs. Only once the prompt reliably produces the right change do you run it across the full list.

5. **Run at scale, then verify.** Expand `files.txt` to the full set and let the loop run. Afterward, verify the whole batch — build/tests/`git diff` — because per-file success doesn't guarantee the aggregate is correct.

Use the bundled template at `scripts/fan-out.sh` as the loop harness — it reads `files.txt` and runs `claude -p` per file with scoped `--allowedTools`. It is **non-destructive by default** (prints the commands as a dry run); the user uncomments the live invocation once the prompt is proven on the sample. Consult the **fan-out-migration** skill for the full workflow, prompt-design tips, and safety notes.
