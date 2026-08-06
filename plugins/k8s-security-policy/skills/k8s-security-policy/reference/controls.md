# Kubernetes Security Control List

Paths are relative to the Pod spec (`spec` for a Pod, `spec.template.spec` for controllers). Container-level fields live under `containers[*].securityContext`.

## Container securityContext (Restricted profile)

| Control | Path | Required value | Severity | Why |
|---|---|---|---|---|
| No privileged | `securityContext.privileged` | `false` (or unset) | High | Privileged = full host access; effectively root on the node. |
| No priv escalation | `securityContext.allowPrivilegeEscalation` | `false` | High | Blocks setuid binaries from gaining more privs than the parent. |
| Run as non-root | `securityContext.runAsNonRoot` | `true` | High | Prevents UID 0 in-container; limits blast radius. |
| Explicit UID/GID | `securityContext.runAsUser` / `runAsGroup` | non-zero | Med | Deterministic identity; needed when image lacks a USER. |
| Drop capabilities | `securityContext.capabilities.drop` | `["ALL"]` | High | Removes Linux caps; add back only the specific one needed. |
| Read-only root FS | `securityContext.readOnlyRootFilesystem` | `true` | Med | Stops tampering/persistence; use emptyDir for writable dirs. |
| Seccomp | `securityContext.seccompProfile.type` | `RuntimeDefault` | Med | Restricts syscalls to a safe default set. |

Can also be set once at pod level (`spec.securityContext`) for `runAsNonRoot`, `runAsUser`, `fsGroup`, `seccompProfile`; container-level overrides pod-level.

## Pod-level & structural controls

| Control | Path | Required | Severity | Why |
|---|---|---|---|---|
| No host network | `hostNetwork` | false/absent | High | Shares node network namespace; bypasses NetworkPolicy. |
| No host PID | `hostPID` | false/absent | High | Can see/signal host processes. |
| No host IPC | `hostIPC` | false/absent | High | Shares host IPC; cross-container leakage. |
| No hostPath volumes | `volumes[*].hostPath` | absent | High | Mounts node filesystem; classic escape/priv-esc vector. |
| No hostPort | `containers[*].ports[*].hostPort` | absent | Med | Binds node port; bypasses Services and scheduling. |
| SA token opt-out | `automountServiceAccountToken` | `false` unless needed | Med | Prevents handing API credentials to workloads that don't call the API. |
| Dedicated SA | `serviceAccountName` | non-default | Low | Enables least-privilege RBAC. |

## Reliability / DoS controls

| Control | Path | Required | Severity | Why |
|---|---|---|---|---|
| CPU/memory requests | `containers[*].resources.requests` | set | Med | Scheduling + fair sharing. |
| CPU/memory limits | `containers[*].resources.limits` | set | Med | Caps consumption; prevents node exhaustion (DoS). |
| Liveness probe | `containers[*].livenessProbe` | set | Low | Restart on hang. |
| Readiness probe | `containers[*].readinessProbe` | set | Low | Keep traffic off unready pods. |

## Image & supply chain

| Control | Path | Required | Severity |
|---|---|---|---|
| Pinned image + digest | `containers[*].image` | `repo:tag@sha256:...`, never `:latest` | Med |
| Pull policy | `containers[*].imagePullPolicy` | `IfNotPresent`/`Always` consistent with digest | Low |

## Enforcement: Pod Security Admission

Label the namespace so the API server enforces the standard (built-in, no extra components):

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: app
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```

Profiles: `privileged` (no restrictions), `baseline` (blocks known escalations), `restricted` (hardened best practice — target this). For policy beyond PSS (image registries, required labels, custom rules) use an admission controller: Kyverno, OPA/Gatekeeper, or Validating Admission Policy (CEL).

Also apply a default-deny **NetworkPolicy** per namespace and least-privilege **RBAC** — these are cluster controls that complement the Pod-level `securityContext`.
