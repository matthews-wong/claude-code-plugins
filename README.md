# 🤖 Agentic Claude Code Plugins

> A marketplace of **20 Claude Code plugins** for agentic workflows — organized around Boris Cherny's five stages of AI adoption. Install any of them with one command.

![Claude Code](https://img.shields.io/badge/Claude%20Code-plugins-D97757?logo=anthropic&logoColor=white)
![Plugins](https://img.shields.io/badge/plugins-20-6f42c1)
![Agentic Workflows](https://img.shields.io/badge/focus-agentic%20workflows-1f883d)
![License](https://img.shields.io/badge/License-MIT-green)

I spend most of my time these days **building agentic workflows with Claude Code** — turning it from an autocomplete into a fleet of agents that verify their own work, review each other, pull their own context, and run on a schedule. This marketplace is that practice packaged up: 20 small, focused plugins (skills, slash commands, subagents, and hooks) you can drop into your own setup.

## 🚀 Install

```bash
# 1) Add this marketplace (one time)
/plugin marketplace add matthews-wong/claude-code-plugins

# 2) Install any plugin
/plugin install skills-connector@matthews-agentic-plugins
/plugin install code-review-agent@matthews-agentic-plugins
# ...or browse them all
/plugin marketplace list
```

Each plugin is a normal Claude Code plugin: a `.claude-plugin/plugin.json` manifest plus the components it ships (`commands/`, `skills/`, `agents/`, `hooks/`).

## 🧭 Organized by the five stages of AI adoption

The plugin categories map to the maturity model from **Boris Cherny's "Steps to AI adoption with Claude Code"** (Anthropic, July 2026), as summarized by Yash Thakker on [explainX](https://www.explainx.ai/blog/boris-cherny-steps-ai-adoption-claude-code-july-2026). Cherny's framing: teams advance not by *buying more tokens* but by **finding and removing the next bottleneck and layering the right guardrail** at each stage.

| Stage | Cherny's bottleneck → guardrail | Plugins here that help |
| --- | --- | --- |
| **1 → 2 · Assisted → Parallel** | Your attention is the bottleneck → give Claude **end-to-end self-verification** before you review | `verify-before-review`, `code-review-agent`, `security-review-agent`, `test-guardian`, `e2e-verifier` |
| **1 → 2 · Permissions** | Review friction → **auto mode** + pre-approved safe commands | `permission-optimizer`, `auto-mode-setup`, `plan-mode-helper` |
| **2 → 3 · Parallel → Supervised** | Trust & context → **context pull** and reusable skills/standards | `skills-connector`, `claude-md-manager`, `context-puller`, `repo-onboarder` |
| **2 → 4 · Orchestration** | Throughput → **agent-to-agent kickoff, worktree isolation, loops & routines** | `agent-kickoff`, `worktree-isolation`, `loop-runner`, `parallel-lanes`, `routine-scheduler` |
| **3 → 4 · Governance** | Cost & oversight → **model-selection policy, budgets, telemetry** | `cost-controller`, `token-budget-tracker`, `otel-governance` |

> Cherny's honesty test for what to automate at Step 3: *"Is this something an engineer would have done?"* — and his caution that **behavior, not your license SKU, determines your stage.** These plugins are the small, concrete guardrails that make each step-up stick.

## 📦 The 20 plugins

### ✅ Verification & review — *give Claude end-to-end verification before a human sees the output*
| Plugin | What it installs |
| --- | --- |
| [**verify-before-review**](./plugins/verify-before-review) | A Stop hook + `/verify` command that runs tests, lint, and build as a self-verification loop before you review. |
| [**code-review-agent**](./plugins/code-review-agent) | A `code-reviewer` subagent + `/code-review` for automated review of your working diff. |
| [**security-review-agent**](./plugins/security-review-agent) | A `security-reviewer` subagent + `/security-review` that flags common vulnerabilities, severity-ranked. |
| [**test-guardian**](./plugins/test-guardian) | A PostToolUse hook that runs the fast test suite after edits and surfaces failures. |
| [**e2e-verifier**](./plugins/e2e-verifier) | A checklist skill + `/e2e-check` to verify a change end-to-end before handing it off. |

### 🔐 Permissions & guardrails — *reduce review friction safely*
| Plugin | What it installs |
| --- | --- |
| [**permission-optimizer**](./plugins/permission-optimizer) | Analyzes denied tool calls and proposes a **read-only-only** allowlist to cut permission prompts. |
| [**auto-mode-setup**](./plugins/auto-mode-setup) | Configures auto mode and pre-approves a vetted set of safe bash/MCP commands. |
| [**plan-mode-helper**](./plugins/plan-mode-helper) | A plan-first workflow: draft an approach + test strategy, confirm, then execute. |

### 🧠 Context & skills — *ground agents and build a reusable library*
| Plugin | What it installs |
| --- | --- |
| [**skills-connector**](./plugins/skills-connector) | ⭐ Scaffold, list, and wire up Claude Code **skills** — the backbone for an agentic skills library. |
| [**claude-md-manager**](./plugins/claude-md-manager) | Scaffold and lint `CLAUDE.md` standards (and trim derivable bloat). |
| [**context-puller**](./plugins/context-puller) | Gather README/docs/ADRs/history into a grounded working brief before a task. |
| [**repo-onboarder**](./plugins/repo-onboarder) | An exploring subagent that maps a repo and writes an `ONBOARDING.md`. |

### 🚦 Orchestration & loops — *scale beyond one agent*
| Plugin | What it installs |
| --- | --- |
| [**agent-kickoff**](./plugins/agent-kickoff) | Decompose a task and kick off subagents in parallel (agent-to-agent). |
| [**worktree-isolation**](./plugins/worktree-isolation) | Run agents on isolated git worktrees to avoid merge chaos. |
| [**loop-runner**](./plugins/loop-runner) | Turn a repeatable task into a recurring routine via the `/loop` taxonomy. |
| [**parallel-lanes**](./plugins/parallel-lanes) | Fan a big task into independent lanes, then synthesize. |
| [**routine-scheduler**](./plugins/routine-scheduler) | Define scheduled routines (e.g., nightly PR triage, dependency checks). |

### 💰 Cost & governance — *control spend and keep oversight*
| Plugin | What it installs |
| --- | --- |
| [**cost-controller**](./plugins/cost-controller) | A model-selection policy: cheap/fast for bulk work, frontier for judgment. |
| [**token-budget-tracker**](./plugins/token-budget-tracker) | A session hook + `/token-budget` to track usage and trim context. |
| [**otel-governance**](./plugins/otel-governance) | Enable OpenTelemetry export + spend caps for team governance. |

## 🛠️ Repo layout

```
.claude-plugin/
  marketplace.json        # lists all 20 plugins (marketplace: "matthews-agentic-plugins")
plugins/
  <plugin-name>/
    .claude-plugin/plugin.json
    commands/ | skills/ | agents/ | hooks/
    README.md
```

Validate locally before use with `/plugin validate .`.

## 📝 Notes

These are practical, open-source plugins I use and iterate on — starting points to adapt, not turnkey enterprise tooling. Hook scripts are intentionally simple so you can tailor them to your stack. Contributions welcome (see [CONTRIBUTING.md](./CONTRIBUTING.md)).

## 📚 Reference

- Boris Cherny, *Steps to AI adoption with Claude Code* (Anthropic, July 2026) — summarized by Yash Thakker: **[explainx.ai/blog/boris-cherny-steps-ai-adoption-claude-code-july-2026](https://www.explainx.ai/blog/boris-cherny-steps-ai-adoption-claude-code-july-2026)**
- [Claude Code plugin & marketplace docs](https://code.claude.com/docs/en/plugin-marketplaces.md)

## License

MIT © 2026 Matthews Wong

---

_Part of my cloud & AI portfolio — see [github.com/matthews-wong](https://github.com/matthews-wong) · [matthewswong.com](https://matthewswong.com)._
