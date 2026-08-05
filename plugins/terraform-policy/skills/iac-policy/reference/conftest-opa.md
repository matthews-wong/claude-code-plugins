# Conftest + OPA (Rego) starter

Use Conftest/OPA for **organization-specific** rules that the built-in scanners
(Checkov, tfsec/Trivy) don't cover. Evaluate the Terraform **plan JSON** so
computed and resolved values are visible.

## Generate plan JSON

```sh
terraform init
terraform plan -out=tf.plan
terraform show -json tf.plan > plan.json
```

## Example policy: deny public S3 buckets

`policy/s3.rego`:
```rego
package main

# Deny any S3 bucket public access block that allows public access.
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_public_access_block"
  resource.change.after.block_public_acls == false
  msg := sprintf("S3 bucket '%s' must set block_public_acls = true", [resource.address])
}
```

## Example policy: deny 0.0.0.0/0 SSH ingress

`policy/sg.rego`:
```rego
package main

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group"
  rule := resource.change.after.ingress[_]
  rule.from_port <= 22
  rule.to_port   >= 22
  cidr := rule.cidr_blocks[_]
  cidr == "0.0.0.0/0"
  msg := sprintf("Security group '%s' exposes SSH (22) to 0.0.0.0/0", [resource.address])
}
```

## Example policy: require tags

`policy/tags.rego`:
```rego
package main

required_tags := {"Owner", "Environment", "CostCenter", "DataClass"}

deny[msg] {
  resource := input.resource_changes[_]
  tags := object.get(resource.change.after, "tags", {})
  missing := required_tags - {k | tags[k]}
  count(missing) > 0
  msg := sprintf("%s is missing required tags: %v", [resource.address, missing])
}
```

## Run

```sh
conftest test plan.json -p policy/
```

Conftest exits non-zero on any `deny` — good as a CI gate. Use `warn[msg]` for
advisory-only rules that should not fail the build.

## CI wiring

- Add a pipeline step running `checkov -d .` (or `trivy config .`) plus
  `conftest test plan.json -p policy/`.
- Add a pre-commit hook so developers catch issues before pushing.
- Keep Rego policies versioned alongside the Terraform they govern; write unit
  tests for policies with `conftest verify` / OPA test.

## Honest scope

- Plan-based evaluation reflects intended changes, not live/drifted state.
- Rego rules are only as good as the resource attributes present in the plan;
  some provider-computed values appear as `null`/unknown at plan time — handle
  those cases explicitly rather than assuming compliance.
