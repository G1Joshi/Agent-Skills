---
name: docker-desktop
description: Expert Docker Desktop assistance covering container resource allocation, Docker Compose, Kubernetes, Extensions, and VirtioFS. Use when configuring and troubleshooting local developer container environments.
---

# Docker Desktop

Docker Desktop provides the GUI, Kubernetes cluster, and extensions for Docker. 2025 features improved **Resource Saver** mode and **AI Extensions**.

## When to Use

- **Local Containerized Development on macOS & Windows**: Running Docker and Kubernetes with native OS filesystem optimizations.
- **VirtioFS & Rosetta 2 Virtualization (Apple Silicon)**: Fast cross-platform x86_64 emulation and high-speed disk sharing on macOS.
- **Single-Node Local Kubernetes**: One-click local Kubernetes cluster for testing manifests and Helm charts.
- **Docker Extensions & Resource Allocation**: Monitoring container CPU, memory, and disk usage visually.

## Quick Start

```bash
# Check Docker Desktop daemon and engine version
docker version

# Test container runtime
docker run --rm hello-world

# Inspect allocated CPU, memory, and disk resources
docker info
```

## Core Concepts

#VirtioFS & Resource Tuning Configuration

Optimizing disk performance in `settings.json`:

```json
{
  "cpus": 6,
  "memoryMiB": 12288,
  "swapMiB": 2048,
  "diskSizeMiB": 102400,
  "filesharingImplementation": "virtiofs",
  "useVirtualizationFramework": true,
  "useWindowsContainers": false,
  "kubernetes": {
    "enabled": true,
    "showSystemContainers": false
  }
}
```

#Local Multi-Container Development Workflow

Orchestrating services with port publishing and health checks:

```bash
# Check Docker engine version and virtualization driver
docker version

# Inspect resource consumption across local containers
docker stats --no-stream

# Clean up build caches and dangling volumes to reclaim disk
docker system prune -a --volumes
```

#Enabling Single-Node Kubernetes

Testing Kubernetes manifests locally:

```bash
# Switch kubectl context to Docker Desktop cluster
kubectl config use-context docker-desktop

# Verify local cluster nodes
kubectl get nodes
```

## Common Patterns

### Docker Compose Multi-Container Development Stack

**Problem**: Coordinating app, database, and cache containers locally with volume mounts.

**Solution**:
Define unified `docker-compose.yml`:

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    volumes:
      - ./src:/app/src
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## Best Practices (2026)

- **Do** enable VirtioFS on macOS for up to 10x faster file-syncing in bind-mounted development directories.
- **Do** enable Rosetta 2 emulation on Apple Silicon to run x86_64 images with near-native performance.
- **Do** configure explicit memory and CPU limits in Docker Desktop settings to prevent starving host applications.
- **Do** run `docker system prune --volumes` periodically to reclaim gigabytes of orphaned build cache.
- **Don't** allocate 100% of host RAM to the Docker VM; leave at least 4GB-8GB for the host OS.
- **Don't** use Docker Desktop in production server environments; deploy native Docker Engine or containerd on Linux.
- **Don't** store persistent production data inside local Docker Desktop volumes.

## Troubleshooting

| Error                                        | Cause                                                               | Solution                                                                    |
| :------------------------------------------- | :------------------------------------------------------------------ | :-------------------------------------------------------------------------- |
| `Docker Desktop failed to start`             | Corrupted settings JSON or port conflict in virtualization service. | Reset Docker to factory defaults in Troubleshoot menu.                      |
| `Slow file synchronization on macOS/Windows` | Legacy osxfs/gRPC FUSE file sharing slowing down volume mounts.     | Enable **VirtioFS** in Docker Desktop Settings > General / Virtualization.  |
| `No space left on device`                    | Virtual disk (`Docker.raw`) filled by dangling images and volumes.  | Run `docker system prune -af --volumes` or resize virtual disk in Settings. |

## References

- [Docker Desktop Manual](https://docs.docker.com/desktop/)
