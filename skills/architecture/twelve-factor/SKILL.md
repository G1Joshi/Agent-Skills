---
name: twelve-factor
description: Expert Twelve-Factor App methodology assistance covering declarative setup, environment configuration, backing service bindings, stateless processes, and concurrency models. Use when architecting cloud-native applications, containerizing web services, or standardizing 12-factor compliance.
---

# Twelve-Factor App

The Twelve-Factor App methodology provides architectural guidelines for building portable, resilient software-as-a-service applications optimized for modern cloud platforms and container runtimes.

## When to Use

- **Cloud-Native Application Architecture**: Designing stateless, scalable web applications intended for Kubernetes, PaaS, or container clusters.
- **Legacy Replatforming**: Modernizing monolithic legacy software into containerized, cloud-ready deployment units.
- **Zero-Downtime Rolling Deploys**: Ensuring services can boot fast, survive sudden terminations, and run alongside differing versions.
- **Standardizing Microservice Conventions**: Establishing uniform configuration, logging, and dependency isolation standards across teams.

## Quick Start

```dockerfile
# Dockerfile embodies dependencies, port binding, and build/run separation
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
# Dependencies
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
# Config via Env
ENV PORT=8080
# Port Binding
EXPOSE 8080
# Disposability (Process 1)
CMD ["node", "dist/main.js"]
```

## Core Concepts

### Declarative Dependencies & Port Binding

Dependencies are strictly pinned; applications self-host their web servers and bind directly to assigned ports:

```json
// Explicit pinned dependencies in package.json
{
  "dependencies": {
    "express": "4.19.2",
    "pg": "8.12.0"
  }
}
```

```typescript
// Self-contained port binding (no external application container like Tomcat required)
const port = process.env.PORT || 8080;
app.listen(port, () => console.log(`Server bound to port ${port}`));
```

### Config Stored in the Environment

Strict separation of code and config; credentials, hostnames, and secrets are injected via environment variables:

```typescript
// Validate environment config with Zod at startup
import { z } from "zod";

const EnvSchema = z.object({
  PORT: z.coerce.number().default(8080),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  NODE_ENV: z.enum(["development", "test", "production"]).default("production"),
});

export const config = EnvSchema.parse(process.env);
```

### Disposability & Graceful Shutdown

Processes must start fast and shut down gracefully upon receiving termination signals:

```typescript
// Graceful termination handling
process.on("SIGTERM", async () => {
  console.log("SIGTERM received. Draining connections...");
  server.close(async () => {
    await dbPool.end();
    console.log("All connections closed. Exiting process.");
    process.exit(0);
  });
});
```

## Common Patterns

### Graceful Shutdown (Disposability)

**Problem**: Unhandled SIGTERM signals cause aborted in-flight HTTP requests and database connection leaks during rolling updates.

**Solution**:
Intercept OS termination signals to drain traffic and close resources cleanly:

```typescript
import express from "express";

const app = express();
const server = app.listen(process.env.PORT || 8080);

const shutdown = async (signal: string) => {
  console.log(`Received ${signal}, starting graceful shutdown...`);
  server.close(async () => {
    // Close DB pool, flush queues, drain connections
    await dbPool.end();
    console.log("Cleanup complete. Exiting.");
    process.exit(0);
  });

  // Force shutdown after timeout
  setTimeout(() => {
    console.error("Forcefully terminating process due to timeout.");
    process.exit(1);
  }, 10000).unref();
};

process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));
```

## Best Practices

**Do**:

- Treat Logs as Event Streams: Write JSON logs directly to `stdout` / `stderr`; let vector collectors (FluentBit, Promtail) ship them.
- Execute One-Off Admin Tasks in the Same Environment: Run database migrations via one-off container jobs matching release image hashes.
- Keep Development and Production Parity: Use Docker Compose locally to run the exact database and cache engines used in production.
- Keep Processes Stateless: Store persistent data in external backing services (PostgreSQL, S3, Redis).

**Don't**:

- Hardcode configuration or secrets in source code: Keep all credentials out of Git repositories.
- Rely on sticky sessions: Session state must live in distributed caches (Redis) to allow effortless horizontal scaling.
- Log to local files inside containers: Container filesystems are ephemeral and destroyed upon pod restart.

## Troubleshooting

| Error                             | Cause                                                   | Solution                                                                      |
| :-------------------------------- | :------------------------------------------------------ | :---------------------------------------------------------------------------- |
| `Container killed with 137 (OOM)` | Memory leak or unbounded container memory limit.        | Set appropriate memory limits and profile process heap usage.                 |
| `EADDRINUSE`                      | Port binding conflict or previous process did not exit. | Check running containers/processes; ensure dynamic `PORT` assignment.         |
| `Missing environment variable`    | Config not injected during container startup.           | Validate required env vars at startup using schema validation (e.g. Zod/Joi). |

## References

- [The Twelve-Factor App](https://12factor.net/)
- [Beyond the Twelve-Factor App (O'Reilly)](https://www.oreilly.com/library/view/beyond-the-twelve-factor/9781492042631/)
