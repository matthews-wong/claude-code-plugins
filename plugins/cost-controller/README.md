# cost-controller

Cost and governance plugin for Claude Code. A model-selection policy: route
bulk, mechanical work to cheaper/faster models and reserve frontier models for
judgment and review — optimizing for the lowest total cost to a *correct*
result.

## Components

- **Command `/model-policy`** — classify a task by judgment and volume, get a
  tier recommendation, and see how to switch models per session and per
  subagent.
- **Skill `cost-controller`** — the full policy: tiers, a decision matrix,
  orchestration patterns (frontier plans + reviews, cheap subagents execute),
  how to switch models, and how to avoid the false economy of downgrading too
  far.

## Usage

```
/model-policy migrate 200 files to the new logging API and review the result
```

## The idea

From Boris Cherny's adoption framework: control cost *after* finding
product-market fit. Prove the workflow works on a strong model first, then make
it economical. Model IDs and prices drift between releases, so this plugin talks
in tiers and points to the official Claude Code model list and Anthropic pricing
page for current specifics.

Author: Matthews Wong · License: MIT
