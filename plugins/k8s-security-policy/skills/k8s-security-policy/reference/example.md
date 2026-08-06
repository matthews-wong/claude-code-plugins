# Example: Insecure → Hardened Deployment

## Before (multiple Restricted-profile violations)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 2
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: web
          image: mycorp/web:latest          # unpinned
          ports:
            - containerPort: 8080
          # no securityContext, no resources, no probes
```

Findings: `:latest` image (Med), no `runAsNonRoot`/root by default (High), no `allowPrivilegeEscalation:false` (High), caps not dropped (High), writable root FS (Med), no seccomp (Med), no resource limits (Med), no probes (Low), SA token auto-mounted (Med).

## After (Restricted-compliant)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 2
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: web
          image: mycorp/web:1.4.2@sha256:REPLACE_WITH_REAL_DIGEST
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          securityContext:
            allowPrivilegeEscalation: false
            privileged: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits:   { cpu: "500m", memory: "256Mi" }
          livenessProbe:
            httpGet: { path: /healthz, port: 8080 }
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet: { path: /readyz, port: 8080 }
            initialDelaySeconds: 5
            periodSeconds: 10
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

Note the `emptyDir` at `/tmp` — required once `readOnlyRootFilesystem: true` is set, since most apps need a writable temp dir. Add further `emptyDir` mounts for any other paths the app writes to.
