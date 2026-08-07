# 🤖 Agentic Claude Code Plugins

> A marketplace of **60 Claude Code plugins** for agentic workflows and enterprise engineering — organized around Boris Cherny's five stages of AI adoption, plus security, compliance, quality, and plugins modeled on his own workflow. Install any of them with one command.

![Claude Code](https://img.shields.io/badge/Claude%20Code-plugins-D97757?logo=anthropic&logoColor=white)
![Plugins](https://img.shields.io/badge/plugins-60-6f42c1)
![Agentic Workflows](https://img.shields.io/badge/focus-agentic%20workflows-1f883d)
![Enterprise Ready](https://img.shields.io/badge/enterprise-ready-0A66C2)
![License](https://img.shields.io/badge/License-MIT-green)

I spend most of my time these days **building agentic workflows with Claude Code** — turning it from an autocomplete into a fleet of agents that verify their own work, review each other, pull their own context, and run on a schedule. This marketplace is that practice packaged up: 60 small, focused plugins (skills, slash commands, subagents, and hooks) you can drop into your own setup — from the agentic-adoption core to an enterprise layer for security, compliance, governance, and quality, plus plugins modeled directly on Boris Cherny's own workflow.

📖 **New here?** Read [How to write a good plugin](./docs/writing-good-plugins.md) and [How plugins create lean, structured context](./docs/lean-structured-context.md) — the research behind this marketplace.

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

## 🕹️ How to use

### 1. Install (once)
```bash
/plugin marketplace add matthews-wong/claude-code-plugins   # add the marketplace
/plugin install <plugin>@matthews-agentic-plugins           # install any plugin
/plugin marketplace list                                    # browse everything
```
A plugin does nothing until it's installed in your Claude Code session — adding the marketplace just makes them available.

### 2. Four ways a plugin runs
| Component | How it triggers | Example |
| --- | --- | --- |
| **Skill** | **Auto-invoked** — Claude pulls it in when your request matches the skill's description (no command needed) | ask *"review this diff for security issues"* → `security-review-agent`'s skill fires |
| **Slash command** | You invoke it explicitly | `/context-audit`, `/scan-secrets`, `/spec` |
| **Subagent** | Runs in an isolated context (model delegates, or a skill routes to it) | the `code-reviewer` behind `/code-review` |
| **Hook** | **Deterministic** — fires automatically on an event once installed | `test-guardian` runs tests after every edit |

**Every plugin here ships an auto-invocable skill** (each `SKILL.md` has a `name` + a routing `description`), so most of the time you just describe what you want and the right skill loads itself. The language/stack skills (e.g. `javascript-standards`, `react-patterns`, `rest-api-design`) trigger when you write or review matching code.

### 3. Confirm a skill is firing
Auto-invocation is model-driven routing, not a hardwired switch — it fires when your task matches the description. To check:
```bash
/reload-plugins            # after installing/updating
```
Then give a task that should match and confirm Claude loads the skill instead of improvising. If it doesn't fire, the description needs sharpening (the #1 cause) — see [Writing a good plugin](./docs/writing-good-plugins.md).

### 4. Manage
```bash
/plugin                                          # browse & toggle installed plugins
/plugin marketplace update matthews-agentic-plugins
```

See the [quickstart](./examples/quickstart.md) for suggested bundles by goal.

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

## 📦 Core plugins — agentic adoption (20)

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

## 💻 Language & stack skills — *auto-invoke as you code*

These fire automatically when you write or review matching code — no command needed.

| Plugin | Triggers on | What it applies |
| --- | --- | --- |
| [**javascript-standards**](./plugins/javascript-standards) | `.js/.ts/.jsx/.tsx`, "modern JS" | ESM, `const`/`let`, `===`, async/await, immutability, real error handling. |
| [**typescript-typing**](./plugins/typescript-typing) | TS types, "any", generics | avoid `any` (→ `unknown` + narrowing), discriminated unions, constrained generics, `satisfies`, strict config. |
| [**react-patterns**](./plugins/react-patterns) | JSX/`.tsx`, hooks, components | rules of hooks, state colocation, stable keys, controlled inputs, effect cleanup, measured memoization, a11y. |
| [**css-responsive**](./plugins/css-responsive) | `.css/.scss`, "responsive", layout | mobile-first, flexbox vs grid, relative units, design tokens, `prefers-color-scheme`, container queries. |
| [**rest-api-design**](./plugins/rest-api-design) | API/endpoint design | resource naming, correct status codes, error envelope, pagination, idempotency, versioning, edge validation. |
| [**node-backend-patterns**](./plugins/node-backend-patterns) | Node/Express/Fastify | route→service→data layering, boundary validation, centralized async errors, env config, graceful shutdown. |

## 🏢 Enterprise plugins

Beyond the agentic-adoption core, an enterprise layer for teams that need security, compliance, governance, and quality guardrails.

### 🔒 Security & compliance
| Plugin | What it installs |
| --- | --- |
| [**secret-scanner**](./plugins/secret-scanner) | A hook + `/scan-secrets` that flag likely secrets (keys, tokens, private keys) in the diff before they leak. |
| [**dependency-auditor**](./plugins/dependency-auditor) | `/audit-deps` — vulnerability audit via native tooling (npm/pip/cargo/govulncheck) with triage. |
| [**license-compliance**](./plugins/license-compliance) | `/check-licenses` — inventory dependency licenses and flag ones outside your SPDX allowlist. |
| [**sbom-generator**](./plugins/sbom-generator) | `/generate-sbom` — produce a CycloneDX/SPDX Software Bill of Materials. |
| [**data-classification**](./plugins/data-classification) | `/classify-data` — classify fields (public/internal/confidential/PII) and recommend handling. |
| [**compliance-checklist**](./plugins/compliance-checklist) | `/compliance-check` — pre-release controls mapped to SOC 2 / ISO 27001. |
| [**access-review**](./plugins/access-review) | A read-only subagent that reviews IAM/RBAC changes for over-broad grants and escalation. |

### 📐 Governance & standards
| Plugin | What it installs |
| --- | --- |
| [**pr-governance**](./plugins/pr-governance) | `/pr-review` — enforce PR standards (description, linked ticket, size, tests, scope). |
| [**conventional-commits**](./plugins/conventional-commits) | `/commit` + a hook that formats and validates Conventional Commits. |
| [**adr-manager**](./plugins/adr-manager) | `/adr-new` + `/adr-list` — create and manage Architecture Decision Records. |
| [**changelog-generator**](./plugins/changelog-generator) | `/update-changelog` — maintain a Keep-a-Changelog from commit history. |
| [**release-manager**](./plugins/release-manager) | `/release` — a repeatable semver bump → tag → notes → checklist flow. |
| [**codeowners-manager**](./plugins/codeowners-manager) | `/codeowners` — scaffold and validate CODEOWNERS so critical paths are owned. |
| [**standards-enforcer**](./plugins/standards-enforcer) | `/enforce-standards` — check a diff against your editable org standards profile. |

### 🧪 Quality & reliability
| Plugin | What it installs |
| --- | --- |
| [**test-coverage-gate**](./plugins/test-coverage-gate) | A hook + `/coverage-gate` that gates below a configurable coverage threshold. |
| [**api-contract-guard**](./plugins/api-contract-guard) | `/api-compat` — detect breaking API changes by diffing OpenAPI/JSON schemas. |
| [**docs-guardian**](./plugins/docs-guardian) | A hook + `/docs-check` that flag stale docs when code changes. |
| [**incident-runbook**](./plugins/incident-runbook) | `/incident` — triage, comms templates, and a blameless postmortem scaffold. |
| [**terraform-policy**](./plugins/terraform-policy) | `/tf-policy` — policy-as-code checks for IaC (public buckets, open SGs, missing encryption). |

### 🧮 Context engineering
| Plugin | What it installs |
| --- | --- |
| [**context-budget**](./plugins/context-budget) | ⭐ `/context-audit` — audit `CLAUDE.md` and skills for bloat and enforce lean, structured context via progressive disclosure. |
| [**knowledge-loop**](./plugins/knowledge-loop) | 🧠 A self-improving, folder-scoped memory: a `SessionStart` hook auto-surfaces relevant past learnings via **local vector search**, and `/learn` records new gotchas/fixes — so each agent starts smarter than the last. |

### 🛡️ Security & policy skills — *auto-invocable reviews*
| Plugin | What it installs |
| --- | --- |
| [**threat-modeling**](./plugins/threat-modeling) | STRIDE threat modeling for a feature or design — attack surface + mitigations. |
| [**dockerfile-hardening**](./plugins/dockerfile-hardening) | Review/generate hardened Dockerfiles (non-root, pinned base, minimal layers, no secrets, healthcheck). |
| [**k8s-security-policy**](./plugins/k8s-security-policy) | Review K8s manifests against Pod Security Standards (securityContext, drop caps, no privileged, limits). |
| [**db-migration-safety**](./plugins/db-migration-safety) | Review a schema migration for safety — expand-contract, avoid long locks, nullable-first + backfill. |
| [**accessibility-audit**](./plugins/accessibility-audit) | Audit UI/markup for WCAG 2.2 AA basics — alt text, labels, contrast, keyboard nav, ARIA. |

> **Every plugin ships an auto-invocable skill** — each `SKILL.md` has a `name` and a routing `description`, so Claude pulls the right one in automatically when your task matches (not only via slash command).

## 🔁 Workflow patterns

Packaged straight from Anthropic's official *Claude Code best practices* guide.

| Plugin | What it installs |
| --- | --- |
| [**verify-app**](./plugins/verify-app) | An e2e-verification subagent that runs the app, exercises real flows, and reports PASS/FAIL with evidence. |
| [**spec-writer**](./plugins/spec-writer) | `/spec` — interviews you (via AskUserQuestion) and writes a self-contained `SPEC.md` to execute in a fresh session. |
| [**writer-reviewer**](./plugins/writer-reviewer) | `/review-fresh` — a fresh-context reviewer that checks the diff against the plan, flagging only correctness/requirement gaps. |
| [**context-cleaner**](./plugins/context-cleaner) | Spot the kitchen-sink / over-correction / infinite-exploration traps and recommend `/clear` + a better re-prompt. |
| [**fan-out-migrate**](./plugins/fan-out-migrate) | The large-migration fan-out: generate a file list, loop scoped `claude -p` per file, sample before scaling. |

## 🧑‍💻 Modeled on Boris Cherny's workflow

Plugins that operationalize how [Claude Code's creator actually works](./docs/boris-cherny-principles.md) — his own subagents and engineering principles.

| Plugin | What it installs |
| --- | --- |
| [**code-simplifier**](./plugins/code-simplifier) | Boris's own subagent — simplify the working diff after Claude is done; *prefer deleting lines to adding.* |
| [**mistake-logger**](./plugins/mistake-logger) | The preserve-mistakes loop — capture a repeated mistake into `CLAUDE.md` or a skill so the fix persists. |
| [**senior-standards**](./plugins/senior-standards) | His three principles as a skill + `/standards-check`: simplest change, root cause, minimal blast radius. |

## 📖 Research & guides

Three write-ups that motivate how these plugins are built:

- **[The Boris Cherny playbook](./docs/boris-cherny-principles.md)** — how Claude Code's creator uses it (verification loops, explore→plan→code, lean CLAUDE.md, subagents, parallel worktrees), with each plugin mapped to a practice.
- **[Writing a good Claude Code plugin](./docs/writing-good-plugins.md)** — choosing skill vs. command vs. subagent vs. hook, description-as-trigger, progressive disclosure, validation, and security.
- **[Lean & structured context](./docs/lean-structured-context.md)** — how skills, path-scoped rules, subagents, and deferred MCP schemas keep the context window lean, with the token-budget math.

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
