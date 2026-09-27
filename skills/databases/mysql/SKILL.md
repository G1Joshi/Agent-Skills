---
name: mysql
description: Expert MySQL relational database assistance covering InnoDB engine, query optimization with EXPLAIN, transactions, and replication. Use when designing relational schemas, tuning SQL queries, or scaling MySQL.
---

# MySQL

MySQL is a widely used relational database management system (RDBMS). It is the "M" in the LAMP stack and powers huge platforms like Facebook and WordPress.

## When to Use

- **Web Application Relational Backbone**: The world's most popular open-source relational database powering WordPress, Rails, and web backends.
- **ACID Transaction Guarantees**: Processing financial transactions, order checkouts, and inventory balances reliably with InnoDB.
- **Read-Heavy Web Applications**: Scaling reads horizontally using primary-replica asynchronous and semi-synchronous replication topologies.
- **Modern Document Store (JSON Columns)**: Indexing and querying semi-structured JSON documents alongside relational SQL tables.

## Quick Start

```sql
-- Upsert (Insert or Update)
INSERT INTO users (id, name) VALUES (1, 'Jane')
ON DUPLICATE KEY UPDATE name = 'Jane';
```

## Core Concepts

#InnoDB Storage Engine & B+Tree Clustered Indexes

InnoDB stores table rows clustered physically on disk by primary key, providing instant primary key lookups:

```sql
CREATE TABLE commerce.orders (
    order_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    status ENUM('PENDING', 'PAID', 'SHIPPED', 'CANCELLED') DEFAULT 'PENDING',
    details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_status (user_id, status)
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC;
```

#JSON Functional Indexes

Creates virtual indexed columns over specific JSON paths to accelerate document queries:

```sql
-- Create functional index on JSON path
ALTER TABLE commerce.orders
ADD INDEX idx_customer_tier ((CAST(details->>'$.customer.tier' AS CHAR(20))));

-- Optimized index query
SELECT * FROM commerce.orders
WHERE details->>'$.customer.tier' = 'Platinum';
```

#Semi-Synchronous Replication Topology

Guarantees that at least one read replica has received transaction events before returning success:

```
[ Primary Master ] ──Replication Event──→ [ Replica 1 (Awaits ACK) ] ──ACK──→ [ Primary Commits ]
                                                  │
                                                  ▼
                                       [ Replica 2 (Async) ]
```

## Common Patterns

### Keyset Pagination (Seek Method)

**Problem**: Traditional `OFFSET 1000000 LIMIT 20` scans and discards 1 million rows, resulting in extreme query latency.

**Solution**:
Use keyset seek pagination utilizing indexed primary key comparisons:

```sql
-- Fast seek pagination regardless of page depth
SELECT id, title, price, created_at
FROM products
WHERE (created_at, id) < ('2025-03-01 10:00:00', 94821)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

## Best Practices (2026)

**Do**:

- **Choose Compact Primary Keys**: Use `BIGINT UNSIGNED AUTO_INCREMENT` or ordered UUIDs (v7); secondary indexes store the primary key.
- **Size `innodb_buffer_pool_size` Appropriately**: Allocate 70-80% of total physical RAM to the InnoDB buffer pool on dedicated servers.
- **Use `EXPLAIN FORMAT=JSON`**: Inspect query execution plans to identify temporary tables, filesorts, and full table scans.
- **Enable Binary Logging with Row Format**: Set `binlog_format = ROW` for safe, deterministic replication and point-in-time recovery.

**Don't**:

- **Don't use random UUIDv4 as primary keys**: Random UUIDs cause index page fragmentation and severe disk I/O thrashing during inserts.
- **Don't use `SELECT *` in production code**: Query only needed columns to leverage covering indexes.
- **Don't store unstructured text without character sets**: Default to `utf8mb4` with `utf8mb4_0900_ai_ci` collation for full Unicode support.

## Troubleshooting

| Error                                            | Cause                                                                  | Solution                                                                                   |
| :----------------------------------------------- | :--------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| `ERROR 1205 (HY000): Lock wait timeout exceeded` | Long-running transaction holding row locks requested by another query. | Kill blocking transaction (`SHOW PROCESSLIST`) and keep transactions short.                |
| `ERROR 1040: Too many connections`               | Connection pool exhaustion exceeding `max_connections`.                | Increase `max_connections` or place ProxySQL connection pooler in front.                   |
| `Using filesort; Using temporary in EXPLAIN`     | Query cannot use index to satisfy `ORDER BY` or `GROUP BY`.            | Add composite index that includes both WHERE filter columns and ORDER BY columns in order. |

## References

- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/)
