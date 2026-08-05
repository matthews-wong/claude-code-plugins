---
description: A model-selection cost policy for Claude Code — route bulk, mechanical work to cheaper/faster models and reserve frontier models for judgment and review. Covers the cost/quality tradeoff, a decision matrix, how to switch models per task and per subagent, and orchestration patterns that minimize total cost to a correct result. Use when deciding which model to run or how to control spend.
---

# Cost Controller

The core idea: **match the model to the marginal value of its judgment.** Frontier
models are worth their cost where a better decision changes the outcome. For
high-volume mechanical work whose correctness is easy to check, a cheaper, faster
model gets you the same result for a fraction of the cost.

This mirrors Boris Cherny's adoption framing: controlling cost is a step you take
*after* finding product-market fit with a workflow. First prove the workflow
produces value with the strongest model; then optimize its economics. Optimizing
cost before the workflow works is premature.

## The tiers

Claude offers a spectrum of models trading capability against cost and latency.
Rather than pin exact model IDs (they change across releases), think in tiers —
and check the current Claude Code model list and Anthropic pricing page for
today's specifics:

- **Fast / cheap tier** (Haiku-class): cheapest per token, lowest latency. Best
  for high-volume, mechanical, easily-verified work.
- **Balanced tier** (Sonnet-class): strong capability at moderate cost. A sound
  default for most everyday coding.
- **Frontier tier** (Opus-class): deepest reasoning; highest cost. Reserve for
  judgment-heavy work where a wrong call is expensive.

## Decision matrix

| Work type | Examples | Tier |
|---|---|---|
| Mechanical, high-volume | mass renames, formatting, boilerplate, log scraping, test scaffolding, mechanical migrations | Fast / cheap |
| Everyday coding | feature work, ordinary bug fixes, refactors, writing tests | Balanced |
| High-judgment | architecture, security review, ambiguous debugging, interface/API design, tradeoff calls, final review of critical changes | Frontier |

Two quick heuristics:
- **Is correctness cheap to verify?** If yes (tests, a diff you can eyeball),
  lean cheaper. If a subtle wrong answer slips through expensively, lean
  frontier.
- **How many times will this run?** One-off high-stakes -> frontier. Runs across
  hundreds of files -> cheap, because the per-call savings compound.

## Orchestration is the biggest lever

The largest savings come not from picking one model but from *splitting* work:

- Let a **frontier orchestrator** plan the work and review the result — the
  decisions that need judgment.
- **Delegate bulk execution to cheaper subagents.** The expensive model decides;
  cheap models do the volume. For example, a frontier agent designs a migration
  and reviews the final diff, while Haiku-class subagents apply the mechanical
  change across 200 files in parallel lanes.

This keeps frontier tokens on the small, high-value surface and pushes the large,
low-value surface to cheap tokens.

## How to switch models in Claude Code

- **`/model`** — change the model for the current interactive session.
- **`--model <name>`** at launch — set the model for a whole session.
- **Per-subagent model** — an agent definition can specify its own model, and
  spawning an agent can override the model. This is what lets an orchestrator on
  a frontier model dispatch bulk lanes on a cheaper one.
- **Settings/env** — a default model can be configured for the environment.

Treat the above as the mechanisms; for exact syntax and available names in your
version, consult the Claude Code documentation rather than assuming flags.

## Total cost, not token price

Optimize for the **lowest total cost to a correct result**, not the lowest price
per token. Downgrading too aggressively is a false economy when a cheap model
produces work a human or a frontier model must redo — the rework, review time,
and context re-loading can exceed what the stronger model would have cost
outright. Signs you downgraded too far: repeated correction loops, a cheap
agent thrashing on an ambiguous task, or output that fails review. When you see
them, move that task up a tier.

## A workable default policy

1. Start a new, unproven workflow on a strong model until it reliably produces
   value.
2. Once it works, classify its steps: keep judgment/review on frontier, move the
   mechanical bulk to cheaper tiers.
3. Where volume is high, orchestrate: frontier plans + reviews, cheap subagents
   execute.
4. Watch for rework as the signal that you cut too deep, and re-tier.
