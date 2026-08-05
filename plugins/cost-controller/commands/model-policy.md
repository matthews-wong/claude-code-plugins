---
name: model-policy
description: Recommend a per-task model policy — which model to use for the work at hand — trading cost and speed against judgment quality, and show how to switch models in Claude Code.
args: "<the task or workload you want a model recommendation for>"
---

You are advising on model selection for the following work:

$ARGUMENTS

Apply the cost-controller policy: cheaper/faster models for bulk and mechanical
work, frontier models for judgment and review. Reserve the strongest model for
where its judgment actually changes the outcome.

1. Classify the task on two axes:
   - **Judgment required**: mechanical/deterministic (formatting, renames,
     boilerplate, log scraping, test scaffolding, mass edits) vs. high-judgment
     (architecture, security review, ambiguous debugging, API/interface design,
     tradeoff calls).
   - **Volume / repetition**: one-off vs. run-many-times-or-across-many-files.

2. Recommend a tier, and say why in one line:
   - **Fast/cheap tier (e.g. Haiku-class)** — high-volume mechanical work where
     correctness is easy to verify. Cheapest per token, quickest turnaround.
   - **Balanced tier (e.g. Sonnet-class)** — most everyday coding: solid
     capability at moderate cost; a sensible default for mixed work.
   - **Frontier tier (e.g. Opus-class)** — judgment-heavy work: design, review,
     thorny debugging, anything where a wrong call is expensive to unwind.
   Do not hard-code exact model IDs or prices that drift between releases; name
   the tier and, if the user needs specifics, point to the current Claude Code
   model list and Anthropic pricing page.

3. Suggest an orchestration split when the task is mixed: use a frontier model to
   plan and review, and delegate the bulk execution to a cheaper model via
   subagents. This is the core cost lever — the expensive model makes the
   decisions; cheap models do the volume. Name which parts go to which tier.

4. Show how to switch models in Claude Code:
   - `/model` to change the model for the current session interactively.
   - The `--model` flag when launching Claude Code for a whole session.
   - Per-subagent model selection when delegating (an agent definition's model,
     or the model override when spawning an agent), so bulk lanes run cheap while
     the orchestrator stays frontier.
   State these as the mechanisms; if the user needs exact syntax for their
   version, point them to the Claude Code docs.

5. Frame the tradeoff honestly (per Boris Cherny's adoption framework, cost
   control is the step you take AFTER finding product-market fit — first make it
   work, then make it economical). Note that aggressive downgrading can cost more
   in rework if a cheap model produces work a human or a frontier model must
   redo. The goal is lowest total cost to a correct result, not lowest cost per
   token.

Keep the recommendation concrete and short. Consult the `cost-controller` skill
for the full policy and the decision matrix.
