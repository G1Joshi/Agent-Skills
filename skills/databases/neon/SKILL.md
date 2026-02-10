---
name: neon
description: Neon serverless PostgreSQL with branching. Use for serverless Postgres.
---

# Neon

Neon is a serverless open-source PostgreSQL database. It separates storage and compute to offer features like "Scale to Zero", "Instant Branching", and "Bottomless Storage".

## When to Use

- **Cost Efficiency**: "Scale to Zero" means you pay nothing when no one is using the app (Dev/Test envs).
- **Developer Workflow**: "Instant Branching" (Copy-on-write) lets you create a full clone of specific Prod data for testing in 1 second.
- **Standard Postgres**: It _is_ Postgres. Not a fork with limitations.

## Core Concepts

### Separated Architecture

- **Compute**: Stateless Postgres nodes. Can boot in <500ms.
- **Storage**: Custom "Pageserver" layer purely for storage.

### Data Branching

You can fork your database at a specific timestamp or LSN.

```bash
# Create a branch for testing feature X
neon branch create test_feature_x --from main
```

This is instant (COW) and cheap.

## Best Practices (2025)

**Do**:

- **Use Branching for CI/CD**: Spin up an ephemeral DB branch for every Pull Request. Run tests, delete branch.
- **Use Connection Pooling**: Neon includes PgBouncer proxy. Use the pooled connection string for serverless functions.
- **Autoscaling**: Configure autoscaling limits to handle spikes without overpaying.

**Don't**:

- **Don't worry about storage size**: Neon storage scales automatically.

## References

- [Neon Documentation](https://neon.tech/docs)
