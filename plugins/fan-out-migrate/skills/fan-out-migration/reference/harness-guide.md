# Fan-out harness guide

Depth behind the `scripts/fan-out.sh` template and the fan-out workflow.

## Designing the per-file prompt

Because the prompt runs once per file with no shared memory, precision compounds:

- **Name the transformation exactly.** "Replace `import X from 'a'` with `import X from 'b'`" beats "update the imports."
- **State the no-ops.** Tell it what NOT to touch, and to make no edits if the file doesn't need the change. This prevents spurious diffs.
- **Make it self-contained.** Include any context a fresh headless run needs — it can't see your earlier conversation.
- **One responsibility per run.** If the migration has two independent parts, consider two passes over the list rather than one overloaded prompt.

## Scoping `--allowedTools`

Grant the minimum:

- `"Edit"` — edit the target file only.
- `"Edit,Bash(git commit *)"` — edit and commit per file (recommended: isolates each change for easy revert).
- Add `Read`/`Grep` only if the transformation genuinely needs to look around.

Tight scope is a safety mechanism: a misfiring prompt can't run arbitrary commands.

## Sample-before-scale, concretely

1. Copy 2–3 representative paths into `files.txt` (include an edge case if the codebase has variety).
2. Run the dry run (`sh fan-out.sh`) and read the printed invocations.
3. Run live (`sh fan-out.sh --live`) on the sample.
4. `git diff` / `git log` — are the changes exactly right? Any over-reach?
5. Fix the prompt and repeat until the sample is clean. Only then expand `files.txt`.

## Resuming a partial run

Because each file is committed separately, a stopped run is easy to resume: regenerate `files.txt` to exclude already-committed files (e.g. diff the worklist against `git log --name-only`) and re-run. Idempotent prompts ("if already migrated, make no edits") make re-running safe.

## Parallelism (optional)

For large lists you can process files concurrently, e.g. with `xargs -P N` feeding paths to a worker. Only do this once the prompt is proven, keep N modest, and avoid it if runs might touch shared files or the same git index simultaneously (per-file commits serialize poorly under high parallelism).

## Verifying the aggregate

Per-file success is necessary, not sufficient. After the full run:

- Build and run the test suite.
- Skim `git diff --stat` for surprising files or unexpectedly large diffs.
- Spot-check a few files by hand.
- If something is wrong broadly, the per-file commits make a targeted `git revert` or reset straightforward.
