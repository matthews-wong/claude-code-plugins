# repo-onboarder

Map an unfamiliar repository fast. A read-only exploring subagent walks the
codebase — stack, entry points, how to build/test/run, conventions, and
gotchas — and the `/onboard` command turns its findings into an `ONBOARDING.md`
at the repo root.

## Components
- `agents/repo-onboarder.md` — read-only subagent (Read, Glob, Grep) that
  explores and returns a structured repo map.
- `commands/onboard.md` — `/onboard` delegates to the subagent and writes
  `ONBOARDING.md`.

## Why a subagent
Exploration reads a lot of files. Doing it in a dedicated subagent keeps that
noise out of the main thread and returns only the distilled map — a clean
context-pull that grounds later work.

## Usage
```
/onboard
```

Author: Matthews Wong — MIT License.
