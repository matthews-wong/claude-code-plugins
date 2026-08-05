---
name: onboard
description: Use when new to an unfamiliar repo and need to get productive fast — explores the codebase with a read-only subagent and writes an ONBOARDING.md covering stack, entry points, build/test/run, conventions, and gotchas.
---

Produce an `ONBOARDING.md` at the repository root that would let a new engineer
(or a fresh agent) become productive quickly.

Delegate the exploration to the **repo-onboarder** subagent — it is read-only
(Glob/Grep/Read) and specialized for mapping a codebase. Ask it to map the
current repository and return its structured summary. Running the exploration in
a subagent keeps the large volume of file reads out of the main conversation and
returns just the distilled map.

When the subagent reports back, write `ONBOARDING.md` with these sections:

1. **Overview** — one paragraph: what this project is and its stack.
2. **Getting started** — prerequisites, install, and the exact build/test/run
   commands (attributed to where they came from).
3. **Project layout** — the organizing principle and the key directories.
4. **Conventions** — formatting, linting, testing, naming, and architecture
   rules actually in use.
5. **Gotchas** — required env vars, external services, setup steps, surprises.
6. **Open questions** — anything the exploration could not confirm.

Rules:
- Only include facts the subagent could verify from the repository. Do not
  fabricate commands, versions, or services. If something is unknown, list it
  under Open questions rather than guessing.
- If an `ONBOARDING.md` already exists, read it first and update it in place
  rather than duplicating content.
- Keep it practical and skimmable — headings, short bullets, real commands in
  fenced code blocks.

After writing the file, give the user a two or three sentence summary of what
you captured and anything notable you found.
