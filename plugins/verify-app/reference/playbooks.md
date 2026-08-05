# Verification Playbooks

Worked, copy-adaptable playbooks for exercising software for real. Pick the one that
matches the app under test (a repo may need more than one — a web app with an API is
both). Each playbook is: **detect → run the real thing → exercise happy path → exercise
one failure case → what PASS looks like.** Adapt commands to the project's actual
tooling (you learned that from `README`, `package.json`, `Makefile`, etc. — never
invent commands). Every command's output is evidence: capture it per `evidence.md`.

General rules that apply to every playbook:

- **Run the real artifact**, not a mock of it. Build the build, start the server, invoke
  the CLI. A green unit suite is supporting evidence, not a substitute for running it.
- **Time-bound and background long-running processes.** Start servers/workers in the
  background, poll a readiness signal, do the work, then kill them. Never leave a process
  hanging your run.
- **Always do a failure case.** Software that only "works" on the happy path is unverified.
  One deliberate bad input that returns the *right* error is worth more than three happy paths.
- **Capture exit codes.** `echo "exit=$?"` after the command that matters.

---

## Web app (browser UI)

**Detect:** `index.html`, a `dev`/`start`/`build` script in `package.json`, a framework
dep (React, Vue, Svelte, Next, Vite, Astro), or a `public/`+`src/` layout.

**Steps:**

1. **Install & build** — prove it compiles before you prove it runs.
   ```bash
   npm ci        # or: pnpm i / yarn
   npm run build ; echo "exit=$?"
   ```
   PASS signal: exit 0 and a "compiled/built successfully" line; note the output dir.

2. **Start the dev/preview server in the background**, then poll until it answers.
   ```bash
   npm run dev >/tmp/dev.log 2>&1 &   # or: npm run preview
   SERVER_PID=$!
   for i in $(seq 1 30); do
     curl -sf http://localhost:5173 >/dev/null && break
     sleep 1
   done
   ```

3. **Load the page and inspect it.** Best: drive a headless browser to render it, take a
   screenshot, and read the console. If Playwright/Puppeteer is available in the repo, use
   it; otherwise fall back to curling the served HTML and asserting the app root/mount
   point and key text are present.
   ```bash
   # Fallback without a browser driver:
   curl -s http://localhost:5173 | grep -qi '<div id="root"' && echo "mount point present"
   ```
   With a browser driver, script: goto URL → wait for the main content selector →
   `page.screenshot({ path: 'evidence/home.png' })` → collect `console` events.

