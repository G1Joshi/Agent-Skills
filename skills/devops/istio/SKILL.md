---
name: istio
description: Expert Istio service mesh assistance covering VirtualServices, DestinationRules, mTLS policies, Envoy sidecars, and ingress gateways. Use when managing microservice networking, traffic splitting, and zero-trust security on Kubernetes.
---

# Istio

Istio is an open-source service mesh providing transparent traffic management, zero-trust security with mutual TLS, dynamic telemetry, and sidecarless Ambient Mesh architectures.

## When to Use

- **Enterprise Kubernetes Service Mesh**: Zero-trust mTLS encryption, traffic management, and telemetry across microservices.
- **Canary & Blue-Green Traffic Splitting**: Shifting percentage-based traffic smoothly using VirtualService and DestinationRule.
- **Fault Injection & Chaos Testing**: Injecting synthetic HTTP delays and abort errors to test microservice resilience.
- **Egress & Ingress Traffic Governance**: Restricting outbound network connections and securing inbound traffic via Istio Ingress Gateway.

## Quick Start

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
    - reviews
  http:
    - route:
        - destination:
            host: reviews
            subset: v1
          weight: 80
        - destination:
            host: reviews
            subset: v2
          weight: 20
```

## Core Concepts

### Traffic Shifting with VirtualService & DestinationRule

Implementing a 90/10 Canary release rollout:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: payment-service
  namespace: default
spec:
  host: payment-service
  subsets:
    - name: v1
      labels:
        version: "1.0"
    - name: v2
      labels:
        version: "2.0"
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    tls:
      mode: ISTIO_MUTUAL # Strict mTLS within mesh
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: payment-service
  namespace: default
spec:
  hosts:
    - payment-service
  http:
    - route:
        - destination:
            host: payment-service
            subset: v1
          weight: 90
        - destination:
            host: payment-service
            subset: v2
          weight: 10
      timeout: 3s
      retries:
        attempts: 3
        perTryTimeout: 1s
        retryOn: 5xx,connect-failure
```

### Strict Mutual TLS (mTLS) PeerAuthentication

Enforcing encryption for all inter-service pod communication:

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT # Rejects all non-mTLS plain-text connections
```

### Fault Injection for Resiliency Verification

Testing application tolerance against downstream latencies:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ratings-delay
spec:
  hosts:
    - ratings
  http:
    - fault:
        delay:
          percentage:
            value: 20.0
          fixedDelay: 5s
      route:
        - destination:
            host: ratings
```

## Common Patterns

### Circuit Breaking with Outlier Detection in DestinationRule

**Problem**: Slow or failing pod replicas drag down the response times of the entire service.

**Solution**:
Eject consecutive failing pods automatically:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: backend-circuit-breaker
spec:
  host: backend-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

## Best Practices

**Do**:

- Target Istio Ambient Mesh mode where available to eliminate sidecar container resource overhead.
- Configure `mode: STRICT` in `PeerAuthentication` to guarantee zero-trust mutual TLS encryption.
- Define explicit `timeout` and `retries` policies on all `VirtualService` routes to prevent cascading failures.
- Export metrics via the Istio Prometheus exporter for visualization in Kiali and Grafana.

**Don't**:

- Leave Egress open to wildcard internet access in sensitive environments; enforce strict `ServiceEntry` policies.
- Mix multiple conflicting `VirtualService` rules targeting the same host.
- Deploy sidecars into Kubernetes jobs or short-lived batch pods without proper termination handling.

## Troubleshooting

| Error                             | Cause                                                               | Solution                                                                               |
| :-------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------- |
| `503 Service Unavailable (UC/UF)` | Envoy proxy cannot reach upstream pod or connection reset.          | Check destination service endpoint health and verify subset labels match active pods.  |
| `mTLS Handshake Failed`           | Incompatible PeerAuthentication mode or expired client certificate. | Verify mesh TLS mode (PERMISSIVE vs STRICT) and confirm cert-manager or istiod health. |
| `High Sidecar Latency`            | CPU throttling on Envoy container during traffic spikes.            | Increase CPU limits in sidecar injection annotations and optimize connection pooling.  |

## References

- [Istio Documentation](https://istio.io/)
