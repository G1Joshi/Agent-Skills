---
name: traefik
description: Traefik cloud-native reverse proxy. Use for container networking.
---

# Traefik

Traefik is a modern reverse proxy that auto-discovers services. v3.0 (2025) supports **Wasm Plugins** and the **Kubernetes Gateway API**.

## When to Use

- **Docker/K8s**: It watches the Docker socket or K8s API and reconfigures itself automatically. No config file edits needed for new services.
- **Ease of Use**: Automatic Let's Encrypt (ACME) integration is best-in-class.
- **Middleware**: Built-in auth (Basic, ForwardAuth), rate limiting, and circuit breakers.

## Quick Start (Docker Compose)

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.my-app.rule=Host(`example.com`)"
  - "traefik.http.routers.my-app.entrypoints=websecure"
  - "traefik.http.routers.my-app.tls.certresolver=myresolver"
```

## Core Concepts

### Providers

Sources of configuration (Docker, Kubernetes, File, Consul).

### EntryPoints

Network ports (80, 443).

### Routers

Connect requests to Services based on Rules (Host, Path).

### Middleware

Modify requests (StripPrefix, Compress, Auth).

## Best Practices (2025)

**Do**:

- **Use v3 syntax**: Adhere to the structure of `routers` and `services`.
- **Use Dashboard**: The web UI is great for debugging routing issues.
- **Use Let's Encrypt**: TLS challenge handling is seamless.

**Don't**:

- **Don't expose Dashboard publicly**: It reveals infrastructure details. Secure it with middleware.

## References

- [Traefik Documentation](https://doc.traefik.io/traefik/)
