---
name: rancher
description: Expert SUSE Rancher assistance covering multi-cluster Kubernetes management, RKE2/K3s, Fleet GitOps, and cluster security policies. Use when administering enterprise multi-cloud Kubernetes clusters.
---

# Rancher

Rancher is a complete software stack for teams adopting containers. It addresses the operational and security challenges of managing multiple Kubernetes clusters.

## When to Use

- **Enterprise Multi-Cluster Kubernetes Management**: Centralized management of EKS, GKE, AKS, and bare-metal RKE2 clusters.
- **Unified RBAC & Global Authentication**: Mapping enterprise Okta/Active Directory groups to Kubernetes RBAC across all clusters.
- **Fleet GitOps Deployment**: Continuous delivery of Kubernetes configurations across thousands of geographically distributed clusters.
- **Cluster Security & CIS Benchmarks**: Running scheduled automated security audits and compliance scans.

## Quick Start

```bash
# Run Rancher server locally with Docker
docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged \
  rancher/rancher:latest

# Access Rancher management console at https://localhost
```

## Core Concepts

#Fleet GitOps Multi-Cluster Deployment (fleet.yaml)

Distributing workloads to targeted clusters based on labels:

```yaml
# fleet.yaml in Git repository root
defaultNamespace: production

labels:
  app: payment-gateway

# Target clusters matching specific environment labels
targetCustomizations:
  - name: production-clusters
    clusterSelector:
      matchLabels:
        env: production
        region: us-east
    helm:
      values:
        replicaCount: 5
        ingress:
          enabled: true
          host: payment.us-east.example.com

  - name: staging-clusters
    clusterSelector:
      matchLabels:
        env: staging
    helm:
      values:
        replicaCount: 2
        ingress:
          enabled: true
          host: payment.staging.example.com
```

#RKE2 Secure Cluster Node Provisioning

Configuring hardened Kubernetes control-plane node:

```yaml
# /etc/rancher/rke2/config.yaml
write-kubeconfig-mode: "0600"
tls-san:
  - "k8s-api.company.internal"
  - "10.0.1.10"
cni: "cilium" # Modern eBPF network plugin
profile: "cis-1.23" # Enforce CIS benchmark profile
```

#Rancher CLI Operations

Switching cluster contexts and managing projects:

```bash
# Log in to Rancher Management Server
rancher login https://rancher.infra.internal --token "$RANCHER_TOKEN"

# Switch active context to specific downstream cluster
rancher context switch

# Inspect running cluster nodes and health
rancher nodes
```

## Common Patterns

### Fleet GitOps Multi-Cluster Continuous Delivery

**Problem**: Applying identical baseline monitoring, ingress, and security policies across 50+ Kubernetes clusters.

**Solution**:
Define Fleet deployment bundle (`fleet.yaml`):

```yaml
defaultNamespace: cattle-monitoring-system
helm:
  releaseName: monitoring-agent
  chart: monitoring-chart
  repo: https://charts.example.com
targets:
  - clusterGroup: production-clusters
  - clusterSelector:
      matchLabels:
        env: prod
```

## Best Practices (2026)

- **Do** deploy RKE2 (Rancher Government / hardened Kubernetes) for enterprise production environments.
- **Do** use Fleet GitOps to manage multi-cluster deployments centrally from version-controlled Git repos.
- **Do** enforce unified RBAC by integrating Rancher with enterprise identity providers (SAML, Okta, Azure AD).
- **Do** run scheduled Rancher CIS benchmark scans to verify cluster compliance.
- **Don't** run production workloads directly on the Rancher management controller cluster; manage downstream clusters.
- **Don't** grant global `Administrator` privileges; scope permissions using Rancher Projects and Roles.
- **Don't** bypass network policies between multi-tenant projects sharing the same physical cluster.

## Troubleshooting

| Error                                              | Cause                                                                   | Solution                                                             |
| :------------------------------------------------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------- |
| `Cluster agent disconnected / Cluster unavailable` | Downstream cluster lost network route to Rancher management server URL. | Verify Rancher server URL under Global Settings > Server URL.        |
| `Failed to install system-upgrade-controller`      | RKE2/K3s cluster upgrade job blocked by node drainage timeout.          | Inspect node pods and force eviction on non-essential workloads.     |
| `Certificate expired in Rancher ingress`           | Rancher self-signed or cert-manager SSL certificate expired.            | Rotate certificates using `rancher-cleanup` or cert-manager renewal. |

## References

- [Rancher Documentation](https://ranchermanager.docs.rancher.com/)
