---
name: argocd
description: Expert Argo CD GitOps assistance covering Application CRDs, sync policies, automated self-healing, Helm/Kustomize, and multi-cluster deployments. Use when managing Kubernetes deployments via GitOps.
---

# ArgoCD

Argo CD is a declarative GitOps continuous delivery tool for Kubernetes, continuously reconciling active cluster state against Git repositories using ApplicationSets.

## When to Use

- **GitOps Continuous Delivery for Kubernetes**: Declarative synchronization of Kubernetes manifests from Git to live clusters.
- **Multi-Cluster Deployment Management**: Centrally deploying and managing workloads across dozens of Kubernetes clusters.
- **Automated Drift Detection & Self-Healing**: Automatically detecting manual cluster mutations and reconciling desired state.
- **Progressive Delivery with Argo Rollouts**: Coordinating Canary and Blue-Green deployments with automated rollbacks.

## Quick Start

```yaml
# Application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
```

## Core Concepts

### Declarative Application CRD

Defining GitOps synchronization between a Git repository and cluster namespace:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/org/payment-manifests.git
    targetRevision: main
    path: environments/production
    helm:
      valueFiles:
        - values.yaml
        - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: payments
  syncPolicy:
    automated:
      prune: true # Delete removed resources
      selfHeal: true # Revert out-of-band cluster edits
    syncOptions:
      - CreateNamespace=true
      - ApplyOutOfSyncOnly=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### App-of-Apps Pattern for Fleet Orchestration

Root application orchestrating multiple microservices:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-cluster-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-fleet.git
    targetRevision: main
    path: apps/production
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Argo CD CLI Management

Syncing and monitoring deployments via the terminal:

```bash
# Log in to Argo CD server
argocd login cd.infra.internal --grpc-web --sso

# Manually trigger synchronization and wait for health check
argocd app sync payment-service-prod --prune
argocd app wait payment-service-prod --health --timeout 300
```

## Common Patterns

### Declarative Argo CD Application Manifest

**Problem**: Manually creating Argo CD applications in the web UI makes disaster recovery difficult.

**Solution**:
Commit declarative Application custom resources directly to Git:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: "https://github.com/myorg/gitops-infra.git"
    targetRevision: main
    path: apps/payment-service/overlays/production
  destination:
    server: "https://kubernetes.default.svc"
    namespace: payments
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Best Practices

**Do**:

- Enable `selfHeal: true` and `prune: true` to guarantee Git remains the single source of truth.
- Adopt the App-of-Apps or ApplicationSet pattern to manage cluster applications hierarchically.
- Pin production `targetRevision` to explicit Git commit SHAs or release tags rather than floating branch names.
- Protect secrets using external secret operators (Sealed Secrets, External Secrets Operator + Vault) rather than plain Git.

**Don't**:

- Allow direct `kubectl edit` in production clusters; enforce changes exclusively via Git pull requests.
- Run Argo CD without RBAC and SSO integration (GitHub, Okta, or Keycloak).
- Omit `ApplyOutOfSyncOnly=true` in large clusters; it prevents API server overload during reconcile loops.

## Troubleshooting

| Error                                                            | Cause                                                                   | Solution                                                       |
| :--------------------------------------------------------------- | :---------------------------------------------------------------------- | :------------------------------------------------------------- |
| `ComparisonError: repository not found or authentication failed` | Git repository credentials missing or expired SSH key in Argo CD.       | Add repository credentials in Argo CD Settings > Repositories. |
| `OutOfSync: Resource failed validation`                          | Kubernetes manifest contains deprecated apiVersion or invalid schema.   | Run `kubectl apply --dry-run=client` locally on the manifest.  |
| `Degraded: CrashLoopBackOff on child pod`                        | Application container crashing due to missing env var or port conflict. | Inspect pod logs via `kubectl logs -n <ns> <pod-name>`.        |

## References

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
