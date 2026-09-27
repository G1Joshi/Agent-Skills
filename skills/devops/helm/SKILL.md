---
name: helm
description: Expert Helm Kubernetes package manager assistance covering charts, values.yaml, Go templates, release rollbacks, and dependencies. Use when packaging and deploying Kubernetes applications.
---

# Helm

Helm helps you manage Kubernetes applications via Charts (packages of pre-configured K8s resources). Helm v4 (2025) improves OCI integration and enables server-side apply.

## When to Use

- **Kubernetes Package Management**: Packaging, templating, versioning, and deploying complex Kubernetes applications.
- **Multi-Environment Value Overrides**: Reusing a single chart across dev, staging, and production with distinct `values.yaml` files.
- **Third-Party Open-Source Deployment**: Installing community software (Cert-Manager, Ingress-Nginx, Prometheus) via Helm Repos.
- **Release Lifecycle & Rollbacks**: Upgrading, tracking release revisions, and executing automated rollbacks via `helm rollback`.

## Quick Start

```bash
# Install a chart
helm install my-release oci://registry-1.docker.io/bitnamicharts/nginx

# Create a chart
helm create my-chart
```

```yaml
# values.yaml
replicaCount: 2
image:
  repository: nginx
  tag: "1.25"
```

## Core Concepts

#Parameterized Deployment Template

Templating Kubernetes resources with Helm helpers:

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.port }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

#Values Schema Validation (values.schema.json)

Enforcing strict type checking on user-provided values:

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "properties": {
    "replicaCount": {
      "type": "integer",
      "minimum": 1
    },
    "image": {
      "type": "object",
      "required": ["repository"],
      "properties": {
        "repository": { "type": "string" },
        "tag": { "type": "string" }
      }
    }
  },
  "required": ["replicaCount", "image"]
}
```

#Helm CLI Deployment & Rollback Commands

Deploying, linting, and managing releases:

```bash
# Lint chart templates for errors
helm lint ./mychart

# Dry run deployment with template rendering
helm install my-release ./mychart --dry-run --debug

# Upgrade with atomic rollback if health checks fail
helm upgrade --install my-release ./mychart \
  --namespace production \
  --create-namespace \
  --values values-production.yaml \
  --atomic \
  --timeout 5m

# Roll back to previous revision if needed
helm rollback my-release 1 --namespace production
```

## Common Patterns

### Parameterized Values Template with Default Fallback

**Problem**: Hardcoding replica counts and container images in raw Kubernetes YAML.

**Solution**:
Use Helm Go templates with values defaults:

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
spec:
  replicas: {{ .Values.replicaCount | default 2 }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
        - name: app
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          ports:
            - containerPort: {{ .Values.service.port | default 8080 }}
```

## Best Practices (2026)

- **Do** always use `--atomic` and `--timeout` during `helm upgrade` to ensure automatic rollback on deployment failure.
- **Do** author a `values.schema.json` to catch configuration errors before reaching the Kubernetes API server.
- **Do** define helper templates in `_helpers.tpl` for standard label generation and naming conventions.
- **Do** store Helm charts in OCI-compliant container registries (GHCR, ECR, Artifact Registry) via `helm push`.
- **Don't** hardcode sensitive passwords in `values.yaml`; inject secrets via external secret managers.
- **Don't** use `helm template` and `kubectl apply` without validating that CRDs and hooks are handled appropriately.
- **Don't** deploy charts without setting explicit resource requests and limits in default values.

## Troubleshooting

| Error                                                                                | Cause                                                                    | Solution                                                                       |
| :----------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `Error: UPGRADE FAILED: another operation (install/upgrade/rollback) is in progress` | Previous Helm operation interrupted leaving release secret locked.       | Rollback release or manually unlock release secret: `helm rollback <release>`. |
| `Error: execution error at (templates/deployment.yaml:10:15): nil pointer`           | Accessing non-existent key in `.Values` without default check.           | Verify key exists in `values.yaml` or use `default` function.                  |
| `Error: rendered manifests contain a resource that already exists`                   | Attempting to adopt an existing Kubernetes resource not tracked by Helm. | Add annotations: `meta.helm.sh/release-name: <name>` or delete resource.       |

## References

- [Helm Documentation](https://helm.sh/)
