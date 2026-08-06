# k8s-security-policy

A skill-first Claude Code plugin that reviews **Kubernetes manifests against the Pod Security Standards (Restricted profile)**.

## What it does
Auto-invokes on "kubernetes security", "securityContext", "pod security", or when a K8s workload manifest is shown. It checks `runAsNonRoot`, `readOnlyRootFilesystem`, dropped capabilities, no privilege escalation, seccomp, resource limits, and host-namespace/hostPath hygiene — then returns a findings table and a hardened manifest.

## Structure
- `skills/k8s-security-policy/SKILL.md` — review method + core controls.
- `skills/k8s-security-policy/reference/controls.md` — full control list with YAML paths, severity, and Pod Security Admission enforcement.
- `skills/k8s-security-policy/reference/example.md` — insecure manifest vs. hardened rewrite.

## Usage
Paste a Deployment/Pod/StatefulSet manifest and ask for a security review. The skill activates automatically.

## Note
Recommends `kube-score`, `kubeconform`, Trivy, Checkov, or Polaris for automated checks rather than fabricating scanner output.

## License
MIT © Matthews Wong
