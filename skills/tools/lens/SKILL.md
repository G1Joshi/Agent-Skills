---
name: lens
description: Expert Lens (Kubernetes IDE) assistance covering cluster visualization, pod metrics, log viewing, helm release management, and RBAC auditing. Use when operating and troubleshooting Kubernetes clusters via GUI.
---

# Lens Desktop

Lens is an intuitive Kubernetes desktop IDE that simplifies cluster monitoring, pod troubleshooting, log inspection, and multi-cluster navigation.

## When to Use

- **Multi-Cluster Kubernetes Observability**: Visualizing nodes, pods, deployments, and CRDs across AWS EKS, Google GKE, Azure AKS, and local clusters.
- **Fast Troubleshooting & Container Exec**: Inspecting live container logs, resource utilization, and opening interactive terminal sessions inside pods.
- **Helm Release Lifecycle Management**: Deploying, customizing values, and rolling back Helm charts directly from a unified desktop interface.
- **RBAC & Security Audit**: Auditing ServiceAccounts, ClusterRoles, and RoleBindings across complex enterprise multi-tenant environments.

## Quick Start

```bash
# Add active kubeconfig context to Lens desktop application:
# File > Add Cluster > Select from local ~/.kube/config
```

## Core Concepts

### Unified Multi-Cluster Kubeconfig Management

Configuring Lens to track multiple cloud and on-premise clusters via aggregated kubeconfig:

```bash
# Merge multiple cloud kubeconfigs into a dedicated Lens catalog file
export KUBECONFIG=~/.kube/config:~/.kube/prod-eks.yaml:~/.kube/staging-gke.yaml
kubectl config view --flatten > ~/.kube/lens-clusters.yaml

# Set permissions and launch Lens with target kubeconfig
chmod 600 ~/.kube/lens-clusters.yaml
```

Lens cluster catalog entry in `~/.k8slens/clusters.json`:

```json
{
  "clusters": [
    {
      "id": "prod-us-east-1",
      "name": "Production EKS US-East",
      "kubeConfigPath": "~/.kube/lens-clusters.yaml",
      "contextName": "arn:aws:eks:us-east-1:123456789012:cluster/prod-us-east",
      "prometheus": {
        "type": "prometheus-operator",
        "service": "monitoring/prometheus-k8s:9090"
      }
    }
  ]
}
```

### Lens Metrics & Prometheus Operator Integration

Configuring Prometheus ServiceMonitor to feed live node and pod metrics into Lens:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: lens-metrics-collector
  namespace: monitoring
  labels:
    release: prometheus-stack
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: kube-state-metrics
  endpoints:
    - port: http-metrics
      interval: 15s
```

### Automated Pod Log Export & Shell Diagnostics

- Select pod in **Workloads -> Pods**.
- Click **Terminal** icon to spawn instant shell with injected environment:
  ```bash
  # Inside Lens pod shell: inspect process tree and open network sockets
  ps aux
  netstat -tuln
  curl -I http://localhost:8080/healthz
  ```

## Common Patterns

### Multi-Cluster Kubeconfig Management

**Problem**: Managing distinct credentials for dozens of Kubernetes clusters.  
**Solution**: Merge multiple cluster configs into a unified directory watched by Lens.

```bash
# Merge multiple kubeconfigs
export KUBECONFIG=~/.kube/config:~/.kube/prod-cluster.yaml:~/.kube/staging-cluster.yaml
kubectl config view --flatten > ~/.kube/all-clusters.yaml
# Add ~/.kube/all-clusters.yaml to Lens Catalog
```

## Best Practices

**Do**:

- Configure Prometheus metrics provider in cluster settings to enable CPU, Memory, and Network graphs.
- Use Lens Workspaces to categorize clusters by environment (Production, Staging, Ephemeral Dev).
- Audit RBAC permissions before granting team members cluster access; Lens inherits underlying kubeconfig privileges.
- Utilize the built-in Terminal with cluster context pre-set to run `kubectl` commands rapidly.

**Don't**:

- Leave production cluster connections active without MFA-backed IAM authenticator tokens.
- Edit production ConfigMaps or Deployments live in Lens UI without checking changes into Git (GitOps).
- Install unverified community extensions that require broad local file access.

## Troubleshooting

| Error                                | Cause                                                                   | Solution                                                                   |
| :----------------------------------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `Metrics not showing in Lens charts` | Prometheus not installed or Lens cluster metrics settings unconfigured. | Right-click cluster > Settings > Metrics > Select Prometheus provider.     |
| `Cluster state shows Disconnected`   | API server unreachable or certificate expired in kubeconfig.            | Refresh kubeconfig token via cloud CLI (e.g. `aws eks update-kubeconfig`). |
| `Lens CPU / Memory usage high`       | Monitoring multiple high-pod clusters simultaneously.                   | Close inactive cluster workspaces in Lens drawer.                          |

## References

- [Lens Documentation](https://docs.k8slens.dev/)
