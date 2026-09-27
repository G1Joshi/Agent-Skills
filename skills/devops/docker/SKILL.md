---
name: docker
description: Expert Docker containerization assistance covering multi-stage Dockerfiles, Docker Compose, layer caching, and container security. Use when containerizing applications, creating reproducible environments, or optimizing images.
---

# Docker

Docker standardizes software delivery by packaging apps into containers. In 2025, Docker emphasizes **BuildKit** for high-performance builds and **Docker Scout** for supply chain security.

## When to Use

- **Application Containerization**: Packaging code, runtime, system libraries, and settings into portable, reproducible container images.
- **Multi-Stage Build Optimization**: Creating ultra-small, secure production container images stripped of compilers and build tooling.
- **Local Microservice Development**: Orchestrating multi-container environments (app, database, cache) with Docker Compose.
- **Standardized CI/CD Artifacts**: Building OCI-compliant images deployed to Kubernetes, ECS, or serverless container runtimes.

## Quick Start

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS deps
RUN npm ci

FROM base AS release
COPY --from=deps /app/node_modules ./node_modules
COPY . .
CMD ["node", "index.js"]
```

## Core Concepts

#Multi-Stage Production Dockerfile

Building a minimal, secure Node.js container with non-root user:

```dockerfile
# syntax=docker/dockerfile:1.7
# Stage 1: Build & Dependencies
FROM node:22-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build && npm prune --production

# Stage 2: Distroless/Minimal Production Runtime
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Security: Run as unprivileged non-root user
USER node

# Copy only production artifacts
COPY --chown=node:node --from=builder /app/node_modules ./node_modules
COPY --chown=node:node --from=builder /app/dist ./dist
COPY --chown=node:node --from=builder /app/package.json ./package.json

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/healthz || exit 1

ENTRYPOINT ["node", "dist/index.js"]
```

#Multi-Container Orchestration with Docker Compose

Defining local development stacks with health checks:

```yaml
services:
  api:
    build:
      context: .
      target: runner
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://app:secret@db:5432/appdb
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine

volumes:
  postgres_data:
```

#Image Build Caching & Optimization

Accelerating builds using Docker Buildx:

```bash
# Build multi-platform image with layer caching
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag myregistry.com/app:v2.1.0 \
  --cache-to type=inline \
  --push .
```

## Common Patterns

### Secure Multi-Stage Dockerfile with Non-Root User

**Problem**: Container images are bloated (>1GB) and run as root, creating container breakout security risks.

**Solution**:
Use multi-stage builds and unprivileged user execution:

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production runtime stage (minimal footprint)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

## Best Practices (2026)

- **Do** always use multi-stage builds to exclude compilers, test frameworks, and development dependencies from final images.
- **Do** run containers as non-root users (`USER appuser`) to mitigate container breakout vulnerabilities.
- **Do** order Dockerfile instructions by change frequency: copy package manifests first to leverage layer caching.
- **Do** include an explicit `HEALTHCHECK` instruction to allow orchestrators to assess container readiness.
- **Don't** use `:latest` tags in production; pin specific immutable version tags or digest SHAs.
- **Don't** store sensitive secrets or `.env` files in images; use BuildKit secret mounts (`--mount=type=secret`).
- **Don't** run systemd or multiple processes inside a single container; maintain one responsibility per container.

## Troubleshooting

| Error                                                                | Cause                                                                       | Solution                                                                                      |
| :------------------------------------------------------------------- | :-------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `Cannot connect to the Docker daemon at unix:///var/run/docker.sock` | Docker daemon is not running or current user lacks docker group permission. | Start Docker service (`systemctl start docker`) or add user: `sudo usermod -aG docker $USER`. |
| `no space left on device during docker build`                        | Dangling images and unused build cache filling disk.                        | Prune unused Docker data: `docker system prune -af --volumes`.                                |
| `exec user process caused: no such file or directory`                | Shell script has Windows CRLF line endings or missing glibc on Alpine.      | Convert line endings to LF (`dos2unix`) or install `libc6-compat`.                            |

## References

- [Docker Documentation](https://docs.docker.com/)
