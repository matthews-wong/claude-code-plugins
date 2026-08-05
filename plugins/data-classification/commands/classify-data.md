---
name: classify-data
description: Classify data fields in a schema, model, or file and recommend handling controls for each sensitivity tier.
args: "[path or field list] — optional file, directory, or comma-separated field names to classify"
---

You are performing a data classification pass for the target: `$ARGUMENTS` (if empty, ask the user for a schema file, model, or list of fields, or infer from the current working set).

Follow this procedure:

1. **Gather fields.** Read the target schema, ORM model, migration, DTO, config, or log statement. Enumerate every distinct data field or value being stored, transmitted, or logged. Do not guess at fields that are not present.

2. **Classify each field** into exactly one tier — `public`, `internal`, `confidential`, or `PII` (a field may be both confidential and PII; when so, treat PII handling as the floor). Load the `data-classification` skill and consult its classification matrix reference for tier definitions and field-name heuristics. Base each decision on the field's semantics, not only its name.

3. **Flag PII and secrets** explicitly. Call out any PII appearing in log statements, error messages, analytics events, URLs, or plaintext storage — these are the highest-priority findings. Flag credentials/tokens/keys as confidential secrets that must never be logged or committed.

4. **Recommend handling** per field: encryption at rest / in transit, retention limit, access restriction, data minimization (should it be collected at all?), masking/tokenization for logs, and pseudonymization where it reduces exposure.

5. **Output** a Markdown table with columns: Field | Tier | Rationale | Required Handling. Below the table, list the top action items ordered by risk, and note any field you could not confidently classify so a human can decide.

Be precise and conservative: when in doubt between two tiers, choose the more restrictive one and say why. Do not fabricate regulatory citations; refer to control categories generically unless the repo states a specific framework.
