---
name: twelve-factor
description: Twelve-factor app methodology. Use for cloud-native apps.
---

# Twelve-Factor App

The Twelve-Factor App methodology is a set of best practices for building software-as-a-service apps. In 2025, it remains the gold standard for Cloud Native microservices and containerized applications.

## When to Use

- ALWAYS, for any web application or service destined for the cloud (Kubernetes, PaaS, Serverless).
- Migrating legacy apps to the cloud (Replatforming).

## The Twelve Factors (2025 Context)

1.  **Codebase**: One codebase tracked in revision control (Git), many deploys.
2.  **Dependencies**: Explicitly declare and isolate dependencies (Docker, package.json). No system-wide installs.
3.  **Config**: Store config in the environment (Env Vars, Secrets Manager). Never in code.
4.  **Backing Services**: Treat backing services (DB, Queue, Cache) as attached resources (URL/Credentials).
5.  **Build, Release, Run**: Strictly separate build and run stages. CI/CD pipelines are mandatory.
6.  **Processes**: Execute the app as one or more stateless processes. State goes to backing services (Redis/DB).
7.  **Port Binding**: Export services via port binding (e.g., `app.listen(8080)`). No reliance on server injection (Tomcat).
8.  **Concurrency**: Scale out via the process model (Replicas in K8s).
9.  **Disposability**: Maximize robustness with fast startup and graceful shutdown (SIGTERM handling).
10. **Dev/Prod Parity**: Keep development, staging, and production as similar as possible (Docker helps here).
11. **Logs**: Treat logs as event streams. Do not write to files; write to `stdout`/`stderr`.
12. **Admin Processes**: Run admin/management tasks as one-off processes (e.g., DB migrations) in the same environment.

## Quick Start (Dockerized App)

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

## Best Practices

**Do**:

- Use **Docker** to satisfy dependencies and dev/prod parity.
- Use **Environment Variables** for secrets and config.
- Implement **Graceful Shutdown** to stop accepting new requests and finish current ones.

**Don't**:

- Don't hardcode IP addresses or file paths.
- Don't rely on "Sticky Sessions" (violates Statelessness).
- Don't log to local files in a container (they vanish).

## References

- [The Twelve-Factor App](https://12factor.net/)
- [Beyond the Twelve-Factor App (O'Reilly)](https://www.oreilly.com/library/view/beyond-the-twelve-factor/9781492042631/)
