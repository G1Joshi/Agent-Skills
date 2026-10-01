---
name: render
description: Expert Render cloud platform assistance covering render.yaml blueprints, Web Services, Background Workers, Cron Jobs, and Managed PostgreSQL. Use when deploying modern web applications and APIs.
---

# Render

Render is a modern cloud application hosting platform offering zero-downtime deploys, managed databases, preview environments, and Infrastructure as Code via Render Blueprints.

## When to Use

- **Modern Cloud Application Hosting**: Deploying web services, background workers, cron jobs, and static sites.
- **Infrastructure as Code with Render Blueprints**: Defining entire multi-service stacks in a version-controlled `render.yaml`.
- **Managed PostgreSQL & Redis**: High-availability managed databases with point-in-time recovery and connection pooling.
- **Zero-Downtime Deploys & Automated Previews**: Automatic branch previews and zero-downtime rolling releases.

## Quick Start

```yaml
# render.yaml (Blueprint)
services:
  - type: web
    name: my-api
    env: node
    plan: starter
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: PORT
        value: 10000
    autoDeploy: true
```

## Core Concepts

### Declarative Blueprint Specification (render.yaml)

Defining web APIs, background workers, and managed databases:

```yaml
# render.yaml
services:
  # Web API Service
  - type: web
    name: core-api
    runtime: node
    plan: standard
    region: oregon
    buildCommand: npm ci && npm run build
    startCommand: npm run start
    healthCheckPath: /healthz
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: core-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: core-cache
          property: connectionString

  # Background Queue Worker
  - type: worker
    name: queue-worker
    runtime: node
    plan: starter
    region: oregon
    buildCommand: npm ci
    startCommand: npm run worker:start
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: core-db
          property: connectionString

databases:
  - name: core-db
    plan: standard
    region: oregon
    postgresMajorVersion: "16"
```

### Static Site Hosting with Zero-Downtime Edge CDN

Deploying frontend static apps with SPA rewrite rules:

```yaml
- type: static
  name: marketing-site
  buildCommand: npm run build
  staticPublishPath: ./dist
  routes:
    - type: rewrite
      source: /*
      destination: /index.html
```

### Render API & Deploy Hooks

Triggering deployments programmatically:

```bash
# Trigger immediate zero-downtime deployment via deploy hook URL
curl -X POST https://api.render.com/deploy/srv-c0123456789abc?clearCache=clear
```

## Common Patterns

### Infrastructure as Code with render.yaml Blueprints

**Problem**: Inconsistent environment variable configurations between staging and production instances.

**Solution**:
Define complete application stack declaratively in `render.yaml`:

```yaml
services:
  - type: web
    name: api-service
    env: node
    plan: starter
    buildCommand: npm ci && npm run build
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: prod-db
          property: connectionString

databases:
  - name: prod-db
    plan: starter
    databaseName: ecommerce
    user: dbuser
```

## Best Practices

**Do**:

- Manage all services, databases, and cron tasks declaratively using `render.yaml` Blueprints.
- Configure `healthCheckPath` on all web services to ensure zero-downtime rolling deploys.
- Use environment variable linking (`fromDatabase`, `fromService`) to avoid hardcoding connection strings.
- Enable Point-in-Time Recovery (PITR) on production PostgreSQL databases.

**Don't**:

- Store persistent files on web service local disks; attach a persistent Disk or use S3/R2 storage.
- Commit secrets to `render.yaml`; mark variables as `sync: false` and set them in the Render Dashboard.
- Run long-running batch jobs in web service instances; offload to dedicated Background Workers.

## Troubleshooting

| Error                                       | Cause                                                                             | Solution                                                                        |
| :------------------------------------------ | :-------------------------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| `Port binding failed / Service unavailable` | Server not listening on port 10000 or `$PORT`.                                    | Configure server to listen on `process.env.PORT \|\| 10000` and host `0.0.0.0`. |
| `Build exceeded memory limit`               | Memory-intensive build step (e.g. Next.js static generation) exhausting plan RAM. | Pre-build artifacts in external CI or upgrade to higher Render plan.            |
| `Database connection limit exceeded`        | Serverless connections overwhelming Render starter database.                      | Enable Render connection pooling or deploy external PgBouncer.                  |

## References

- [Render Documentation](https://render.com/docs)
