---
name: iac-policy
description: >
  Use when reviewing Terraform or other IaC for security/compliance, running
  policy-as-code, or writing OPA/Rego rules. Triggers: "terraform security",
  "policy as code", "conftest", "opa", "rego", "tfsec", "checkov", "trivy
  config", "public S3 bucket", "open security group", "0.0.0.0/0", "missing
  encryption", "required tags", "IaC scan", "CIS benchmark terraform".
---

# IaC Policy-as-Code

Catch insecure or non-compliant infrastructure in the code, before it is
applied. Policy-as-code expresses rules as versioned, testable artifacts so the
same checks run locally, in CI, and in review.

## What the tools are (honestly)

- **tfsec / Trivy config** — fast, opinionated Terraform static analysis with a
  built-in rule set. tfsec is now merged into **Trivy** (`trivy config`).
- **Checkov** — broad multi-IaC (Terraform, CFN, K8s, ARM, Helm) scanner with
  many built-in policies and CIS/benchmark mappings; supports custom policies.
- **Conftest + OPA (Rego)** — a general policy engine. You write the rules in
  Rego; ideal for **org-specific** policy the built-in scanners don't cover.
  Test the Terraform **plan JSON**, not raw HCL, so computed values resolve.

None of these prove a system is secure. They check for known-bad patterns in the
code. They do not see runtime state, drift, or logic bugs. Report what passed the
checks that ran — nothing more.

## High-value checks

Prioritize the misconfigurations that most often cause real breaches:

1. **Public storage** — S3 public ACL/policy, `block_public_acls` false,
   publicly readable buckets.
2. **Open ingress** — security group `0.0.0.0/0`/`::/0` to SSH(22), RDP(3389),
   or database ports.
3. **Unencrypted data** — S3/EBS/RDS/snapshots without encryption at rest; no
   TLS enforcement in transit.
4. **Over-broad IAM** — `Action: "*"`, `Resource: "*"`, wildcard trust policies.
5. **Public compute/db** — RDS/instances with public IPs or open to the world.
6. **Missing tags** — owner, environment, cost-center, data-classification.
7. **Missing logging/versioning** — no access logs, no bucket versioning.

Concrete rules, offending patterns, and Terraform fixes are in
`./reference/policies.md`. A starter Conftest/Rego workflow is in
`./reference/conftest-opa.md`.

## Workflow

1. Detect installed scanner (Checkov / tfsec / Trivy / Conftest). Prefer it.
2. For Conftest/OPA, generate plan JSON:
   `terraform plan -out=tf.plan && terraform show -json tf.plan > plan.json`.
3. Run the scan; group findings by severity; give a fix per finding.
4. Wire into CI + pre-commit; keep custom Rego versioned with the code.

## Guardrails

- Never call infrastructure "secure" — only "passed checks X, Y, Z."
- Do not fabricate rule IDs, CVSS scores, or CIS control numbers. If you don't
  have the real ID from the tool, describe the rule instead.
- Static scanning ≠ runtime posture; note that drift and live config are out of
  scope for IaC scanning.
