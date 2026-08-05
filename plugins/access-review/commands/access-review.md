---
name: access-review
description: Review IAM/RBAC/permission changes in the working diff for over-broad grants, wildcards, and privilege escalation, reporting risks by severity.
---

You are helping the user review access-control changes for security risk before they are merged. This is a read-only review — inspect and report, do not modify access configuration.

## What to do

1. Gather the changes to review:
   - Prefer the diff: `git diff --staged` and `git diff` (or `git diff <base>...HEAD` for a PR branch).
   - Identify files that touch access control: IAM policies/roles, Terraform IAM resources, Kubernetes RBAC manifests (`Role`/`ClusterRole`/`*Binding`), trust policies, OPA/Rego, and app-level role/permission definitions.
2. Delegate the analysis to the **access-reviewer** subagent (read-only: Read/Grep/Glob). Give it the list of changed access-control files and the diff context. It will flag over-broad grants, wildcards, over-broad principals/trust, privilege-escalation primitives, scope widening, and removed guardrails — and report by severity.
3. Relay the subagent's findings to the user, ordered by severity, with concrete least-privilege remediations.

## How to report

Lead with the highest severity found and a count by severity. Then list findings (file, the specific grant, why it is risky, how to tighten it). Acknowledge changes that improve posture. Note the caveat that a static diff review cannot compute effective permissions across all attached policies — recommend an authoritative analyzer (AWS IAM Access Analyzer, GCP Policy Analyzer, `kubectl auth can-i`) for definitive checks. Do not fabricate policy content.
