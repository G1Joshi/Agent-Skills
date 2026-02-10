---
name: heroku
description: Heroku platform-as-a-service with buildpacks. Use for easy deployment.
---

# Heroku

Heroku remains the simplest way to deploy full-stack apps. The 2025 "Fir" generation runs on AWS Graviton (ARM) and integrates native AI capabilities.

## When to Use

- **Simplicity**: "Git Push Heroku Master". No K8s, no Dockerfiles (optional).
- **Stateful Apps**: Heroku Postgres is arguably the best managed Postgres service in existence for developer experience (DX).
- **MVP**: Fastest time to market for Rails/Django/Node apps.

## Quick Start

```bash
heroku create
git push heroku main

# Add Postgres
heroku addons:create heroku-postgresql:standard-0
```

## Core Concepts

### Dynos

Lightweight Linux containers. Pro/Enterprise dynos sleep only when told.
2025 includes **Performance-L (Large)** and **Eco** types.

### Buildpacks

Scripts that detect your language (e.g. `package.json` -> Node) and build the app.

### Releases

Atomic deployments. You can instant-rollback to v42 if v43 breaks.

## Best Practices (2025)

**Do**:

- **Use Environment Variables**: 12-Factor App methodology is native to Heroku.
- **Use Review Apps**: Spin up a temp Heroku app for every Pull Request automatically.
- **Use Docker (Container Registry)**: If Buildpacks fail you, push a Docker image.

**Don't**:

- **Don't use local filesystem**: Dynos are ephemeral. Files written to disk vanish on restart. Use S3.

## References

- [Heroku Documentation](https://devcenter.heroku.com/)
