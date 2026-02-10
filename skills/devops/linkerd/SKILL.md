---
name: linkerd
description: Linkerd lightweight service mesh. Use for service networking.
---

# Linkerd

Linkerd is a lightweight Service Mesh. It focuses on simplicity and performance (Rust-based proxies). v2.15 (2025) enables **Mesh Expansion** to VMs.

## When to Use

- **Low Overhead**: You want mTLS and Metrics but can't afford Istio's CPU tax.
- **Simplicity**: "It just works". No complex configuration for basic features.
- **Security**: Default-on mTLS and authorization policies.

## Core Concepts

### Micro-Proxy

Linkerd uses a specialized Rust proxy (not Envoy) that is tiny and fast.

### Viz Extension

A dashboard and Prometheus instance pre-configured to show mesh metrics (Success Rate, Latency).

### ServiceProfiles

Define retry logic and timeouts per route.

## Best Practices (2025)

**Do**:

- **Use HA Mode**: Run control plane in high-availability mode for production.
- **Automate Cert Rotation**: Use `cert-manager` to rotate the mTLS root CA automatically.
- **Expand to VMs**: Use the new 2.15 feature to include legacy databases in the mesh.

**Don't**:

- **Don't disable mTLS**: It's verified automatically. Keep it on.

## References

- [Linkerd Documentation](https://linkerd.io/docs/)
