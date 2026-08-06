---
name: k8s-security-policy
description: Use when reviewing Kubernetes manifests (Pod, Deployment, StatefulSet, DaemonSet, Job) for security — triggers on "kubernetes security", "securityContext", "pod security", "Pod Security Standards", "harden this manifest", "runAsNonRoot", "readOnlyRootFilesystem", or when YAML for a K8s workload is shown. Produces findings mapped to the Restricted profile plus a corrected manifest.
---

# Kubernetes Security Policy Review

Review a Kubernetes workload manifest against the **Pod Security Standards (Restricted profile)** and adjacent hardening controls. Anchor every finding to the actual YAML shown.

## Method

1. **Identify the workload(s).** Find the Pod template (`spec.template.spec` for controllers, or `spec` for a bare Pod) and each container/initContainer.
2. **Evaluate controls** using `reference/controls.md`. For each control mark PASS / FAIL / MISSING with the path (e.g. `spec.containers[0].securityContext.runAsNonRoot`). Absence of a field is usually a FAIL — defaults are insecure.
3. **Report findings**: table of Severity | Control | Path | Current | Required.
4. **Emit a corrected manifest** (or patch) applying the pod-level and container-level `securityContext`, resource limits, and any structural fixes.
5. **Recommend enforcement**: namespace Pod Security Admission labels and/or an admission policy engine — see `reference/controls.md`.

## Core controls (Restricted profile essentials)

Set at **pod level** (`spec.securityContext`) and/or **container level** (`spec.containers[*].securityContext`):

- `runAsNonRoot: true` and an explicit non-zero `runAsUser` / `runAsGroup`.
- `allowPrivilegeEscalation: false` (container level).
- `privileged: false` (never true).
- `capabilities.drop: ["ALL"]`; add back only specific caps if genuinely required (e.g. `NET_BIND_SERVICE`).
- `readOnlyRootFilesystem: true` (mount an `emptyDir` for writable paths).
- `seccompProfile.type: RuntimeDefault` (pod or container level).

Adjacent must-haves:

- **Resource requests AND limits** for cpu and memory on every container (prevents noisy-neighbor DoS and eviction surprises).
- **No host namespaces**: `hostNetwork`, `hostPID`, `hostIPC` all false/absent.
- **No `hostPath` volumes** (or tightly restricted, read-only if unavoidable).
- **No `hostPort`.**
- **Do not auto-mount the service account token** unless the workload calls the K8s API (`automountServiceAccountToken: false`).
- **Pinned image + digest**, never `:latest`; set `imagePullPolicy` appropriately.
- **Liveness & readiness probes** defined.
- Drop unneeded `NET_RAW`; avoid `sysctls` unless required.

## Output

Findings table + corrected manifest + enforcement recommendation. Do not fabricate cluster state, CVEs, or scanner output — recommend `kubectl`, `kube-score`, `kubeconform`, Trivy, Checkov, or Polaris for automated checks.

## References

- `reference/controls.md` — full control list with paths, why, and Pod Security Admission enforcement.
- `reference/example.md` — an insecure manifest and its hardened rewrite.
