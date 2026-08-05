---
name: plan
description: Produce a concise implementation plan (files, approach, risks, tests) and get confirmation before making any edits, then execute.
args: "<task description>"
---

The user wants to work on: $ARGUMENTS

Do not edit any files yet. First investigate, then plan, then wait for confirmation.

## Step 1 — Investigate

Read the relevant code before proposing anything. Identify the files involved, the current
behavior, existing conventions, and the callers or tests that would be affected. Ask a
clarifying question only if a genuine ambiguity blocks planning — otherwise state your
assumptions in the plan.

## Step 2 — Present a concise plan

Keep it tight and skimmable. Cover exactly these sections:

- **Goal** — one sentence restating what we're changing and why.
- **Files to change** — each path with a one-line note on what changes there.
- **Approach** — the key steps in order; call out any design decision and the alternative
  you rejected.
- **Risks** — what could break, edge cases, and anything irreversible or wide-reaching.
- **Test strategy** — how the change will be verified (which tests to add/run, manual
  checks). A bug fix should include a test that fails before and passes after.

Prefer the smallest change that satisfies the requirement. Flag it if the task is larger
than it first appears or should be split.

## Step 3 — Get confirmation

Ask the user to confirm or adjust the plan. Do not begin editing until they approve. If
they request changes, revise the plan and confirm again.

## Step 4 — Execute

Once approved, implement the plan as agreed. If reality diverges from the plan mid-way
(a risk materializes, an assumption proves wrong), pause and surface it rather than
silently improvising. Finish by running the test strategy and reporting results.
