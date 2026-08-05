# Quickstart

Get from zero to a working agentic setup in a few minutes.

## 1. Add the marketplace

```bash
/plugin marketplace add matthews-wong/claude-code-plugins
```

Confirm it loaded:

```bash
/plugin marketplace list
```

## 2. Install a starter set

A good first three that pay off immediately:

```bash
# Close the verification loop — Boris Cherny's #1 lever
/plugin install verify-before-review@matthews-agentic-plugins

# A fresh-context reviewer for your diff
/plugin install code-review-agent@matthews-agentic-plugins

# Keep your context lean
/plugin install context-budget@matthews-agentic-plugins
```

## 3. Use them

```bash
# Run the project's tests/lint/build and report before you review
/verify

# Review the working diff for bugs and edge cases
/code-review

# Audit CLAUDE.md and skills for bloat
/context-audit
```

## 4. Suggested bundles by goal

| Your goal | Install |
| --- | --- |
| **Ship faster, safely** | `verify-before-review`, `code-review-agent`, `plan-mode-helper`, `permission-optimizer` |
| **Scale to many agents** | `worktree-isolation`, `parallel-lanes`, `agent-kickoff`, `writer-reviewer` |
| **Lean context** | `context-budget`, `claude-md-manager`, `mistake-logger` |
| **Enterprise guardrails** | `secret-scanner`, `pr-governance`, `compliance-checklist`, `test-coverage-gate` |
| **Work like the creator** | `code-simplifier`, `senior-standards`, `verify-app`, `spec-writer` |

## 5. Uninstall / manage

```bash
/plugin                 # browse and toggle installed plugins
/plugin marketplace update matthews-agentic-plugins
```

## Validate locally (for contributors)

```bash
python scripts/validate_marketplace.py
# or, in Claude Code:
/plugin validate .
```

See the [docs](../docs/) for the research and design principles, and the [Boris Cherny playbook](../docs/boris-cherny-principles.md) for why these plugins are shaped the way they are.
