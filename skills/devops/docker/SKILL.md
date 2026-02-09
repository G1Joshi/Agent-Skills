---
name: docker
description: Docker containerization with Dockerfile, Compose, multi-stage builds, and production optimization. Use for containers.
---

# Docker

Container platform for building, shipping, and running applications.

## When to Use

- Containerizing applications
- Development environment consistency
- Microservices deployment
- CI/CD pipelines

## Quick Start

```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

## Core Concepts

### Dockerfile Best Practices

```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN adduser --disabled-password appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8000
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8000"]
```

### Docker Compose

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: postgres
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Common Patterns

### Layer Optimization

```dockerfile
# Order layers by change frequency
COPY package*.json ./           # Changes less often
RUN npm ci
COPY . .                        # Changes more often

# Combine RUN commands
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### Common Commands

```bash
# Build
docker build -t myapp .
docker build --target production -t myapp:prod .

# Run
docker run -d --name myapp -p 3000:3000 myapp
docker run -it --rm myapp sh

# Compose
docker compose up -d
docker compose logs -f app
docker compose down -v
```

## Best Practices

**Do**:

- Use multi-stage builds
- Run as non-root user
- Use specific base image tags
- Include health checks

**Don't**:

- Use `latest` tag
- Run as root in production
- Copy unnecessary files
- Ignore .dockerignore

## Troubleshooting

| Issue           | Cause            | Solution                           |
| --------------- | ---------------- | ---------------------------------- |
| Build slow      | No layer caching | Order commands by change frequency |
| Image too large | No multi-stage   | Use multi-stage builds             |
| Container exits | Process crashes  | Check logs, add healthcheck        |

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
