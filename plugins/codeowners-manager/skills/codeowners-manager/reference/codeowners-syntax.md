# CODEOWNERS Syntax & Coverage (reference)

Detailed rules for the `codeowners-manager` skill. Load on demand.

## Pattern matching rules

CODEOWNERS uses a gitignore-style syntax, with important differences:

- `*` matches anything except a `/`. `**` matches across directories.
- A leading `/` anchors the pattern to the repository root. Without it, the pattern can match at any depth.
- A trailing `/` restricts the match to directories (and their contents).
- `docs/*` matches files directly in `docs/` but NOT files in `docs/sub/` — use `docs/` or `docs/**` for the whole tree.
- Unlike gitignore, CODEOWNERS does **not** support `!` negation. You cannot exclude a subpath; instead add a more specific later rule with the desired owner.
- Escaping and character ranges from gitignore are not fully supported — keep patterns simple.

## Ordering: last match wins

GitHub evaluates rules top to bottom and applies the **last** pattern that matches a changed file — not the most specific. Consequences:

- Put broad defaults first (`* @org/maintainers`), then progressively more specific overrides.
- A broad rule placed after a specific one will shadow it. Example bug:
  ```
  /src/auth/**   @org/security
  *              @org/maintainers   # BUG: this now owns everything, including auth
  ```
- To validate, for each critical path determine the LAST matching line and confirm it names the intended owner.

## Owners

- Forms: `@username`, `@org/team`, or `user@example.com` (must map to a GitHub account with repo access).
- Teams must have at least write/triage access and be visible to the repository, or GitHub silently ignores them.
- Multiple owners on one line are all requested as reviewers.
- A line with a pattern and no owner clears ownership for matching paths.

## Critical-path coverage checklist

Ensure an explicit owner for each of these when present in the repo:

- Authentication / authorization / identity code.
- Security configuration, crypto, secrets handling, `.env` templates.
- CI/CD: `/.github/workflows/`, pipeline configs, release automation.
- Infrastructure as code: Terraform, CloudFormation, Kubernetes/Helm manifests, Ansible.
- Dependency manifests & lockfiles: `package.json`, `package-lock.json`, `yarn.lock`, `requirements*.txt`, `poetry.lock`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile.lock`.
- Database migrations and schema definitions.
- Payment, billing, and PII-handling modules.
- The CODEOWNERS file itself and other governance files (SECURITY.md, branch-protection config).

## Recipe: layered ownership

```
# 1. Default owner for everything
*                          @org/maintainers

# 2. Domain teams
/services/billing/**       @org/payments
/services/identity/**      @org/security

# 3. Cross-cutting sensitive paths (kept last so nothing shadows them)
/.github/workflows/        @org/platform @org/security
/infra/**                  @org/platform
**/migrations/**           @org/data
/CODEOWNERS                @org/security
/SECURITY.md               @org/security
```

## Validation output guidance

Report findings as: Path pattern | Owner | Issue | Fix. Categorize issues as: unowned-critical, shadowed-rule, dead-pattern (matches nothing), missing-owner (rule clears ownership), invalid-owner (team/user unlikely to resolve). Offer a corrected file rather than only listing problems.
