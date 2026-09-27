---
name: datagrip
description: Expert JetBrains DataGrip assistance covering multi-database navigation, SQL schema diffs, query explain plans, and data import/export. Use when querying, managing, and profiling relational and NoSQL databases.
---

# DataGrip

DataGrip is the database IDE. It supports PostgreSQL, MySQL, Redis, Mongo, Snowflake, BigQuery, and more.

## When to Use

- **Professional Database Administration & Querying**: JetBrains IDE for PostgreSQL, MySQL, Oracle, SQL Server, and Snowflake.
- **Complex Query Optimization & Visual Explain**: Inspecting query execution plans and index bottlenecks visually.
- **Database Schema Diffing & Migration**: Comparing two databases and generating DDL synchronization migration scripts.
- **Data Export & Transformation**: Exporting query results to CSV, JSON, SQL inserts, or Parquet with custom extractors.

## Quick Start

```sql
-- Use DataGrip scratch files or query consoles to analyze execution plans:
EXPLAIN ANALYZE
SELECT o.id, c.name, o.total
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY o.total DESC;
```

## Core Concepts

#Query Console & Visual Execution Plan Inspection

Optimizing complex analytical SQL queries:

```sql
-- Query Console
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT
    c.customer_id,
    c.full_name,
    SUM(o.total_amount) AS lifetime_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2026-01-01'
GROUP BY c.customer_id, c.full_name
HAVING SUM(o.total_amount) > 1000.0
ORDER BY lifetime_value DESC;
```

DataGrip displays visual trees showing cost percentages, index scans, and sequential scan bottlenecks.

#Database Schema Introspection & Comparison

Generating migration scripts between staging and production:

1. Right-click database connection -> **Tools** -> **Compare Structure...**
2. Select target database environment.
3. Review colored DDL diff pane.
4. Click **Create Migration Script** to export safe ALTER TABLE statements.

#SSH Tunneling & Secure Connection Setup

Configuring secure bastion host routing:

```text
Host: 10.0.2.15 (Private RDS instance)
Port: 5432
SSH Tunnel:
  Proxy Host: bastion.company.com
  Port: 22
  User: devops
  Auth: Public Key (~/.ssh/id_ed25519)
```

## Common Patterns

#Schema Diff and Migration Script Generation
**Problem**: Identify schema drift between staging and production databases.  
**Solution**: Generate migration DDL using DataGrip Schema Compare.

```sql
-- Generated DataGrip schema migration script
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(32);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_phone ON users(phone_number);
```

## Best Practices (2026)

- **Do** configure database connections with read-only modes (`Transaction: Read-only`) when inspecting production databases.
- **Do** inspect Visual Explain plans to identify missing indexes before deploying queries to production.
- **Do** use parameter prompts (`:param_name`) in Query Consoles to test parameterized application SQL.
- **Do** route database traffic through SSH bastions or AWS SSM tunnels rather than exposing DB ports to the public internet.
- **Don't** execute raw `UPDATE` or `DELETE` statements in the Query Console without wrapping in transactions (`BEGIN; ... ROLLBACK;`).
- **Don't** store unencrypted database passwords in shared project `.idea/` directories; use OS Keyring.
- **Don't** run heavy unbounded analytical queries without limit clauses (`LIMIT 1000`).

## Troubleshooting

| Error                                          | Cause                                                  | Solution                                                                   |
| :--------------------------------------------- | :----------------------------------------------------- | :------------------------------------------------------------------------- |
| `Connection to ... failed: Connection refused` | Database port firewalled or SSH tunnel not configured. | Enable SSH/SSL tunnel in DataGrip Data Source properties > SSH tab.        |
| `Driver file not found`                        | JDBC database driver missing.                          | Click "Download Driver" button in Data Source configuration dialog.        |
| `IntelliSense unresolved table reference`      | Schemas not introspected into local metadata cache.    | Right-click data source > **Diagnostics > Refresh / Force Introspection**. |

## References

- [DataGrip Documentation](https://www.jetbrains.com/datagrip/documentation/)
