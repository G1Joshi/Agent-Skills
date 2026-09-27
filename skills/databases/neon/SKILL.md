---
name: neon
description: Expert Neon serverless PostgreSQL assistance covering scale-to-zero, instant database branching, connection pooling, and pgvector. Use when setting up serverless Postgres, ephemeral CI/CD databases, or edge apps.
---

# Neon

Neon is a serverless open-source PostgreSQL database. It separates storage and compute to offer features like "Scale to Zero", "Instant Branching", and "Bottomless Storage".

## When to Use

- **Serverless PostgreSQL**: Modern PostgreSQL with decoupled storage and compute, scaling down to zero when idle to eliminate costs.
- **Database Branching for Previews**: Instantly branching production databases in milliseconds for CI/CD pipelines, staging, and pull requests.
- **Autoscaling Relational Workloads**: Automatically scaling compute CPU and RAM dynamically during traffic spikes without connection dropouts.
- **Edge Computing & Serverless Functions**: Connecting via WebSockets and HTTP drivers from Cloudflare Workers, Vercel, and AWS Lambda.

## Quick Start

```typescript
// Connect to Neon using the serverless driver over WebSockets / HTTP
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL);

async function getUsers() {
  const users = await sql`SELECT id, name, email FROM users LIMIT 10`;
  return users;
}
```

## Core Concepts

#Separation of Compute and Storage Architecture

Stateless PostgreSQL compute nodes query a custom, distributed, multi-tenant storage engine backed by cloud object storage:

```
[ Stateless Postgres Compute Node ] ──Page Service Protocol──→ [ Distributed Storage Engine ]
                                                                        │ (LSM Tree)
                                                                        ▼
                                                             [ Immutable Cloud S3 ]
```

#Copy-on-Write Database Branching

Creates instant, isolated point-in-time database clones using copy-on-write storage:

```bash
# Create a fresh database branch from production using Neon CLI
neon branch create --name pr-415-preview --from main
# Creates an isolated, fully functional Postgres instance in 500ms!
```

#Serverless Driver over WebSockets / HTTP

Bypasses TCP connection handshake overhead from serverless environments:

```typescript
// Connect via Neon Serverless Driver (Vercel / Cloudflare Workers)
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);
const users =
  await sql`SELECT id, email, created_at FROM users WHERE active = true LIMIT 10`;
```

## Common Patterns

### Ephemeral Database Branching for CI/CD

**Problem**: Integration tests running against shared databases cause state collisions and flakiness.

**Solution**:
Create a disposable copy-on-write branch for each PR or test run:

```bash
# Create instant branch from staging parent
BRANCH_INFO=$(neon branch create pr-tests-42 --from staging -o json)
BRANCH_CONN=$(echo $BRANCH_INFO | jq -r '.connection_uris[0].connection_uri')

# Run migrations and integration test suite against ephemeral branch
DATABASE_URL=$BRANCH_CONN npm run test:e2e

# Delete branch after test suite completes
neon branch delete pr-tests-42
```

## Best Practices (2026)

**Do**:

- **Integrate Database Branching into GitHub Actions**: Spin up isolated preview databases for each pull request; destroy them on merge.
- **Use the Serverless HTTP Driver for Edge Functions**: Prevent connection starvation using `@neondatabase/serverless`.
- **Enable Autosuspend for Non-Production Branches**: Configure dev branches to suspend after 5 minutes of inactivity to minimize costs.
- **Leverage Connection Pooling**: Connect via the pooled connection string (`-pooler`) when connecting from serverless backends.

**Don't**:

- **Don't open direct TCP connections from thousands of Lambda functions**: Direct TCP exhausted Postgres connection limits; use the pooled endpoint.
- **Don't keep preview branches alive indefinitely**: Automate cleanup of merged pull request database branches via GitHub Actions.
- **Don't omit query parameters in template strings**: Always use tagged template literals (`sql`SELECT * FROM users WHERE id = ${id}``) to prevent SQLi.

## Troubleshooting

| Error                                              | Cause                                                              | Solution                                                                              |
| :------------------------------------------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `connection timeout on first request (cold start)` | Compute was scaled to zero and requires ~500ms to spin up.         | Use Neon Connection Pooler endpoint (`-pooler` domain suffix) or keep active compute. |
| `too many clients already`                         | Connecting directly to Postgres compute from serverless functions. | Use the pooled connection string with PgBouncer enabled.                              |
| `Branch creation limit reached`                    | Exceeded project branch limits on current subscription tier.       | Automate deletion of merged or stale branches via Neon CLI in CI.                     |

## References

- [Neon Documentation](https://neon.tech/docs)
