# Vulnerability triage rubric

Triage turns a raw list of advisories into a prioritized action plan. Use tool output as ground truth.

## Ranking inputs

1. **Severity** — from the advisory (Critical / High / Moderate / Low), often derived from CVSS. Do not restate a CVSS number the tool did not provide.
2. **Fix availability** — is there a fixed version? "No fix yet" changes the response (mitigate, pin, or accept risk).
3. **Reachability** — is the vulnerable code path actually called? govulncheck answers this directly; for other ecosystems, reason about whether the affected API is used.
4. **Direct vs transitive** — direct deps are yours to upgrade; transitive ones may need an override/resolution or an upstream bump.
5. **Runtime vs dev/test** — a vuln only in build/test tooling is generally lower risk than one in shipped runtime code.
6. **Exposure** — is the affected functionality exposed to untrusted input (network, user data)?

## Response patterns

- **Fix available, non-breaking**: upgrade now. For transitive deps, use `overrides` (npm), `resolutions` (yarn/pnpm), or bump the parent.
- **Fix available, breaking**: schedule the upgrade; assess migration cost; mitigate in the interim if reachable.
- **No fix available**: apply mitigations (input validation, disable the feature, network controls), pin to a known-safe version if one exists, and document a time-boxed risk acceptance.
- **Not reachable / not applicable**: document why, optionally suppress in the tool's ignore config with a rationale and review date. Never silently ignore.

## Remediation output

For each actionable finding provide: package, installed version, advisory ID, fixed version (or "none"), direct/transitive, recommended action. Then a short ordered "do this first" list. Re-run the audit after changes and confirm the count drops.

## Suppressions

Every suppression/ignore needs: the advisory ID, a written justification, an owner, and a review-by date. Suppressions are a ledger, not a mute button.
