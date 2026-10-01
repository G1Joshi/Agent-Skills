---
name: heroku
description: Expert Heroku PaaS assistance covering Procfile, buildpacks, dynos, Heroku Postgres/Redis, and CLI management. Use when deploying and running web applications on Heroku without managing infrastructure.
---

# Heroku

Heroku is a fully managed cloud Platform as a Service (PaaS) that enables developers to build, run, and scale applications without infrastructure management overhead.

## When to Use

- **Rapid Application Deployment & MVPs**: Deploying full-stack web applications with `git push heroku main` and zero server management.
- **Managed Data Add-ons**: Instantly provisioning production-grade Heroku Postgres, Redis, and Apache Kafka.
- **Procfile-Driven Workloads**: Declaring web, background worker, and cron scheduler processes clearly.
- **Enterprise Review Apps**: Automatically spinning up ephemeral preview environments for every GitHub pull request.

## Quick Start

```bash
heroku create
git push heroku main

# Add Postgres
heroku addons:create heroku-postgresql:standard-0
```

## Core Concepts

### Declarative Process Definition with Procfile

Declaring web servers, queue workers, and database release migrations:

```text
# Procfile in repository root
release: python manage.py migrate --no-input
web: gunicorn myproject.wsgi:application --workers 4 --bind 0.0.0.0:$PORT
worker: celery -A myproject worker -l info --concurrency 2
clock: python clock.py
```

### Ephemeral Review Apps Configuration (app.json)

Automating branch preview environments:

```json
{
  "name": "SaaS Platform",
  "description": "Production SaaS application with Heroku Postgres and Redis",
  "scripts": {
    "postdeploy": "python manage.py setup_test_fixtures"
  },
  "env": {
    "DJANGO_SETTINGS_MODULE": "myproject.settings.review",
    "SECRET_KEY": { "generator": "secret" }
  },
  "addons": [
    { "plan": "heroku-postgresql:essential-0" },
    { "plan": "heroku-redis:mini" }
  ]
}
```

### Heroku CLI Operations

Scaling dynos, managing config, and running one-off processes:

```bash
# Set production environment variables
heroku config:set NODE_ENV=production DATABASE_POOL_SIZE=20 -a my-prod-app

# Scale web and worker dynos
heroku ps:scale web=2:standard-2x worker=1:standard-1x -a my-prod-app

# Run one-off interactive console or migration
heroku run bash -a my-prod-app
heroku logs --tail -a my-prod-app
```

## Common Patterns

### Multi-Process Procfile with Web and Background Worker

**Problem**: Heavy asynchronous tasks block the web dyno and trigger H12 request timeouts.

**Solution**:
Separate HTTP web serving from background worker processes in `Procfile`:

```text
web: node dist/server.js
worker: node dist/worker.js
release: npx prisma migrate deploy
```

Scale dynos: `heroku ps:scale web=2 worker=1`

## Best Practices

**Do**:

- Use the `release:` phase in `Procfile` to run database migrations before routing traffic to new dynos.
- Configure `WEB_CONCURRENCY` to match dyno memory capacity and prevent R14 (Memory Quota Exceeded) errors.
- Bind to `$PORT` provided by Heroku; never hardcode HTTP port numbers in web applications.
- Use Heroku Review Apps in GitHub pull request workflows for stakeholder review.

**Don't**:

- Store uploaded user files on dyno local filesystems; dynos are ephemeral—use AWS S3 or Cloudflare R2.
- Run long-running CPU tasks in web dynos; offload to background worker dynos.
- Leave development add-ons on production apps; upgrade to production-tier Postgres with automated failover.

## Troubleshooting

| Error                                                                               | Cause                                                       | Solution                                                        |
| :---------------------------------------------------------------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------------- |
| `Error R10 (Boot timeout) -> Web process failed to bind to $PORT within 60 seconds` | Server listening on hardcoded port instead of `$PORT`.      | Bind web server to dynamic port: `process.env.PORT`.            |
| `Error H12 (Request timeout) -> Request took longer than 30 seconds`                | Synchronous request exceeded Heroku 30-second router limit. | Offload long-running operations to background worker dynos.     |
| `Error R14 (Memory quota exceeded)`                                                 | Memory usage exceeded dyno limits (512MB on Standard-1X).   | Optimize memory or upgrade to Standard-2X or Performance dynos. |

## References

- [Heroku Documentation](https://devcenter.heroku.com/)
