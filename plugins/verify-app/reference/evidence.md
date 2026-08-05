# Evidence, Not Assertions

The one rule this subagent exists to enforce: **a verdict is only as good as the captured
output behind it.** "The build passes" is a claim. "I ran `npm run build`, exit code 0,
last line `compiled successfully in 4.2s`" is evidence. If you cannot produce the output
that demonstrates a result, that result is **not** a PASS — it is FAIL or BLOCKED.

## What counts as evidence

Evidence is something you *captured from running the real thing*, quoted verbatim, that a
skeptical reader could check. In rough order of strength:

- **The exact command + its exit code + the load-bearing lines of its output.** The
  minimum unit of evidence. Always include the exit code for the command that decides
  PASS/FAIL (`echo "exit=$?"`).
- **An HTTP status line and response body** for an endpoint you actually hit
  (`curl -w 'HTTP %{http_code}'`), with the JSON quoted.
- **A test-run summary** from the real suite: `N passed, M failed`, plus the failing
  output if any. (Supporting evidence — not a replacement for running the app.)
- **A screenshot** for a UI, saved to a path, described in one line ("home page rendered,
  nav + hero + CTA visible"). Reference the path in the report.
- **A log line proving a side effect** — the worker line showing a job processed, the row
  count that changed, the file that got written.

## What is NOT evidence

- "It should work" / "presumably" / "this looks correct." If you write these, you have not
  verified — go run it.
- A passing unit test used to claim the *running app* works. Different thing.
- Reasoning about the code instead of executing it.
- Output you didn't actually capture (paraphrased or remembered results).

## Capturing it cleanly

- Redirect long output to a file and quote the decisive slice:
  `cmd > /tmp/out.log 2>&1; echo "exit=$?"; tail -n 20 /tmp/out.log`.
- Force status codes to the surface: `curl -s -w '\nHTTP %{http_code}\n' URL`.
- Save UI screenshots under an `evidence/` path and cite the path.
- Quote **real** lines. Trim to what's load-bearing; don't paste 500 lines of a build log —
  paste the 10 that prove the outcome.

## PASS / FAIL report template

Fill every field. An empty "Not verified" section is fine; a missing one is not — never
silently drop a flow you couldn't run.

```
VERDICT: PASS | FAIL | BLOCKED

How I ran it:
  <exact commands, and where each came from — README line, package.json script, etc.>

Flows exercised:
  1. <flow name — e.g. "Happy path: create item via POST /api/items"> — PASS/FAIL
     ran:      <the exact command>
     expected: <what a pass means>
     observed: <actual output / exit code / HTTP status, quoted verbatim>
  2. <failure case — e.g. "POST with missing field returns 422"> — PASS/FAIL
     ran:      <command>
     expected: <e.g. HTTP 422 + error body, not 500>
     observed: <quoted output>

Evidence:
  <the load-bearing lines of real output that prove the verdict — build result,
   HTTP status + body, test summary, screenshot path, worker log line>

Not verified:
  <flows you could not exercise and why — a blocked flow is never a silent PASS>
```

**Verdict discipline:**

- **PASS** — every flow you set out to check ran and produced the expected observed output.
- **FAIL** — at least one flow produced the wrong result; quote the wrong output.
- **BLOCKED** — you could not run the thing (won't build/start, missing dep or secret).
  Report the blocking error output and stop; don't guess past it.
