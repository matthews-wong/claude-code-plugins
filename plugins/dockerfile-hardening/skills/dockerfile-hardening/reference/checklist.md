# Dockerfile Hardening Checklist

Mark each PASS / FAIL / N/A against the actual file. Severity reflects typical production risk.

## Base image & supply chain
- [ ] **[High]** Base image pinned to an explicit tag AND `@sha256:` digest (no `latest`, no floating major).
- [ ] **[High]** Base image is minimal (distroless / `-slim` / `alpine` / `scratch`) rather than a full OS.
- [ ] **[Med]** Base image is from a trusted/official or internally-vetted registry.
- [ ] **[Med]** Dependencies installed from lockfiles with pinned versions; checksums/signatures verified where supported.
- [ ] **[Low]** Image is rebuilt regularly to pick up base patches (documented in CI, not the Dockerfile itself).

## Privilege & runtime user
- [ ] **[High]** A non-root user is created and `USER` switches to it before the entrypoint runs.
- [ ] **[High]** The final running process does not run as UID 0.
- [ ] **[Med]** Prefer a numeric UID (e.g. `USER 10001`) so orchestrators can enforce `runAsNonRoot`.
- [ ] **[Med]** File ownership/permissions on copied artifacts are least-privilege (`COPY --chown`, no world-writable).

## Secrets
- [ ] **[High]** No secrets, tokens, private keys, or credentials in `ENV`, `ARG`, or copied files.
- [ ] **[High]** Build-time secrets use BuildKit `--mount=type=secret`, never baked into a layer.
- [ ] **[Med]** A `.dockerignore` excludes `.git`, `.env`, secrets, and build junk from the build context.
- [ ] **[Med]** Runtime secrets are injected by the platform (env/volume/secret manager), not the image.

## Build structure & footprint
- [ ] **[High]** Multi-stage build: build tooling and source excluded from the final image.
- [ ] **[Med]** Package manager caches cleaned in the same `RUN` layer (`rm -rf /var/lib/apt/lists/*`, `--no-cache`).
- [ ] **[Med]** `--no-install-recommends` (apt) / minimal package sets; no compilers/curl/shells left in final image if avoidable.
- [ ] **[Low]** Related `RUN` commands combined to reduce layers; `.dockerignore` keeps context small.

## Runtime configuration
- [ ] **[Med]** `HEALTHCHECK` defined, or liveness/readiness delegated to the orchestrator (documented).
- [ ] **[Med]** `ENTRYPOINT`/`CMD` in exec form (`["bin","arg"]`), not shell form, so signals propagate (PID 1 handling).
- [ ] **[Med]** `WORKDIR` set explicitly (never rely on `/`).
- [ ] **[Low]** `EXPOSE` only the ports actually served.
- [ ] **[Low]** OCI `LABEL`s for source, revision, and maintainer.

## Documented deploy-time hardening (belongs in orchestration, verify it's intended)
- [ ] Read-only root filesystem (`--read-only` / `readOnlyRootFilesystem`).
- [ ] Drop all Linux capabilities, add back only required ones (`--cap-drop=ALL`).
- [ ] `no-new-privileges` set.
- [ ] Resource limits (CPU/memory) applied.
- [ ] Image scanned in CI (Trivy / Grype / Docker Scout) and blocked on critical findings.

## Rationale highlights
- **Digest pinning** guarantees the exact bytes you tested are what ships — a moving tag is a supply-chain risk.
- **Non-root + cap-drop** limits blast radius if the app is compromised.
- **Multi-stage** removes compilers and shells that turn a foothold into RCE.
- **No secrets in layers**: every layer is extractable; a deleted secret in an earlier layer still ships.
