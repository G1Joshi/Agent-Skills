---
name: planetscale
description: Expert PlanetScale serverless MySQL assistance covering non-blocking schema migrations, Vitess sharding, and database branching. Use when scaling MySQL without downtime, managing migrations, or horizontal scaling.
---

# PlanetScale

PlanetScale is a serverless database platform compatible with MySQL. It is built on **Vitess**, the technology used by YouTube/Slack to scale massively.

## When to Use

- **Horizontally Scaled MySQL (Vitess)**: Scaling relational MySQL applications to millions of queries per second without manual sharding.
- **Non-Blocking Schema Migrations**: Executing online DDL schema changes on live multi-terabyte tables with zero downtime and zero locking.
- **Database Branching & Developer Workflows**: Branching production databases for local development and merging schema changes via Deploy Requests.
- **Serverless Web Applications**: Querying MySQL from serverless environments over HTTP using the PlanetScale serverless driver.

## Quick Start

Uses standard MySQL drivers.

```bash
# Connect via CLI
pscale shell my-database main
```

## Core Concepts

### Vitess Horizontal Sharding Architecture

VTGate proxies route queries transparently across underlying VTTablet MySQL instances based on a VSchema keyspace:

```text
[ Application Client ] ──→ [ VTGate Stateless Proxy ]
                                    ├── Routes to Shard 1 (-80)
                                    └── Routes to Shard 2 (80-)
```

### Non-Blocking Online DDL & Deploy Requests

Applies schema changes via an isolated shadow table in the background, syncing changes asynchronously before an atomic cutover:

```bash
# 1. Create a development schema branch
pscale branch create my-database add-indexes

# 2. Apply migration on dev branch
pscale shell my-database add-indexes
# SQL: ALTER TABLE orders ADD INDEX idx_status (status);

# 3. Create Deploy Request to merge into production safely
pscale deploy-request create my-database add-indexes
```

### PlanetScale Serverless Driver over Fetch / HTTP

Executes queries over HTTP/1.1 and HTTP/2 without persistent TCP connections:

```typescript
import { connect } from "@planetscale/database";

const conn = connect({ url: process.env.DATABASE_URL });
const response = await conn.execute(
  "SELECT id, name FROM users WHERE active = :active",
  { active: 1 },
);
console.log("Users:", response.rows);
```

## Common Patterns

### Non-Blocking Deploy Requests for Zero-Downtime Migrations

**Problem**: Running `ALTER TABLE` on large production MySQL tables locks reads/writes and causes outages.

**Solution**:
Use PlanetScale deploy requests to test changes on a branch and apply online:

```bash
# 1. Create a schema development branch
pscale branch create my-db add-index-branch

# 2. Apply ALTER schema change safely on the branch
pscale shell my-db add-index-branch < schema_update.sql

# 3. Create deploy request to merge into main branch with zero downtime
pscale deploy-request create my-db add-index-branch
```

## Best Practices

**Do**:

- Always Use Deploy Requests for Migrations: Never attempt manual DDL migrations in production; let PlanetScale coordinate non-blocking cutovers.
- Define a Sharding Key (VSchema) Early: If planning to shard, select a high-cardinality sharding key (e.g. `user_id` or `tenant_id`).
- Use Safe Migrations Mode: Enable Safe Migrations on production branches to block accidental direct DDL executions.
- Leverage the Serverless Driver: Use `@planetscale/database` for serverless environments (Vercel, AWS Lambda, Cloudflare).

**Don't**:

- Use Foreign Key Constraints in Sharded Keyspaces: Vitess does not support distributed foreign key constraints; enforce integrity in application logic.
- Use auto-incrementing integers across sharded tables: Use distributed ID generators (UUIDv7, Snowflake IDs).
- Execute cross-shard joins frequently: Distributed joins across multiple shards incur heavy network latency.

## Troubleshooting

| Error                                                 | Cause                                                                        | Solution                                                                                      |
| :---------------------------------------------------- | :--------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `foreign key constraints are not supported (default)` | Vitess architecture discourages native foreign keys for horizontal sharding. | Enforce referential integrity in application layer or enable foreign key support in settings. |
| `Query exceeds maximum execution time`                | Query missing supporting index causing full cluster table scan.              | Add supporting index via deploy request and review query plan in Insights.                    |
| `PlanetsScale connection limit exceeded`              | Serverless application establishing excessive unpooled TCP connections.      | Use `@planetscale/database` fetch driver or configure connection pooling.                     |

## References

- [PlanetScale Documentation](https://planetscale.com/docs)
