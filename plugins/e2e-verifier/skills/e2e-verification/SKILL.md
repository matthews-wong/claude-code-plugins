---
name: e2e-verification
description: Use when a code change needs end-to-end verification before handing it to a human — reproduce the change through the real running system, confirm the happy path plus at least one edge case, capture concrete evidence, and only then declare it ready.
---

# End-to-end verification

Unit tests prove units; this skill proves the **whole change actually works** when
exercised through the running system. Do not declare a change "done" on the basis of
reading the diff or passing unit tests alone. Follow this checklist in order and
report against it explicitly.

## 0. Establish what "working" means

- Restate the change's intended user-visible behavior in one sentence.
- Identify the entry point that exercises it end-to-end: a CLI command, an HTTP
  endpoint, a UI flow, a script, or a function called through its public API.
- Note the expected observable outcome (output, status code, DB row, file, log line).

## 1. Reproduce the happy path

- Bring up whatever the change needs (build, start the server/app, seed data).
- Exercise the real entry point with a realistic, valid input.
- Confirm the observable outcome matches the intended behavior.
- If you cannot run it in this environment, say so plainly and provide the exact
  commands a human must run, with expected output — do not claim success you did not
  observe.

## 2. Verify at least one edge case

Pick the edge case most likely to break, and exercise it too. Choose from:

- Empty / missing / malformed input.
- Boundary value (zero, max, negative, very large).
- Error path (invalid auth, not-found, downstream failure).
- Concurrency or repeated invocation, if relevant.

Confirm the system handles it correctly (graceful error, correct validation
message, no crash, no corrupted state).

## 3. Guard against regressions

- Re-run the project's existing test suite and confirm it still passes.
- Sanity-check that closely related, unchanged behavior still works.

## 4. Capture evidence

For each check above, record concrete proof, not a claim:

- The exact command(s) run and the relevant output (trimmed).
- Status codes, response bodies, log lines, screenshots, or DB state as applicable.
- The before/after difference where it clarifies the effect.

## 5. Verdict and hand-off

Produce a short report:

- A checklist showing each item as **verified / not verified / could-not-run**.
- The evidence for the happy path and the edge case.
- Any residual risk or untested area, stated honestly.
- A clear verdict: **"Ready for human review"** only if the happy path and at least
  one edge case were actually verified with evidence; otherwise **"Not ready"** with
  exactly what remains.

Only hand a change to a human once this checklist is genuinely satisfied. Honesty
about what you could not verify is more valuable than an optimistic "it works."
