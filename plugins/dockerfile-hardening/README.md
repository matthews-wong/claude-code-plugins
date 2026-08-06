# dockerfile-hardening

A skill-first Claude Code plugin that reviews or generates **hardened, production-grade Dockerfiles**.

## What it does
Auto-invokes when you mention a "Dockerfile", "container image", or ask to "harden" one. It checks for pinned+digested base images, non-root users, multi-stage builds, absence of secrets, minimal layers, HEALTHCHECK, and dropped capabilities — then returns a findings table and a corrected Dockerfile.

## Structure
- `skills/dockerfile-hardening/SKILL.md` — review/generate method + core controls.
- `skills/dockerfile-hardening/reference/checklist.md` — full pass/fail checklist with severity and rationale.
- `skills/dockerfile-hardening/reference/patterns.md` — multi-stage templates (Go/Node/Python/Java), runtime flags, `.dockerignore`.

## Usage
Paste a Dockerfile and ask for a security review, or ask for a hardened Dockerfile for your stack. The skill activates automatically.

## Note
It recommends running a scanner (Trivy, Grype, Docker Scout) rather than reporting fabricated scan output.

## License
MIT © Matthews Wong
