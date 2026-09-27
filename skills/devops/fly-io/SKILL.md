---
name: fly-io
description: Expert Fly.io assistance covering fly.toml, global app distribution, persistent volumes, Machines API, and scaling. Use when deploying full-stack apps and databases close to users globally.
---

# Fly.io

Fly.io transforms containers into Firecracker MicroVMs running on bare metal across the globe. It is essentially a "CDN for your backend".

## When to Use

- **Global Edge Microservices & APIs**: Deploying full-stack applications and databases physically close to users.
- **Modern Full-Stack Frameworks**: Next.js, Remix, Phoenix LiveView, Rails, and Node.js with instant global scaling.
- **LiteFS Distributed SQLite**: Replicating SQLite databases globally with low-latency local reads and streaming primary writes.
- **GPU Inference at the Edge**: Running open-weight AI models on edge GPUs with rapid cold starts.

## Quick Start

```bash
fly launch
# Scans source code, creates Dockerfile, creates fly.toml

fly deploy
```

```toml
# fly.toml
app = "my-app"
primary_region = "iad"

[http_service]
  internal_port = 8080
  force_https = true
```

## Core Concepts

#Declarative Configuration with fly.toml

Defining machine resources, scaling rules, and health checks:

```toml
# fly.toml
app = "api-edge-service"
primary_region = "ord" # Chicago primary

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = 'stop'   # Scale to zero when idle
  auto_start_machines = true
  min_machines_running = 1

  [http_service.concurrency]
    type = "requests"
    soft_limit = 200
    hard_limit = 250

[[vm]]
  size = "shared-cpu-2x"
  memory = "2048mb"

[[services.http_checks]]
  interval = "10s"
  timeout = "2s"
  grace_period = "5s"
  method = "get"
  path = "/healthz"
```

#Global SQLite Replication with LiteFS

Configuring distributed SQLite clusters with automated failover:

```yaml
# etc/litefs.yml
fuse:
  dir: "/litefs"

data:
  dir: "/var/lib/litefs"

exit-on-error: false

proxy:
  addr: ":8080"
  target: "localhost:8081"
  db: "production.db"

lease:
  type: "consul"
  advertise-url: "http://${FLY_ALLOC_ID}.vm.${FLY_APP_NAME}.internal:20202"
  candidate: ${FLY_REGION == "ord"} # Only Chicago is eligible for primary
```

#Fly CLI (flyctl) Deployment Workflows

Deploying and scaling applications across geographic regions:

```bash
# Launch app from current directory
fly launch --no-deploy

# Deploy container image to edge fleet
fly deploy

# Scale application to multiple global regions
fly scale count 3 --region ord,fra,sin

# Inspect status of running Fly Machines
fly status
fly logs
```

## Common Patterns

### Persistent Volume with Multi-Region Machine Configuration

**Problem**: Stateful databases on ephemeral serverless platforms lose disk data when scaled.

**Solution**:
Attach persistent Fly volumes in `fly.toml`:

```toml
app = "my-sqlite-db"
primary_region = "ord"

[mounts]
  source = "data_vol"
  destination = "/data"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
```

Provision volume: `fly volumes create data_vol --region ord --size 10`

## Best Practices (2026)

- **Do** set `auto_stop_machines = 'stop'` and `auto_start_machines = true` to reduce costs on low-traffic endpoints.
- **Do** deploy in regions closest to your primary database or users to minimize latency.
- **Do** use persistent Fly Volumes (`fly volumes create`) for services requiring local storage.
- **Do** use `fly secrets set` to encrypt and inject environment variables securely.
- **Don't** commit sensitive environment secrets into `fly.toml`.
- **Don't** run multi-node primary-write databases without LiteFS or managed PostgreSQL clusters.
- **Don't** neglect health checks; Fly requires passing checks to route HTTP traffic to instances.

## Troubleshooting

| Error                                                    | Cause                                                           | Solution                                               |
| :------------------------------------------------------- | :-------------------------------------------------------------- | :----------------------------------------------------- |
| `Error: could not find an instance of app ... in region` | App has no running Machines deployed in the targeted region.    | Deploy machines with `fly scale count 2 --region ord`. |
| `Machine crashed with exit code 137`                     | Process exceeded allocated Machine RAM (OOM killed).            | Increase machine RAM: `fly scale memory 1024`.         |
| `Health check failing on /health`                        | Application took longer to boot than configured `grace_period`. | Increase `grace_period = "30s"` in `fly.toml`.         |

## References

- [Fly.io Documentation](https://fly.io/docs/)
