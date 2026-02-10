---
name: kubernetes
description: Kubernetes container orchestration with Helm, operators, and service mesh. Use for cluster management.
---

# Kubernetes (K8s)

Kubernetes is the standard for orchestrating containerized applications. In 2025, the **Gateway API** has replaced Ingress as the standard for traffic routing, and **Sidecars** are native.

## When to Use

- **Scale**: You have hundreds of microservices.
- **Resilience**: You need self-healing, auto-restart, and multi-zone availability.
- **Platform Building**: You are building an internal platform (IDP) for developers.

## Quick Start (Gateway API)

```yaml
# Gateway (The Load Balancer)
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
spec:
  gatewayClassName: nginx
  listeners:
    - name: http
      protocol: HTTP
      port: 80

---
# HTTPRoute (The Routing Rule)
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
spec:
  parentRefs:
    - name: my-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: my-service
          port: 8080
```

## Core Concepts

### Control Plane

API Server, etcd, Scheduler. The brain of the cluster.

### Gateway API

The successor to Ingress. Split roles between **Infrastructure Provider** (GatewayClass), **Cluster Operator** (Gateway), and **Developer** (HTTPRoute/GRPCRoute).

### Custom Resource Definitions (CRDs)

Extend K8s API. Used by Operators (e.g., Prometheus Operator, Postgres Operator) to manage complex stateful apps.

## Best Practices (2025)

**Do**:

- **Use Gateway API**: Stop writing new `Ingress` resources.
- **Use GitOps**: ArgoCD or Flux to manage cluster state.
- **Set Requests/Limits**: The scheduler needs them to bin-pack nodes efficiently.
- **Use Native Sidecars**: K8s 1.29+ supports `restartPolicy: Always` for init containers, making sidecars first-class.

**Don't**:

- **Don't use `latest` tag**: Always pin image versions (SHA or specific tag) for reproducibility.

## References

- [Kubernetes Documentation](https://kubernetes.io/)
