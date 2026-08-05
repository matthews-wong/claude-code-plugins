# adr-manager

Create and manage Architecture Decision Records (ADRs) in a MADR-style format.

## Commands

- **`/adr-new "<title>"`** — creates the next numbered record
  (`NNNN-title.md`) in `docs/adr/` (created if absent), pre-filled from the
  MADR template with Status `Proposed` and today's date.
- **`/adr-list [status]`** — lists existing records as
  `# | Title | Status | Date`, with an optional status filter.

## Template

Each record captures **Context**, **Decision**, **Consequences**, and
**Considered Options**, with a status lifecycle of
Proposed -> Accepted -> Deprecated / Superseded (or Rejected). Full annotated
template and an example live in `skills/adr-authoring/reference/`.

## License

MIT — Matthews Wong
