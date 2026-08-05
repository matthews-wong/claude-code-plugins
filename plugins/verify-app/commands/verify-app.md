---
name: verify-app
description: Use when you want to confirm the current change actually works end to end — "verify the app", "prove it works", "run the happy path", "did the build pass", before marking a task done. Delegates to the verify-app subagent, which runs the app/build, exercises real flows, and returns PASS/FAIL with captured evidence.
---

Verify that the software works right now, end to end, with evidence — not assertions.

Delegate this to the **verify-app** subagent (via the Agent/Task tool) so verification runs in its own context and reports back cleanly. Pass it:

- What was just built or changed (the diff, the feature, the fix under test).
- The specific flows that matter — at minimum the happy path, plus at least one failure case (bad input, missing resource, auth boundary) the requirements call out.
- Any run hints you already know (start command, test command, base URL, credentials for a local/dev environment).

The subagent ships with worked playbooks it will follow — `reference/playbooks.md` (web app, HTTP API, CLI, background worker) and `reference/evidence.md` (evidence rules + report template). It runs the real thing, exercises the happy path plus a failure case, and reports only what it captured.

$ARGUMENTS

Require the subagent to come back with: the exact commands it ran and where it found them, each flow marked PASS/FAIL with expected-vs-observed output, the load-bearing evidence quoted from real output, and an overall verdict. If it reports FAIL or BLOCKED, surface the error output — do not paper over it. Do not accept "it should work"; only accept demonstrated results.
