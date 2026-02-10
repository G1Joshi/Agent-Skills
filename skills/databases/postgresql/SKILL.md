---
name: postgresql
description: PostgreSQL relational database with JSONB, CTEs, window functions, and extensions. Use for SQL queries.
---

# PostgreSQL

PostgreSQL (Postgres) is a powerful, open-source object-relational database system. It is known for its reliability, feature robustness (JSONB, GIS, Full Text Search), and performance.

## When to Use

- **Primary Database**: The default choice for almost any modern application (Django, Rails, Node).
- **Complex Data**: When you need Relational + JSON (NoSQL) + Geo-spatial (PostGIS) in one DB.
- **Data Integrity**: When strictly typed schemas and ACID compliance are critical.

## Quick Start

```sql
-- JSONB column usage
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB
);

INSERT INTO events (data) VALUES ('{"type": "login", "user": "alice"}');

-- Query JSON directly (indexing supported)
SELECT * FROM events WHERE data->>'user' = 'alice';
```

## Core Concepts

### JSONB

Binary JSON storage. Faster to process and allows indexing.

```sql
CREATE INDEX idx_data ON events USING GIN (data);
```

### Common Table Expressions (CTEs)

Readable complex queries using `WITH`.

```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
)
SELECT * FROM regional_sales WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales);
```

### MVCC (Multi-Version Concurrency Control)

Postgres handles simultaneous access by keeping multiple versions of a row. Readers don't block writers, and writers don't block readers.

## Best Practices (2025)

**Do**:

- **Use `pgvector`**: For AI/ML vector embeddings storage (Postgres 17+ optimizations).
- **Use `GENERATE_SERIES`**: Great for generating test data or filling gaps in time-series reports.
- **Tune `work_mem`**: Default is low (4MB). Increase specific session `work_mem` for complex complex sort/hash operations.

**Don't**:

- **Don't use `NOT IN` with NULLs**: It often behaves counter-intuitively. Use `NOT EXISTS`.
- **Don't skip VACUUM**: Although autovacuum is good, heavy write loads may need tuning.

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [Postgres Weekly](https://postgresweekly.com/)
