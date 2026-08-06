---
name: dockerfile-hardening
description: Use when reviewing, writing, or hardening a "Dockerfile" or "container image" — triggers on "harden image", "Docker security", "non-root container", "distroless", "multi-stage build", "pin base image", or when a Dockerfile is shown and the user wants it production/enterprise-ready. Produces a hardened Dockerfile and a findings list mapped to concrete fixes.
---

# Dockerfile Hardening

Review an existing Dockerfile or generate a new one that is safe for enterprise production. Work from the concrete Dockerfile in front of you; do not assume best practices are present.

## When reviewing

1. Read the Dockerfile top to bottom. Note base image, stages, user, exposed ports, entrypoint, and anything copied in.
2. Run the checklist in `reference/checklist.md`. For each item, mark PASS / FAIL / N/A with the offending line.
3. Report findings as a table: Severity | Issue | Line | Fix. Order High → Low.
4. Provide a corrected Dockerfile (or a unified diff) implementing the High/Medium fixes.
5. Note anything that needs a human decision (e.g. which minimal base is acceptable, whether a package is truly required).

## When generating

Produce a **multi-stage** Dockerfile that satisfies the core controls below. Match the project's language/runtime. See `reference/patterns.md` for language-specific multi-stage templates (Go, Node, Python, Java).

## Core controls (must-haves)

1. **Pinned base + digest.** Reference a specific tag AND `@sha256:` digest, e.g. `FROM node:20.14.0-slim@sha256:...`. Never `latest`. Prefer minimal bases (distroless, `-slim`, `alpine`, or scratch) to shrink attack surface.
2. **Non-root user.** Create and switch to an unprivileged user (`USER 10001` or a named user). The final process must not run as UID 0.
3. **Multi-stage build.** Compile/build in a builder stage; copy only the runtime artifact into a minimal final stage. Keep build tools, source, and caches out of the final image.
4. **No secrets in the image.** No tokens, keys, or `.env` in `ENV`, `ARG`-baked values, or copied files. Use BuildKit `--mount=type=secret` for build-time secrets; inject runtime secrets at deploy time. Add a `.dockerignore`.
5. **Minimal layers & footprint.** Combine related `RUN` steps, clean package caches in the same layer (`rm -rf /var/lib/apt/lists/*`), install only what is needed (`--no-install-recommends`).
6. **HEALTHCHECK.** Define a meaningful `HEALTHCHECK` (or document that orchestration handles liveness/readiness probes instead).
7. **Least privilege at runtime.** Document the intended runtime hardening: read-only root filesystem, `--cap-drop=ALL` (add back only what is required), `--security-opt=no-new-privileges`, non-root enforced by the orchestrator.
8. **Deterministic dependencies.** Use lockfiles and pinned package versions; verify checksums/signatures where the ecosystem supports it.
9. **Explicit metadata.** Set `WORKDIR`, a non-shell-form `ENTRYPOINT` (exec form `["..."]`), `EXPOSE` only needed ports, and OCI `LABEL`s.

## Output

A findings table plus the hardened Dockerfile. Do not invent CVE counts or scanner output — recommend running a scanner (Trivy, Grype, Docker Scout) rather than reporting fabricated results.

## References

- `reference/checklist.md` — full pass/fail hardening checklist with rationale.
- `reference/patterns.md` — multi-stage templates per language + runtime flags + `.dockerignore`.
