---
name: sql
description: Expert SQL assistance covering ANSI SQL, CTEs, Window Functions, aggregation, indexing, and query optimization. Use when writing complex analytical queries, tuning query execution plans, or designing databases.
---

# SQL

Standard language for storing, manipulating and retrieving data in databases.

## When to Use

- **Relational Data Storage & ACID Transactions**: Financial ledgers, ERP systems, e-commerce checkouts, and customer databases.
- **Complex Analytical Queries & Aggregations**: Generating multi-dimensional business reports, cohorts, and funnels.
- **Hierarchical & Graph Data Traversal**: Querying organizational charts, bills of materials, and parent-child trees using recursive CTEs.
- **Semi-Structured Document Querying**: Using native JSON/JSONB indexing and operators in modern relational engines like PostgreSQL.

## Quick Start

```sql
-- Create Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- Insert Data
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Query Data
SELECT * FROM users WHERE name = 'Alice';
```

## Core Concepts

#Advanced Window Functions & Analytical Partitioning

Computing running totals, rankings, and lead/lag intervals across result partitions:

```sql
SELECT
    order_id,
    customer_id,
    order_date,
    amount_usd,
    -- Running cumulative sum per customer
    SUM(amount_usd) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    -- Rank customers by transaction size within their region
    DENSE_RANK() OVER (
        PARTITION BY region_code
        ORDER BY amount_usd DESC
    ) AS regional_rank,
    -- Difference from previous order
    amount_usd - LAG(amount_usd, 1, 0.0) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS diff_from_prev_order
FROM orders
WHERE order_date >= '2026-01-01';
```

#Hierarchical Tree Traversal with Recursive Common Table Expressions (CTEs)

Traversing nested organizational charts or bill-of-materials structures:

```sql
WITH RECURSIVE org_tree AS (
    -- Anchor member: top-level executives (no manager)
    SELECT
        employee_id,
        manager_id,
        full_name,
        title,
        1 AS depth,
        full_name AS hierarchy_path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive member: join subordinates
    SELECT
        e.employee_id,
        e.manager_id,
        e.full_name,
        e.title,
        ot.depth + 1,
        ot.hierarchy_path || ' -> ' || e.full_name
    FROM employees e
    INNER JOIN org_tree ot ON e.manager_id = ot.employee_id
)
SELECT * FROM org_tree ORDER BY hierarchy_path;
```

#JSONB Semi-Structured Operations & GIN Indexing

Querying nested payloads with indexed containment queries:

```sql
-- Create GIN index for high-speed containment lookup
CREATE INDEX idx_events_payload ON audit_events USING gin (payload jsonb_path_ops);

-- Query using JSONB operators
SELECT
    event_id,
    payload->>'action' AS action_name,
    payload->'user'->>'email' AS user_email,
    payload#>>'{metadata,ip_address}' AS client_ip
FROM audit_events
WHERE payload @> '{"action": "user.login", "status": "failed"}'
  AND (payload->'retry_count')::int > 3;
```

## Common Patterns

### Window Functions for Rolling Averages and Ranking

**Problem**: Computing running totals or ranking top performers requires multiple slow self-joins.

**Solution**:
Use SQL window functions (`OVER (PARTITION BY ... ORDER BY ...)`):

```sql
SELECT
  order_date,
  customer_id,
  order_amount,
  -- Running total per customer
  SUM(order_amount) OVER (
    PARTITION BY customer_id
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) as cumulative_spent,
  -- Rank orders by size per customer
  DENSE_RANK() OVER (
    PARTITION BY customer_id
    ORDER BY order_amount DESC
  ) as rank_by_amount
FROM orders;
```

## Best Practices (2026)

- **Do** always use parameterized queries and prepared statements in application code to completely neutralize SQL injection attacks.
- **Do** inspect query execution plans (`EXPLAIN (ANALYZE, BUFFERS)`) to verify index usage and eliminate sequential table scans.
- **Do** enforce referential integrity using foreign keys with appropriate `ON DELETE RESTRICT` or `ON DELETE CASCADE` rules.
- **Do** use appropriate column types: `TIMESTAMPTZ` for timestamps, `NUMERIC`/`DECIMAL` for financial currency, not floating point.
- **Don't** use `SELECT *` in production application queries; explicitly declare only needed columns to reduce network overhead.
- **Don't** perform calculations or wrap indexed columns in non-sargable functions in `WHERE` clauses (e.g. `WHERE DATE(created_at) = '2026-01-01'`).
- **Don't** run long-running batch migrations or table locks without timeouts (`SET statement_timeout = '5s'`).

## Troubleshooting

| Error                                             | Cause                                                               | Solution                                                               |
| :------------------------------------------------ | :------------------------------------------------------------------ | :--------------------------------------------------------------------- |
| `Column '...' must appear in the GROUP BY clause` | Non-aggregated column in SELECT without being included in GROUP BY. | Add column to GROUP BY or apply an aggregate function (`MIN`, `MAX`).  |
| `Subquery returns more than 1 row`                | Scalar subquery used with `=` operator returned multiple rows.      | Replace `=` with `IN` or add `LIMIT 1` in subquery.                    |
| `Division by zero`                                | Mathematical division with zero in denominator.                     | Use `NULLIF(denominator, 0)` to return NULL instead of throwing error. |

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
