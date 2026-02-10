---
name: mysql
description: MySQL relational database with InnoDB, replication, and stored procedures. Use for MySQL operations.
---

# MySQL

MySQL is a widely used relational database management system (RDBMS). It is the "M" in the LAMP stack and powers huge platforms like Facebook and WordPress.

## When to Use

- **Web Applications**: Standard for PHP/Laravel/Wordpress ecosystems.
- **Read-Heavy Workloads**: Historically very fast for simple read operations.
- **Replication**: Huge ecosystem of tools for Master-Slave replication and clustering (Galera, InnoDB Cluster).

## Quick Start

```sql
-- Upsert (Insert or Update)
INSERT INTO users (id, name) VALUES (1, 'Jane')
ON DUPLICATE KEY UPDATE name = 'Jane';
```

## Core Concepts

### Storage Engines

- **InnoDB**: The default. Supports transactions (ACID), row-level locking, and foreign keys. **Always use this**.
- **MyISAM**: Legacy. Fast reads but table-level locking and no transactions. Avoid.

### Explain

Prefix any query with `EXPLAIN` to see how MySQL executes it (indexes used, rows scanned).

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@test.com';
```

### Replication

MySQL replication is often asynchronous by default, meaning slaves might lag behind master.

## Best Practices (2025)

**Do**:

- **Use MySQL 8.4+**: For LTS features like `EXPLAIN ANALYZE` and CTE support.
- **Use `utf8mb4`**: The _real_ UTF-8. The standard `utf8` in MySQL is a partial implementation (max 3 bytes).
- **Disable `mysql_native_password`**: In 8.4+, use `caching_sha2_password` for security.

**Don't**:

- **Don't use MyISAM**: It is effectively obsolete for modern apps.
- **Don't store logic in Stored Procedures**: Hard to version control and debug. Keep logic in the app layer.

## References

- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/)
