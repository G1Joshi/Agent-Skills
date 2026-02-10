---
name: railway
description: Railway platform for instant deployments. Use for simple hosting.
---

# Railway

Railway is a modern PaaS that offers "Infrastructure from Code". It introspects your repo and deploys it. Can also deploy Databases (Postgres, Redis, Mongo).

## When to Use

- **Heroku Alternative**: Cheaper and more modern interface than Heroku.
- **Databases**: Spining up a private network with a Service and a Redis/Postgres DB is 1 click.
- **Monorepos**: Excellent support for building multiple services (frontend, backend, worker) from one repo.

## Quick Start (CLI)

```bash
railway login
railway init
railway up
```

## Core Concepts

### Services

Apps or Databases.

### Canvas

A visual graph of your infrastructure showing usage and relationships.

### Config as Code

`railway.toml` allows you to define build commands and deploy health checks.

## Best Practices (2025)

**Do**:

- **Use Private Networking**: Services communicate over private IP (IPv6). Explicitly expose only what needs public access.
- **Use Templates**: One-click deploy "PostHog", "Metabase", "Cronicle".
- **Use Priority Boarding**: For critical production apps, upgrade the plan to ensure capacity.

**Don't**:

- **Don't rely on ephemeral disk**: Just like Heroku, filesystem is reset on deploy.

## References

- [Railway Documentation](https://docs.railway.app/)
