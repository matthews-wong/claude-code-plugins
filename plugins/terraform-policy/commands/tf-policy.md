---
name: tf-policy
description: Run policy-as-code checks over Terraform/IaC and flag insecure or non-compliant resources.
args: "[path] (optional directory of Terraform files; defaults to current dir)"
---

Evaluate Infrastructure-as-Code against security and compliance policy. Load the
skill `iac-policy` for the check catalog and honest scope of each tool.

Steps:

1. Scope the target: the given path or the current directory. Identify the IaC
   type (Terraform `.tf`, Terraform plan JSON, CloudFormation, etc.).

2. Prefer a real scanner if one is installed; report its findings and explain
   them. Detect and use, in rough order of convenience:
   - **Checkov** — `checkov -d <path>` (broad built-in policy set, multi-IaC).
   - **tfsec** — `tfsec <path>` (Terraform-focused, now part of Trivy:
     `trivy config <path>`).
   - **Conftest + OPA** — `conftest test <plan.json>` against Rego policies for
     custom org rules. For accurate results, evaluate a **plan**, not raw HCL:
     `terraform plan -out=tf.plan && terraform show -json tf.plan > plan.json`.

   If none are installed, do a best-effort static review of the HCL yourself
   using the policy catalog, and clearly label it as a manual review, not a
   certified scan.

3. Apply the high-value policy checks (see skill + `./reference/policies.md`):
   - **Public S3 / storage**: public ACLs, `block_public_*` disabled, public
     bucket policies.
   - **Open security groups**: `0.0.0.0/0` (or `::/0`) ingress, especially to
     22/3389/database ports.
   - **Missing encryption**: unencrypted S3, EBS, RDS, snapshots; no KMS;
     encryption-in-transit not enforced.
   - **Missing required tags**: owner, environment, cost-center, data-class.
   - **Public exposure**: RDS/instances with public IPs, open metadata, wildcard
     IAM (`Action: "*"`, `Resource: "*"`).
   - **Logging/versioning**: disabled access logging, no bucket versioning.

4. Report findings grouped by severity (Critical/High/Medium/Low). For each:
   the resource and file:line, the rule, why it matters, and the concrete
   Terraform fix (show the corrected attribute).

5. Recommend wiring the chosen tool into CI (pre-commit + pipeline) and, for
   org-specific rules, writing Rego policies for Conftest/OPA.

Be honest about limits: static IaC scanning catches misconfigurations in code,
not drift or runtime state. Never claim a resource is "secure" — only that it
passed the checks that ran. Do not fabricate rule IDs or CV/compliance mappings.