4. **Compare to the intended design.** Open the screenshot against the design/spec (Figma,
   mockup, the requirement's description). Check the load-bearing things: the primary
   content rendered, layout isn't broken/blank, the key CTA is visible. Note concrete
   diffs, not vibes.

5. **Check the console.** Any uncaught error, failed network request (4xx/5xx for the
   app's own assets/API), or React/hydration warning that breaks function is a FAIL.

6. **Failure case:** load a route that should 404, or submit the main form with invalid
   input — confirm the app shows its error state rather than a blank page or a crash.

7. **Clean up:** `kill $SERVER_PID 2>/dev/null`.

**What PASS looks like:** build exit 0; server answered on its port; screenshot shows the
intended page rendered (attach the path); console clean of functional errors; the failure
case produced the expected error UI.

---

## HTTP API (no UI)

**Detect:** a server entrypoint (`app.py`/`main.go`/`server.js`/`index.ts`), a web
framework dep (Express, FastAPI, Flask, Gin, Spring, Rails), route definitions, or an
OpenAPI/`routes` file. No browser front end.

**Steps:**

1. **Start the server in the background**, capture logs, poll a health/root endpoint.
   ```bash
   npm start >/tmp/api.log 2>&1 &   # or: uvicorn app:app --port 8000, go run ./..., etc.
   API_PID=$!
   for i in $(seq 1 30); do
     curl -sf http://localhost:8000/health >/dev/null 2>&1 && break
     sleep 1
   done
   ```

2. **Curl the key endpoints** — status code AND response shape both matter.
   ```bash
   # -w prints the status; -s silences the progress meter; -o keeps the body.
   curl -s -w '\nHTTP %{http_code}\n' http://localhost:8000/api/items
   curl -s -w '\nHTTP %{http_code}\n' \
        -X POST http://localhost:8000/api/items \
        -H 'Content-Type: application/json' \
        -d '{"name":"widget","qty":3}'
   ```
   Assert: expected status (200/201), and the body has the fields the contract promises
   (`id`, `name`, ...). Pipe through `jq` if available: `... | jq '.id, .name'`.

3. **Failure case — the important half.** Send a request that *should* be rejected and
   confirm it fails *correctly*: right status, useful error body, not a 500 stack trace.
   ```bash
   # Missing required field should be a 4xx, not a 500:
   curl -s -w '\nHTTP %{http_code}\n' \
        -X POST http://localhost:8000/api/items \
        -H 'Content-Type: application/json' -d '{}'
   # Unknown id should be 404:
   curl -s -w '\nHTTP %{http_code}\n' http://localhost:8000/api/items/does-not-exist
   ```
   PASS signal: 400/422 for bad input, 404 for missing resource, and an error message —
   NOT 200 and NOT 500.

4. **Clean up:** `kill $API_PID 2>/dev/null`. Check `/tmp/api.log` for unexpected errors.

**What PASS looks like:** server came up; each key endpoint returned the expected status
and a body with the right shape (quote the actual JSON); the failure case returned the
correct 4xx with a sane error, not a crash.

---

## CLI tool

**Detect:** a `bin` entry in `package.json`, `[project.scripts]`/console_scripts,
`argparse`/`click`/`cobra`/`clap` usage, or a `main` that parses `argv`.

**Steps:**

1. **Build/install so the command is runnable** (or invoke via the project's runner:
   `node ./bin/cli.js`, `python -m pkg`, `go run .`, `./target/debug/tool`).

2. **`--help` works and documents the real interface.**
   ```bash
   mytool --help ; echo "exit=$?"
   ```
   PASS: exit 0, usage text lists the commands/flags the task expects.

3. **Happy path — valid input, assert exit code AND output.**
   ```bash
   mytool convert input.txt --format json ; echo "exit=$?"
   # Or with a pipeline / on-disk artifact:
   mytool build --out dist/ && test -f dist/result.json && echo "artifact present"
   ```
   PASS: exit 0, expected content on stdout (grep for the load-bearing token), and any
   promised output file exists with sane content.

4. **Failure case — invalid input must fail loudly, not silently.**
   ```bash
   mytool convert /no/such/file    ; echo "exit=$?"   # expect NON-zero
   mytool --nonsense-flag          ; echo "exit=$?"   # expect NON-zero + usage hint
   ```
   PASS: non-zero exit code and a clear error message on stderr. A tool that returns exit
   0 on bad input is a FAIL.

**What PASS looks like:** `--help` exits 0 with real usage; valid input gives exit 0 and
the expected output/artifact; invalid input gives a non-zero exit and a readable error.
Quote the commands and their exit codes.

---

## Background worker / service

**Detect:** a queue/broker dep (Celery, BullMQ, Sidekiq, RQ, Kafka/RabbitMQ consumer), a
`worker`/`consumer` process, cron/scheduler code, or a long-running loop that isn't an
HTTP server.

**Steps:**

1. **Start the worker (and any broker it needs) in the background**, capture logs.
   ```bash
   # e.g. bring up dependencies, then the worker:
   docker compose up -d redis          # or the broker the project uses
   npm run worker >/tmp/worker.log 2>&1 &   # or: celery -A app worker, sidekiq, etc.
   WORKER_PID=$!
   sleep 2   # let it connect; confirm via log, not just a guess
   grep -qi 'ready\|connected\|listening' /tmp/worker.log && echo "worker up"
   ```

2. **Enqueue a real job** the way the app does (a small script, a CLI enqueue command, or
   an API call that schedules work).
   ```bash
   node ./scripts/enqueue.js '{"task":"resize","id":42}'   # or the project's enqueue path
   ```

3. **Verify it was processed** — the whole point. Prove the effect, not just that the
   worker is alive: the log shows the job handled, the DB row/output file/queue count
   changed, or a downstream side effect happened.
   ```bash
   for i in $(seq 1 20); do
     grep -q 'job 42 done' /tmp/worker.log && { echo "processed"; break; }
     sleep 1
   done
   # And confirm the side effect, e.g.:
   test -f output/42.jpg && echo "artifact written"
   ```

4. **Check the logs** for errors, retries, or dead-letter/failed entries during the run.

5. **Failure case:** enqueue a job that should fail (bad payload) and confirm the worker
   handles it as designed — moves it to a failed/retry queue and logs it, rather than
   crashing the whole worker.

6. **Clean up:** `kill $WORKER_PID 2>/dev/null` and tear down any `docker compose` deps.

**What PASS looks like:** worker started and connected (quote the log line); the enqueued
job was processed and its side effect is observable (quote the log line + show the
artifact/row); the bad job failed safely without taking the worker down.
