# Policy catalog (Terraform examples)

Each entry: the risk, the offending pattern, and a corrected snippet. AWS is used
for examples; the same categories apply to Azure/GCP.

## 1. Public S3 buckets

Risk: data exposure to the internet.

Offending:
```hcl
resource "aws_s3_bucket" "data" { bucket = "my-data" }
# no public access block; ACL/policy may allow public read
```

Fix — always attach a public access block:
```hcl
resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

## 2. Open security groups

Risk: world-reachable admin/database ports.

Offending:
```hcl
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]   # SSH open to the world
}
```

Fix — restrict to known CIDRs / use SSM Session Manager instead:
```hcl
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/8"]  # corporate range, or drop 22 entirely
}
```

Flag any `0.0.0.0/0` (or `::/0`) ingress, especially ports 22, 3389, 3306,
5432, 6379, 27017, 9200.

## 3. Missing encryption at rest

Offending: S3/EBS/RDS with no encryption block.

Fix examples:
```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" }
  }
}

resource "aws_db_instance" "db" {
  # ...
  storage_encrypted = true
  kms_key_id        = aws_kms_key.db.arn
}

resource "aws_ebs_volume" "vol" {
  # ...
  encrypted = true
}
```

## 4. Over-broad IAM

Offending:
```hcl
statement {
  actions   = ["*"]
  resources = ["*"]
}
```

Fix — scope actions and resources to least privilege; avoid wildcards on both.

## 5. Publicly exposed compute / databases

Fix:
```hcl
resource "aws_db_instance" "db" { publicly_accessible = false }
resource "aws_instance" "app"  { associate_public_ip_address = false }
```

## 6. Missing required tags

Enforce a standard tag set on every resource:
```hcl
tags = {
  Owner       = "team-platform"
  Environment = "prod"
  CostCenter  = "cc-1234"
  DataClass   = "confidential"
}
```
Use `default_tags` on the provider to apply org-wide tags automatically.

## 7. Logging and versioning

```hcl
resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_logging" "data" {
  bucket        = aws_s3_bucket.data.id
  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3/"
}
```

## Severity guidance

- Critical: public data store, world-open admin/db port, wildcard IAM.
- High: missing encryption on sensitive data, public DB/instance.
- Medium: missing logging/versioning, weak TLS policy.
- Low: missing tags, cosmetic policy deviations.

Severity depends on data sensitivity and exposure — a public bucket of static
assets differs from one holding PII. State the assumption behind each rating.
