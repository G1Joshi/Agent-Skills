---
name: rancher
description: Rancher Kubernetes management platform. Use for multi-cluster K8s.
---

# Rancher

Rancher is a complete software stack for teams adopting containers. It addresses the operational and security challenges of managing multiple Kubernetes clusters.

## When to Use

- **Multi-Cluster**: Manage EKS, AKS, GKE, and on-prem RKE2 clusters from a single pane of glass.
- **User Management**: Unified Auth (SSO) across all clusters.
- **Edge**: Manage thousands of small K3s clusters (retail/IoT).

## Core Concepts

### RKE2

Rancher's Government-grade Kubernetes distribution. Secure by default, FIPS compliant.

### Fleet

GitOps at scale. Deploy bundles of resources to 10,000 clusters simultaneously.

### Cluster Explorer

A rich UI for interacting with Kubernetes resources (CRDs, logs, shells) without needing `kubectl` setup locally.

## Best Practices (2025)

**Do**:

- **Use Fleet**: For managing deployments across many clusters. It's built into Rancher.
- **Use RKE2/K3s**: For the downstream clusters provided by Rancher.
- **Centralize Auth**: Hook Rancher up to your OIDC/AD provider once, and get RBAC across all clusters.

**Don't**:

- **Don't expose Rancher UI publicly**: It's the keys to the kingdom. Put it behind a VPN or strict Identity Aware Proxy.

## References

- [Rancher Documentation](https://ranchermanager.docs.rancher.com/)
