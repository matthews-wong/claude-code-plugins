# access-review

Reviews IAM/RBAC/permission changes in a diff for **over-broad grants, wildcards, and privilege escalation**, and reports risks by severity — grounded in least-privilege principles.

## What it provides

- **`access-reviewer` subagent** — a **read-only** reviewer (Read/Grep/Glob only) that inspects access-control changes and reports findings by severity. It never modifies files or runs commands.
- **`/access-review`** — gathers the working diff, routes access-control changes to the subagent, and relays the prioritized findings.

## What it catches

- Wildcards in actions/resources (`"*":"*"`, `s3:*`, K8s `verbs: ["*"]`).
- Privilege-escalation primitives (`iam:PassRole`, `sts:AssumeRole` widening, K8s `bind`/`escalate`/`impersonate`).
- Over-broad principals/trust (`Principal: "*"`, `allUsers`, `system:authenticated`).
- Admin/owner grants (`AdministratorAccess`, `roles/owner`, `cluster-admin`).
- Scope widening (namespaced → cluster-scoped, specific ARN → `*`) and removed guardrails (dropped `Condition`/`Deny`/boundary).

Covers AWS/GCP/Azure IAM, Kubernetes RBAC, Terraform/IaC, and app-level RBAC (OPA/Rego, Casbin).

## Caveat

A static diff review cannot compute **effective** permissions across all attached policies. For definitive checks use AWS IAM Access Analyzer, GCP Policy Analyzer, or `kubectl auth can-i`. Findings are grounded only in the reviewed text — no policy content is fabricated.

## License

MIT — Matthews Wong
