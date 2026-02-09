---
name: postgresql
description: Comprehensive PostgreSQL expertise covering advanced SQL, window functions, CTEs, JSON operations, performance optimization, indexing, and security. Use for PostgreSQL databases and complex queries.
---

# PostgreSQL

Advanced PostgreSQL database development with performance optimization and best practices.

## When to Use

- Working with PostgreSQL databases
- Writing complex SQL queries with CTEs and window functions
- Optimizing query performance
- Designing database schemas

## Quick Start

```sql
-- Create table with constraints
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert with conflict handling
INSERT INTO users (email, name)
VALUES ('john@example.com', 'John')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;
```

## Core Concepts

### Window Functions

```sql
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) as month,
        customer_id,
        SUM(amount) as total_amount
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date), customer_id
)
SELECT
    month,
    customer_id,
    total_amount,
    RANK() OVER (PARTITION BY month ORDER BY total_amount DESC) as rank,
    LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY month) as prev_month
FROM monthly_sales;
```

### JSON Operations

```sql
SELECT
    id,
    data->>'name' as name,
    data->'tags' as tags,
    jsonb_array_length(data->'tags') as tag_count
FROM products
WHERE data @> '{"featured": true}'
  AND data ? 'category';
```

## Common Patterns

### Indexing Strategies

```sql
-- Partial index for filtered queries
CREATE INDEX CONCURRENTLY idx_active_users
ON users (email) WHERE is_active = true;

-- Composite index for covering queries
CREATE INDEX idx_orders_customer
ON orders (customer_id, created_at DESC)
INCLUDE (status, amount);

-- GIN index for JSONB
CREATE INDEX idx_products_data
ON products USING GIN (data);
```

### CTEs for Complex Queries

```sql
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 as level
    FROM categories WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

## Best Practices

**Do**:

- Use `EXPLAIN ANALYZE` to understand query plans
- Create indexes for frequently filtered columns
- Use CTEs for readable complex queries
- Use connection pooling (PgBouncer)

**Don't**:

- Use `SELECT *` in production
- Create indexes on every column
- Use `OFFSET` for pagination (use keyset)
- Store large BLOBs in database

## Troubleshooting

| Issue              | Cause                | Solution                 |
| ------------------ | -------------------- | ------------------------ |
| Slow query         | Missing index        | Check EXPLAIN, add index |
| Connection refused | Too many connections | Use connection pooling   |
| Lock timeout       | Long transaction     | Check pg_locks, optimize |

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Use The Index, Luke](https://use-the-index-luke.com/)
