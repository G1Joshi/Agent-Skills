---
name: railway
description: Expert Railway cloud platform assistance covering Nixpacks buildpacks, instant deployments, PostgreSQL/Redis plugins, and environment variables. Use when deploying full-stack web applications without infrastructure overhead.
---

# Railway

Railway is a modern PaaS that offers "Infrastructure from Code". It introspects your repo and deploys it. Can also deploy Databases (Postgres, Redis, Mongo).

## When to Use

- **Frictionless Full-Stack Cloud Hosting**: Deploying databases, microservices, and frontends with instant Git synchronization.
- **Private Mesh Networking**: Communicating between services over secure private IPv6 addresses without internet traversal.
- **Managed Production Databases**: One-click provisioning of PostgreSQL, Redis, MySQL, and MongoDB with automated backups.
- **Ephemeral PR Preview Environments**: Creating isolated staging environments automatically for every pull request.

## Quick Start

```bash
railway login
railway init
railway up
```

## Core Concepts

#Declarative Service Configuration (railway.json)

Defining build commands, health checks, and restart policies:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/healthz",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 5
  }
}
```

#Private Networking Across Microservices

Connecting internal services securely using Railway private domains:

```javascript
// Using internal private networking domain (zero public exposure)
const databaseUrl =
  process.env.DATABASE_PRIVATE_URL ||
  "postgresql://postgres:secret@postgres.railway.internal:5432/railway";

const redisUrl =
  process.env.REDIS_PRIVATE_URL ||
  "redis://default:secret@redis.railway.internal:6379";
```

#Railway CLI Workflow

Managing environments and deploying from terminal:

```bash
# Log in to Railway account
railway login

# Link local directory to Railway project
railway link

# Run command locally with remote environment variables injected
railway run npm run migrate

# Trigger deployment from local branch
railway up
```

## Common Patterns

### Nixpacks Configuration with Custom System Packages

**Problem**: Applications requiring system packages (e.g. ffmpeg, graphicsmagick) fail to build on standard container buildpacks.

**Solution**:
Specify custom runtime packages in `nixpacks.toml`:

```toml
[phases.setup]
nixPkgs = ["nodejs-20_x", "ffmpeg", "openssl"]

[phases.build]
cmds = ["npm run build"]

[start]
cmd = "npm start"
```

## Best Practices (2026)

- **Do** use Railway Private Networking (`*.railway.internal`) for service-to-service communication.
- **Do** define an explicit `healthcheckPath` in `railway.json` to enable zero-downtime rolling deployments.
- **Do** enable PR environments to test database migrations and frontend changes in isolated stacks.
- **Do** utilize Nixpacks for automatic dependency and runtime version detection.
- **Don't** expose databases publicly when microservices reside within the same Railway project.
- **Don't** commit `.env` files; use Railway's encrypted environment variables dashboard or CLI.
- **Don't** store persistent file uploads on the service container filesystem; use S3, R2, or Railway Volume mounts.

## Troubleshooting

| Error                                            | Cause                                                                               | Solution                                                                            |
| :----------------------------------------------- | :---------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `Deploy failed: Process did not listen on $PORT` | Web service hardcoding port instead of dynamic Railway `$PORT`.                     | Bind web server to dynamic port: `process.env.PORT                                  |     | 3000`. |
| `Database connection timeout in production`      | Service connecting using public database proxy URL inside the same Railway project. | Use private internal DNS host provided by Railway for zero latency and free egress. |
| `Railway CLI: Unauthorized`                      | Project token or user token missing.                                                | Run `railway login` or export `RAILWAY_TOKEN`.                                      |

## References

- [Railway Documentation](https://docs.railway.app/)
