# verify-app

An end-to-end verification subagent that proves software works instead of assuming it does.

Packages the "**Give Claude a way to verify its work**" practice from Anthropic's *Claude Code best practices* guide: Claude does far better when it can check its own output and iterate against real results — and it should show evidence, not assert success.

## What's inside

- `agents/verify-app.md` — a subagent (tools: Read, Bash, Grep, Glob) that discovers how to run the project, exercises the happy path plus at least one failure case, captures real command output and exit codes, and reports **PASS / FAIL / BLOCKED** with the evidence behind the verdict.
- `reference/playbooks.md` — worked, copy-adaptable verification playbooks per app type: **web app** (build, serve, screenshot, compare to design, check the console), **HTTP API** (start, curl endpoints, assert status + shape, force a failure case), **CLI** (`--help`, valid + invalid input, exit codes), and **background worker/service** (start, enqueue, verify processed, check logs). Each spells out the concrete commands and what PASS looks like.
- `reference/evidence.md` — the "show evidence, not assertions" rule in full, plus the PASS/FAIL report template.
- `commands/verify-app.md` — `/verify-app` delegates to that subagent so verification runs in its own context.

## Usage

```
/verify-app the checkout flow after the payment refactor
```

The subagent will run the build/app, hit the flows, and report what it actually observed. A flow it couldn't run is reported as not-verified — never as a pass.
