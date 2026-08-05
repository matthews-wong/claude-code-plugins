# fan-out-migrate

Apply a repetitive change across many files by fanning out one scoped, headless Claude run per file — instead of doing the whole sweep in a single conversation.

Packages the "**Fan out across files**" practice from Anthropic's *Claude Code best practices* guide.

## What's inside

- `commands/fan-out.md` — `/fan-out` walks the workflow: generate a task list to `files.txt`, write a precise per-file prompt, scope `--allowedTools`, test on 2–3 files, then run at scale and verify.
- `skills/fan-out-migration/` — the workflow, prompt-design tips, and safety notes, with `reference/harness-guide.md` for depth.
- `scripts/fan-out.sh` — a commented POSIX-sh **template** loop that reads `files.txt` and runs `claude -p "…" --allowedTools "Edit,Bash(git commit *)"` per file. **Non-destructive by default** (dry-runs/prints the commands); enable the live run with `--live` once the prompt is proven.

## Usage

```
/fan-out migrate every file from the old logger API to the new one
```

Then, at the shell:

```sh
sh scripts/fan-out.sh          # dry run — prints commands, changes nothing
sh scripts/fan-out.sh --live   # run for real once the prompt is proven
```

## Guardrails

Test on 2–3 files before running at scale; scope `--allowedTools` to the minimum; commit per file so each change is isolated and revertible; and verify the whole batch (build/tests/`git diff`) after — per-file success doesn't guarantee the aggregate is correct.
