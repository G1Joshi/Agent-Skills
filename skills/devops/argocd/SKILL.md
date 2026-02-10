---
name: argocd
description: ArgoCD GitOps continuous delivery for Kubernetes. Use for K8s GitOps.
---

# ArgoCD

ArgoCD is the industry standard for **GitOps**. It syncs the state of a Kubernetes cluster with a Git repository. 2025 features: **ApplicationSets** for multi-tenant management.

## When to Use

- **Kubernetes CD**: Continuous Delivery specifically for K8s.
- **GitOps**: You want your cluster state (YAML) versioned in Git.
- **Drift Detection**: ArgoCD alerts you if someone manually hacks `kubectl edit` in production.

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

### Application

The link between a Git source and a K8s destination.

### ApplicationSet

A generator that spawns multiple `Application` resources. Example: "Deploy _every_ folder in this repo as an app" or "Deploy this app to _every_ cluster".

### Sync Phases

Pre-Sync (Schema migration), Sync (Deployment), Post-Sync (Health check).

## Best Practices (2025)

**Do**:

- **Use ApplicationSets**: The modern way to manage many apps.
- **Separate Config from Code**: Keep app source code and K8s manifests in separate repos or at least separate folders.
- **Use "App of Apps"**: A bootstrap pattern where one root Argo app deploys all other apps.

**Don't**:

- **Don't manage Secrets in plain Git**: Use Sealed Secrets, External Secrets Operator, or ArgoCD Vault Plugin.

## References

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
