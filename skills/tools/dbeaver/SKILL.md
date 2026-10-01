---
name: dbeaver
description: Expert DBeaver open-source multi-platform database tool assistance covering SQL editing, ER diagrams, data transfer, and driver management. Use when administering SQL, NoSQL, and embedded databases.
---

# DBeaver

DBeaver is a universal, open-source database tool supporting relational, document, key-value, and analytical databases with an intuitive SQL editor and data browser.

## When to Use

- **Universal Multi-Platform Database Tool**: Free, open-source database client supporting JDBC drivers for 100+ database engines.
- **Cross-Database Data Migration & Export**: Transferring tables and datasets across heterogeneous engines (e.g. MySQL to PostgreSQL).
- **Entity-Relationship Diagram (ERD) Generation**: Visualizing relational schemas, primary keys, and foreign key relations.
- **Automated Database Tasks & Script Execution**: Executing batch SQL scripts via DBeaver CLI or Task Scheduler.

## Quick Start

```sql
-- DBeaver supports executing SQL queries and parameterized templates:
SELECT
    table_schema,
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as total_size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC;
```

## Core Concepts

### Configuring JDBC Connection with SSL & SSH Tunnel

Setting up encrypted database connectivity:

```text
Driver: PostgreSQL
Host: db-internal.cluster.local
Port: 5432
Database: production_analytics
Authentication: Database Native (Username / Password)
Network -> SSH Tunnel:
  Host: bastion.cloud.internal:22
  User: ec2-user
  Private Key: ~/.ssh/bastion_key.pem
SSL Settings:
  Mode: verify-full
  Root Certificate: /etc/ssl/certs/rds-combined-ca-bundle.pem
```

### Generating Visual Entity-Relationship Diagrams (ERD)

Visualizing database schema topology:

1. Expand Database Navigator -> Right-click Schema (e.g. `public`).
2. Select **View Diagram**.
3. DBeaver renders entity boxes with columns, data types, and foreign key connector arrows.
4. Export diagram to SVG or PNG for architecture documentation.

### Exporting Datasets with Custom Formatters

Exporting query results to SQL Inserts or JSON:

```sql
SELECT
    user_id,
    email,
    created_at
FROM users
WHERE is_active = true;
```

- Right click result grid -> **Export Data** -> Select target format (**JSON**, **CSV**, **SQL INSERTs**, **Markdown**).

## Common Patterns

### Mock Data Generation

**Problem**: Populate development database with realistic test datasets.  
**Solution**: Configure DBeaver Mock Data Generator.

```sql
-- DBeaver mock data generation script
INSERT INTO customers (id, first_name, last_name, email, created_at)
SELECT
  gen_random_uuid(),
  'User_' || substr(md5(random()::text), 1, 6),
  'Test',
  'user_' || generate_series(1, 100) || '@example.com',
  NOW() - (random() * interval '30 days');
```

## Best Practices

**Do**:

- Set connection type to **Production** (sets background color to red and enforces auto-commit warnings).
- Use SSH Tunneling with public key authentication for all cloud-hosted database connections.
- Configure `dbeaver.ini` to allocate sufficient JVM heap memory (`-Xmx2048m`) when querying large datasets.
- Use the Data Transfer wizard for moving schema tables and data across different database engines.

**Don't**:

- Leave **Auto-Commit** enabled on production databases; use **Manual Commit** mode.
- Commit `dbeaver-data-sources.xml` containing plain text credentials to version control.
- Fetch hundreds of thousands of rows at once; configure result set fetch size limits.

## Troubleshooting

| Error                                                  | Cause                                                               | Solution                                                                      |
| :----------------------------------------------------- | :------------------------------------------------------------------ | :---------------------------------------------------------------------------- |
| `Java heap space / OutOfMemoryError in DBeaver`        | Query fetching millions of rows into GUI memory buffer.             | Enable "Use fetch size" (default 200) in SQL Editor settings.                 |
| `Cannot connect to database: Access Denied`            | Driver credentials or network security group restricting client IP. | Check IP allowlist in cloud database and test connection.                     |
| `Driver download failed: maven repository unreachable` | Network proxy blocking access to Maven Central.                     | Configure HTTP proxy in DBeaver Window > Preferences > Connections > Network. |

## References

- [DBeaver Documentation](https://dbeaver.com/docs/wiki/)
