# data-classification

Claude Code plugin for data-handling policy enforcement. Classifies data fields as **public / internal / confidential / PII**, flags PII and secrets in code, schemas, and logs, and recommends handling controls (encryption, retention, minimization).

## Components

- **`/classify-data [path or fields]`** — runs a classification pass over a schema, model, migration, or field list and outputs a tier table with required handling and risk-ranked actions.
- **`data-classification` skill** — auto-triggers when you review schemas, payloads, config, or log statements for sensitive data. Lean summary plus `reference/classification-matrix.md` for full rules (progressive disclosure).

## Usage

```
/classify-data src/models/user.ts
/classify-data email, ip_address, ticket_id, api_key
```

## Notes

The skill stays under budget by keeping only the decision heuristic and baseline controls inline; the detailed matrix, keyword map, and tie-breakers load on demand from the reference file. Recommendations are framework-neutral; no regulatory citations are fabricated.

MIT licensed. Author: Matthews Wong.
