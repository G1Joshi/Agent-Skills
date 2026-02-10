---
name: podman
description: Podman daemonless container engine. Use for rootless containers.
---

# Podman

Podman is a daemonless container engine for developing, managing, and running OCI Containers. It is a drop-in replacement for Docker (`alias docker=podman`). Podman v5 (2025) features a rewritten hypervisor support for Mac/Windows.

## When to Use

- **Security**: Rootless containers by default. No central daemon running as root.
- **HPC / Restricted Env**: Run containers on systems where you don't have root access.
- **Kubernetes**: Generating K8s YAML from running containers (`podman kube generate`).

## Quick Start

```bash
# Run a container (Rootless)
podman run -dt -p 8080:80 nginx

# Generate K8s YAML
podman kube generate my-container > pod.yaml

# Run K8s YAML locally
podman kube play pod.yaml
```

## Core Concepts

### Daemonless

Fork/Exec model. The parent process is the user shell, not a `dockerd` daemon. If Podman crashes, it doesn't take down your containers (usually).

### Pods

Podman can manage "Pods" (groups of containers sharing network namespace) locally, mimicking K8s Pods.

### Quadlet

Systemd integration. Run containers as systemd services effortlessly.

## Best Practices (2025)

**Do**:

- **Use `podman-desktop`**: A GUI alternative to Docker Desktop.
- **Use Rootless**: This is the main selling point. Stick to it to improve security posture.
- **Use `podman kube play`**: Test your K8s manifests locally without a full Minikube cluster.

**Don't**:

- **Don't mount Docker socket**: It doesn't exist. Use the Podman socket if you need tools to talk to the engine, but be aware of API differences.

## References

- [Podman Documentation](https://podman.io/)
