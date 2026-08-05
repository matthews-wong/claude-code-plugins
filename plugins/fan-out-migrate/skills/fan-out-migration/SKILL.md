---
name: fan-out-migration
description: Use when a repetitive, mechanical change must be applied across many files — a bulk migration, codemod, rename, or API/import update spanning a whole codebase. Covers generating a task list to a file and looping a scoped headless `claude -p` per file, testing on a few files before running at scale.
---

# Fan out across files

Some changes are the same edit repeated over dozens or hundreds of files. Doing that in one conversation blows the context and degrades partway through. Instead, fan out: drive one small, scoped, headless Claude run per file, coordinated by a shell loop.

## The workflow

1. **Generate a task list to a file.** Find every target (Glob/Grep) and write the paths to `files.txt`, one per line. The worklist lives on disk, not in context — that's what lets it scale to hundreds of files.

2. **Write a precise per-file prompt.** A single, self-contained instruction for transforming one file, runnable with no conversation history. Ambiguity is multiplied across every file, so state exactly what to change and what to leave alone.

3. **Scope `--allowedTools` tightly.** Give each run only what it needs, e.g. `--allowedTools "Edit,Bash(git commit *)"`. Least privilege per iteration limits the blast radius if the prompt misbehaves.

4. **Test on 2–3 files first.** Point the loop at a tiny `files.txt` of representative files, run it, and inspect the diffs. Iterate on the prompt until it's reliably correct on the sample.

5. **Run at scale, then verify the aggregate.** Expand to the full list and run. Then verify the whole batch — build, tests, `git diff` — because per-file success doesn't prove the whole migration is correct.

## The loop (see `scripts/fan-out.sh`)

The bundled `scripts/fan-out.sh` is a commented POSIX-sh template:

```sh
while IFS= read -r file; do
  claude -p "APPLY <the change> to $file. Do X. Do NOT do Y." \
    --allowedTools "Edit,Bash(git commit *)"
done < files.txt
```

It ships **non-destructive by default**: it prints (dry-runs) each command instead of executing it, so you can eyeball the exact invocations first. You edit the prompt and tool scope, prove it on a sample `files.txt`, then uncomment the live line to run for real.

## Principles

- **Small, uniform, mechanical** changes fan out well; judgment-heavy or interdependent edits don't — do those interactively.
- **Prompt precision matters more here** than anywhere, because errors replicate across every file.
- **Commit per file** (via the scoped `git commit`) so each change is isolated and easy to revert.
- **Always sample before scale.** Never point an unproven prompt at the full list.

See `reference/harness-guide.md` for prompt-design detail, resuming a partial run, parallelism, and post-run verification.
