---
name: service-mesh
description: Service mesh for microservices networking. Use for service-to-service.
---

# Service Mesh

A Service Mesh is a dedicated infrastructure layer for handling service-to-service communication. It's usually implemented as lightweight network proxies (Sidecars) deployed alongside the application code.

## When to Use

- **Mature Microservices**: You have 20+ services and managing retries, timeouts, and auth in each language is becoming a nightmare.
- **Zero Trust Security**: You need mTLS (Mutual TLS) between all services.
- **Observability**: You need uniform metrics (Gold signals) and tracing across a polyglot stack.

## Core Concepts

### Sidecar Proxy

The mesh injects a proxy (e.g., Envoy) next to your app container. Your app talks to localhost, the proxy handles the network magic.

### Control Plane

The brain that configures the proxies (e.g., Istio Control Plane).

### Data Plane

The set of proxies that actually route the traffic.

## Features

- **Traffic Management**: Canary deployments (1% traffic to v2), Circuit Breaking, Retries.
- **Security**: mTLS rotation, Authorization policies.
- **Observability**: Automatic metrics (latency, success rate) without code changes.

## Best Practices

**Do**:

- Assess if the **Complexity** is worth it. For small clusters, it's overkill.
- Use simpler alternatives (Linkerd) if Istio is too heavy.
- Start with **Observability** features before enabling strict enforcement/mTLS.

**Don't**:

- Don't use a Service Mesh to fix bad application code.
- Don't ignore the resource overhead (CPU/RAM) of sidecars at scale.

## References

- [Istio](https://istio.io/)
- [Linkerd](https://linkerd.io/)
- [The Service Mesh Pattern](https://servicemesh.io/)
