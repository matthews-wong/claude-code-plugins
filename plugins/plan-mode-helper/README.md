# plan-mode-helper

A plan-first workflow for Claude Code: investigate, propose a concise implementation plan,
get confirmation, then execute — so risky or multi-file changes never start with a
surprise edit.

## What it does

- Reads the relevant code before proposing anything.
- Produces a tight plan: goal, files to change, approach, risks, test strategy.
- Waits for the user to confirm or adjust before editing.
- Executes the approved plan and verifies with the stated test strategy.

## Components

- **Command:** `/plan <task description>` — run the plan-first workflow for a task.
- **Skill:** `plan-first` — the planning discipline Claude applies to non-trivial changes.

## Usage

`/plan add pagination to the users API` — Claude investigates, presents a plan, and holds
for your approval before writing code. Pairs naturally with Claude Code's built-in plan
mode (`permissions.defaultMode: "plan"`).

Author: Matthews Wong · License: MIT
