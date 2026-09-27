---
name: linkerd
description: Expert Linkerd service mesh assistance covering ultralight Rust micro-proxies, automatic mTLS, traffic splitting, and zero-config observability. Use when adding secure mTLS and latency metrics to Kubernetes with minimal overhead.
---

# Linkerd

Linkerd is a lightweight Service Mesh. It focuses on simplicity and performance (Rust-based proxies). v2.15 (2025) enables **Mesh Expansion** to VMs.

## When to Use

- **Ultralight Kubernetes Service Mesh**: High-performance, zero-config microservice mesh written in Rust and Go.
- **Automatic Transparent Mutual TLS (mTLS)**: Instant cryptographically verified encryption between pods without code changes.
- **Golden Metrics Collection**: Automated latency, traffic volume, and failure rate metrics exposed to Prometheus.
- **Traffic Splitting & Progressive Delivery**: Canary and blue-green deployments via the Service Mesh Interface (SMI) specification.

## Quick Start

```bash
# Install Linkerd CLI and check cluster compatibility
curl -fsL https://run.linkerd.io/install | sh
linkerd check --pre

# Install Linkerd control plane into Kubernetes
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd check

# Inject Linkerd sidecar into an existing namespace
kubectl get deploy -n my-app -o yaml | linkerd inject - | kubectl apply -f -
```

## Core Concepts

#Automatic Proxy Injection Annotation

Injecting micro-proxies into deployment pods via annotations:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: default
  annotations:
    linkerd.io/inject: enabled # Linkerd proxy automatically injected
spec:
  replicas: 2
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
        - name: app
          image: myregistry/user-service:v1.0
          ports:
            - containerPort: 8080
```

#TrafficSplit for Canary Deployment

Routing canary traffic across distinct service versions:

```yaml
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: user-service-split
  namespace: default
spec:
  service: user-service
  backends:
    - service: user-service-v1
      weight: 800m # 80% traffic
    - service: user-service-v2
      weight: 200m # 20% traffic
```

#Linkerd CLI Diagnostic & Telemetry Inspection

Inspecting real-time traffic statistics between pods:

```bash
# Check Linkerd control plane health
linkerd check

# Real-time traffic inspection (Golden Metrics: RPS, Success Rate, Latency P99)
linkerd viz stat deployment -n default

# Trace live traffic calls between services
linkerd viz tap deployment/user-service -n default --to deployment/db-service
```

## Common Patterns

### TrafficSplit for Canary Deployment

**Problem**: Releasing new microservice versions without the risk of impacting 100% of user traffic.

**Solution**:
Use the SMI TrafficSplit custom resource:

```yaml
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: service-canary-split
  namespace: prod
spec:
  service: my-service
  backends:
    - service: my-service-v1
      weight: 900
    - service: my-service-v2
      weight: 100
```

## Best Practices (2026)

- **Do** prefer Linkerd over heavier service meshes when simplicity, low memory (< 30MB/proxy), and ultra-low latency are paramount.
- **Do** run `linkerd check` in CI and post-deployment validation scripts.
- **Do** monitor the expiry of Linkerd identity issuer certificates using automated alerts or Cert-Manager.
- **Do** use `linkerd viz tap` for live, real-time debugging of failing requests between pods.
- **Don't** inject the Linkerd proxy into Kubernetes batch jobs without configuring automated sidecar shutdown.
- **Don't** disable mTLS verification; Linkerd enables transparent mTLS out of the box with zero configuration.
- **Don't** bypass readiness probes; Linkerd relies on pod health to route mesh traffic.

## Troubleshooting

| Error                                               | Cause                                                               | Solution                                                                  |
| :-------------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------ |
| `linkerd check: failed to connect to control plane` | `linkerd-controller` pod not running or admission webhook unready.  | Run `kubectl get pods -n linkerd` and verify cluster certificates.        |
| `linkerd-proxy: connection refused to 127.0.0.1`    | Application container within pod hasn't finished binding port.      | Configure readiness probe on application container.                       |
| `Certificates expiring soon warning`                | Linkerd internal trust anchor or issuer certificate nearing expiry. | Rotate certificates: `linkerd upgrade --identity-trust-anchors-file ...`. |

## References

- [Linkerd Documentation](https://linkerd.io/docs/)
