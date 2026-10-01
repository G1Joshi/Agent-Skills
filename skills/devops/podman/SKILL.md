---
name: podman
description: Expert Podman container engine assistance covering rootless containers, podman-compose, pod generation (Kubernetes YAML), and systemd integration. Use when managing secure, daemonless OCI containers on Linux.
---

# Podman

Podman is a daemonless, rootless container engine for developing, running, and managing OCI containers and pods, functioning as a secure drop-in alternative to Docker.

## When to Use

- **Rootless & Daemonless Containerization**: Running OCI containers without requiring root privileges or background daemons.
- **Drop-in Docker CLI Replacement**: 100% command-line compatible alias (`alias docker=podman`) with enhanced security.
- **Podman Pods for Kubernetes Prototyping**: Grouping containers into shared network pods locally before deploying to Kubernetes.
- **Systemd Integration via Quadlets**: Running production containers managed natively by Linux `systemd` service managers.

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

### Rootless Pod Architecture & Container Execution

Running containers without root privileges or central daemons:

```bash
# Run rootless container using user namespace mapping
podman run -d \
  --name web-app \
  -p 8080:8080 \
  --userns=keep-id \
  --security-opt no-new-privileges \
  registry.example.com/app:v1.0

# Group containers into a shared-namespace Pod (mirrors Kubernetes Pod)
podman pod create --name microservice-pod -p 3000:3000
podman run -d --pod microservice-pod --name api-service my-api:latest
podman run -d --pod microservice-pod --name redis-cache redis:alpine
```

### Systemd Integration with Podman Quadlets

Managing containers as native systemd services:

```ini
# ~/.config/containers/systemd/api-service.container
[Unit]
Description=Production API Microservice
After=network-online.target

[Container]
Image=registry.example.com/api-service:v2.1.0
ContainerName=api-service
PublishPort=8080:8080
Environment=NODE_ENV=production
UserNS=auto

[Service]
Restart=always

[Install]
WantedBy=default.target
```

```bash
# Reload systemd to generate service and start container
systemctl --user daemon-reload
systemctl --user start api-service
```

### Exporting Pods to Kubernetes YAML

Generating native Kubernetes manifests directly from local Podman pods:

```bash
# Generate Kubernetes Deployment and Service YAML
podman generate kube microservice-pod > k8s-deployment.yaml
```

## Common Patterns

### Generate Systemd Service for Rootless Container Autostart

**Problem**: Containers on bare-metal servers must start automatically on host boot without Docker daemon.

**Solution**:
Use Podman Quadlet or systemd service generation:

```bash
# Run rootless container
podman run -d --name web-api -p 8080:8080 myorg/api:latest

# Generate systemd unit file
podman generate systemd --new --name web-api > ~/.config/systemd/user/container-web-api.service

# Enable user systemd service to start on boot
systemctl --user enable --now container-web-api.service
loginctl enable-linger $USER
```

## Best Practices

**Do**:

- Run containers rootless (`--userns=keep-id`) to neutralize container breakout risks.
- Manage production containers on Linux servers using Podman Quadlets (`.container` systemd files).
- Use `podman generate kube` to prototype Kubernetes pod manifests locally.
- Configure `registries.conf` with explicit, secure container registry search paths.

**Don't**:

- Run containers with `--privileged` unless strictly managing bare-metal kernel hardware.
- Assume ports < 1024 are accessible rootless; use ports >= 1024 (e.g. 8080, 8443) or adjust sysctl.
- Leave orphaned storage layers; clean up periodically with `podman system prune`.

## Troubleshooting

| Error                                                    | Cause                                                        | Solution                                                                                       |
| :------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| `Error: rootless users cannot bind to ports < 1024`      | Linux non-privileged port binding restriction.               | Run on port >1024 (e.g. 8080) or set `sysctl net.ipv4.ip_unprivileged_port_start=80`.          |
| `Error: short-name "..." did not expand to any registry` | Podman requires fully qualified registry domains by default. | Use `docker.io/library/nginx:latest` or configure `registries.conf`.                           |
| `Subuid/subgid range missing for user`                   | User lacks subuid mappings for rootless namespaces.          | Add entry in `/etc/subuid` and `/etc/subgid` with `usermod --add-subuids 100000-165535 $USER`. |

## References

- [Podman Documentation](https://podman.io/)
