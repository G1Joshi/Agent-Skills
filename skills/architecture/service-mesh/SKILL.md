---
name: service-mesh
description: Expert Service Mesh architecture assistance covering Istio, Linkerd, mTLS, and sidecar proxying. Use when configuring service-to-service communication, canary deployments, or zero-trust networking.
---

# Service Mesh

A Service Mesh is a dedicated infrastructure layer for handling service-to-service communication in distributed microservices. It is typically implemented using lightweight network sidecar proxies (such as Envoy) deployed alongside application containers, managed by a centralized control plane.

## When to Use

- **Zero-Trust Microservice Security**: Enforcing mutual TLS (mTLS) encryption and cryptographic workload identity (SPIFFE) across all pods.
- **Fine-Grained Traffic Management**: Implementing canary deployments, percentage-based splits, and circuit breakers at the network layer.
- **Uniform Observability**: Generating standardized golden signal metrics (latency, traffic, errors, saturation) across polyglot microservices.
- **Fault Injection & Chaos Engineering**: Simulating network latency, connection resets, and 500 errors to test system resilience.

## Quick Start

```yaml
# Canary deployment routing 90% traffic to v1, 10% to v2
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service-route
spec:
  hosts:
    - user-service
  http:
    - route:
        - destination:
            host: user-service
            subset: v1
          weight: 90
        - destination:
            host: user-service
            subset: v2
          weight: 10
```

## Core Concepts

### Sidecar Proxy Architecture (Envoy)

A lightweight network proxy intercepts all inbound and outbound pod network traffic transparently:

```text
[ Pod: Billing ]
  [ App Container: port 8080 ] ──localhost──→ [ Envoy Sidecar Proxy ]
                                                       │ (Encrypted mTLS)
                                                       ▼
[ Pod: Orders ]
  [ App Container: port 3000 ] ←──localhost── [ Envoy Sidecar Proxy ]
```

### Mutual TLS (mTLS) & Workload Identity

Authenticates both client and server cryptographically without application-layer code changes:

```yaml
# Istio PeerAuthentication resource
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT # Enforces mTLS across all microservice communication
```

### Canary Traffic Splitting (VirtualService)

Directs traffic dynamically based on weights or request headers:

```yaml
# Istio VirtualService Canary Routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service-routing
spec:
  hosts:
    - payment-svc
  http:
    - route:
        - destination:
            host: payment-svc
            subset: v1
          weight: 90
        - destination:
            host: payment-svc
            subset: v2-canary
          weight: 10
```

## Common Patterns

### Zero-Trust mTLS Enforcement

**Problem**: Cleartext HTTP between internal pods exposes sensitive data to lateral attacks inside a Kubernetes cluster.

**Solution**:
Enforce strict mutual TLS across the service mesh namespace:

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: prod-services
spec:
  mtls:
    mode: STRICT
```

## Best Practices

**Do**:

- Adopt Ambient / Sidecarless Meshes: Evaluate Istio Ambient or Cilium Service Mesh to reduce sidecar memory and CPU overhead.
- Enforce STRICT mTLS: Ensure plain unencrypted traffic cannot traverse internal Kubernetes node networks.
- Implement Network Egress Policies: Restrict which external internet domains pods are permitted to reach.
- Monitor Envoy Proxy Resource Usage: Size sidecar CPU and memory limits to prevent out-of-memory proxy crashes.

**Don't**:

- Deploy a service mesh for simple 3-service clusters: Service meshes add substantial operational complexity; adopt only when scale warrants it.
- Duplicate application-layer retries with mesh retries: Cascading retries cause rapid request storms and amplify outages.
- Ignore mesh control plane upgrades: Keep Istio/Linkerd control planes updated to prevent certificate rotation failures.

## Troubleshooting

| Error                             | Cause                                                               | Solution                                                                               |
| :-------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------- |
| `503 Service Unavailable (UC/UF)` | Sidecar proxy cannot reach upstream pod or connection reset.        | Check destination service endpoint health and verify subset labels match active pods.  |
| `mTLS Handshake Failed`           | Incompatible PeerAuthentication mode or expired client certificate. | Verify mesh TLS mode (PERMISSIVE vs STRICT) and confirm cert-manager or istiod health. |
| `High Sidecar Latency`            | CPU throttling on Envoy container during traffic spikes.            | Increase CPU limits in sidecar injection annotations and optimize connection pooling.  |

## References

- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/2/overview/)
- [Envoy Proxy Architecture](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/arch_overview)
