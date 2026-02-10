---
name: fly-io
description: Fly.io edge platform with global distribution. Use for edge deployment.
---

# Fly.io

Fly.io transforms containers into Firecracker MicroVMs running on bare metal across the globe. It is essentially a "CDN for your backend".

## When to Use

- **Global/Edge**: You want your Node.js server running in Tokyo, London, and New York simultaneously.
- **Postgres**: Run a Postgres read-replica cluster globally with ease.
- **Docker**: You have a Dockerfile and want it running in 5 seconds.

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

### Machines

Fly v2 runs on "Machines" (fast-booting VMs). They can wake-on-request (scale to zero).

### Regions

Choose from 30+ regions. `primary_region` for Writes, others for Reads.

### Fly Proxy

Magic routing layer. Routes `your-app.fly.dev` to the nearest healthy machine. Also handles internal DNS (`app-name.internal`).

## Best Practices (2025)

**Do**:

- **Use Machines API**: For programmatic control (e.g., spinning up on-demand workers).
- **Use Tigris**: S3-compatible object storage integrated with Fly (since Fly has no native S3).
- **Scale to Zero**: Save money on dev environments by allowing machines to sleep.

**Don't**:

- **Don't assume persistent IP**: Machines move. Use the strict internal DNS `[app].internal`.

## References

- [Fly.io Documentation](https://fly.io/docs/)
