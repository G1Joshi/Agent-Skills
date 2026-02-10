---
name: mariadb
description: MariaDB MySQL-compatible database with Galera clustering. Use for MySQL-compatible database needs.
---

# MariaDB

MariaDB is a fork of MySQL, created by the original developers of MySQL. It is guaranteed to stay open source. It lists features that MySQL doesn't have, or adds them faster.

## When to Use

- **MySQL Compatible**: Drop-in replacement for MySQL.
- **Open Source**: If you prefer GPL over Oracle's dual license.
- **Advanced Features**: Flashback, Sequences, Dynamic Columns (NoSQL), Spider Engine (Sharding).

## Quick Start

Same as MySQL usually.

```sql
-- System-Versioned Tables (Time Travel)
CREATE TABLE t (
  x INT,
  PERIOD FOR SYSTEM_TIME (ts_start, ts_end)
) WITH SYSTEM VERSIONING;

-- Query history
SELECT * FROM t FOR SYSTEM_TIME AS OF TIMESTAMP '2024-01-01 00:00:00';
```

## Core Concepts

### Storage Engines

MariaDB supports many more engines out of the box than MySQL:

- **Aria**: Crash-safe replacement for MyISAM.
- **ColumnStore**: For analytics (Columnar storage).
- **Spider**: For database sharding.

### Galera Cluster

Synchronous multi-master replication. Available in MariaDB by default.

## Best Practices (2025)

**Do**:

- **Use Vector Search (2025)**: MariaDB Enterprise 2025 adds native vector search for AI RAG apps.
- **Use Thread Pooling**: Enabled by default in MariaDB (unlike safe MySQL), handling high connection counts efficiently.

**Don't**:

- **Don't assume 100% MySQL parity**: While mostly compatible, new JSON functions and optimizers diverge. Check the specific version docs (11.x).

## References

- [MariaDB Knowledge Base](https://mariadb.com/kb/en/)
