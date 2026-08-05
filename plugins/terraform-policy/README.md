# terraform-policy

Policy-as-code checks for Terraform and other IaC. Flags public buckets, open
security groups, missing encryption and tags, and over-broad IAM — and explains
policy-as-code honestly.

## Components

- **`/tf-policy [path]`** — detects an installed scanner (Checkov, tfsec/Trivy,
  or Conftest/OPA), runs it, and reports findings by severity with a concrete
  Terraform fix per issue. Falls back to a labeled manual review if no scanner
  is present.
- **Skill: iac-policy** — the high-value check catalog and an honest account of
  what each tool does. References:
  - `skills/iac-policy/reference/policies.md` — offending patterns + fixes.
  - `skills/iac-policy/reference/conftest-opa.md` — Rego starter policies + CI.

## Honest scope

Static IaC scanning catches known-bad patterns in code — not runtime drift or
live state. The plugin never calls infrastructure "secure," only "passed the
checks that ran," and never fabricates rule IDs or compliance mappings.

## Recommended tools

[Checkov](https://www.checkov.io/), [Trivy](https://trivy.dev/) (which now
includes tfsec), and [Conftest](https://www.conftest.dev/) + OPA for custom Rego
policy. The plugin works best with at least one installed.

Author: Matthews Wong · License: MIT
