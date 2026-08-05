---
name: e2e-check
description: Run an end-to-end verification of the current change — reproduce the happy path plus one edge case, capture evidence, and give a ready / not-ready verdict.
args:
  - name: focus
    description: Optional description of the specific change or feature to verify end-to-end (e.g. "the new /login endpoint"). Defaults to the current working changes.
---

Perform an end-to-end verification of the current change before it goes to a human.

Apply the **e2e-verification** skill and work through its checklist in order:

1. Establish what "working" means for this change. If a `focus` was given ("$1"),
   verify that specifically; otherwise infer the change from the current working
   diff (`git diff`) and recent edits.
2. Reproduce the **happy path** through the real running system — build/start it as
   needed and exercise the actual entry point (CLI, endpoint, UI flow, or public
   API) with realistic input.
3. Exercise at least **one edge case** most likely to break (empty/malformed input,
   a boundary value, or an error path).
4. Re-run the existing test suite to guard against regressions.
5. **Capture concrete evidence** — the commands you ran and their actual output,
   status codes, log lines, or state — not assertions that it "should" work.
6. Give a checklist-style report and a clear **Ready / Not-ready** verdict.

If you cannot actually run the system in this environment, do not fake success:
provide the exact reproduction steps and expected results for a human to run, and
mark those items as "could-not-run." Do not modify code as part of this check
unless I explicitly ask.
