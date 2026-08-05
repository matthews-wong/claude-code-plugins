---
name: context-pull
description: Use before starting a non-trivial coding task to gather the relevant repository context (README, docs, ADRs, related modules, recent git history) and distill it into a short working brief so the agent starts grounded instead of guessing. Triggers on "pull context", "get me up to speed", "brief before I start", "gather context".
---

# Context Pull

The goal is to spend a small, bounded amount of effort up front so that the
actual work is done with accurate context instead of assumptions. This mirrors
Cherny's Step 2 (pull the right context in) feeding Step 3 (act on it).

## Method

### 1. Read the map before the territory
- Root `README.md` — purpose, stack, how to build/run/test.
- `CLAUDE.md` (root and any nested) — project-specific rules that override defaults.
- `docs/` — architecture, design notes, runbooks.
- ADRs — look in `docs/adr/`, `.harness/adrs/`, or `adr/`. These record *why*
  hard-to-reverse decisions were made; honor them.

### 2. Narrow to the task's blast radius
- Use glob to find candidate files by name (e.g. the feature/domain keyword).
- Use grep to find where a symbol, route, or config key is defined and used.
- Read the handful of files that are clearly central. Skim the periphery — you
  need enough to act correctly, not a full audit.

### 3. Pull recent history for signal
- `git log --oneline -20` for overall momentum.
- `git log --oneline -10 -- <path>` for the specific area.
- Recent churn often points at the code you are about to touch and at bugs.

### 4. Capture conventions and gotchas
Note naming, layering, error-handling, and testing patterns actually used in the
files you read — match the code over any external preference.

## Output: the Working Brief

Produce a single concise brief (aim for one page):

- **Goal** — the task restated in repository terms.
- **Relevant files** — path + one-line role each.
- **How it fits together** — control/data flow in a short paragraph.
- **Conventions to honor** — observed style/architecture/testing rules.
- **Recent activity** — notable recent commits in the area.
- **Open questions / risks** — ambiguities and likely traps.

## Bounds and follow-through
- Time-box the gather. If you have read ~5-10 files and the picture is clear,
  stop and write the brief.
- Do not begin implementation while gathering — separate the phases so the brief
  stays honest.
- Once confirmed accurate, offer to persist the stable parts (conventions,
  architecture summary) into `CLAUDE.md` so future sessions start grounded.
