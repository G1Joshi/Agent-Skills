---
name: mysql
description: MySQL relational database with InnoDB, replication, stored procedures, and performance optimization. Use for MySQL operations.
---

# MySQL

MySQL database development with InnoDB optimization and best practices.

## When to Use

- Working with MySQL databases
- Building applications with LAMP/LEMP stack
- Legacy database maintenance
- Multi-database replication setups

## Quick Start

```sql
-- Create table with InnoDB
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Core Concepts

### Indexing

```sql
-- Composite index
CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date DESC);

-- Covering index
CREATE INDEX idx_users_lookup
ON users (email) INCLUDE (name, status);

-- Full-text index
CREATE FULLTEXT INDEX idx_products_search
ON products (name, description);

-- Check index usage
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

### Joins and Subqueries

```sql
-- Optimized join
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.is_active = 1
GROUP BY u.id, u.name
HAVING order_count > 5;

-- Correlated subquery alternative
SELECT u.name,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u
WHERE u.is_active = 1;
```

## Common Patterns

### Transactions

```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Check for errors before committing
COMMIT;
-- Or ROLLBACK; on error
```

### Stored Procedures

```sql
DELIMITER //
CREATE PROCEDURE GetUserOrders(IN userId INT)
BEGIN
    SELECT o.*, u.name as customer_name
    FROM orders o
    JOIN users u ON o.user_id = u.id
    WHERE o.user_id = userId
    ORDER BY o.created_at DESC;
END //
DELIMITER ;

CALL GetUserOrders(123);
```

## Best Practices

**Do**:

- Use InnoDB engine for transactions
- Use `utf8mb4` for full Unicode support
- Create indexes for WHERE/JOIN columns
- Use prepared statements

**Don't**:

- Use `SELECT *` in production
- Store passwords in plain text
- Use MyISAM for new tables
- Over-index small tables

## Troubleshooting

| Issue                | Cause                 | Solution                      |
| -------------------- | --------------------- | ----------------------------- |
| Slow query           | Full table scan       | Add appropriate index         |
| Deadlock             | Conflicting row locks | Reorder operations, use retry |
| Too many connections | Connection leak       | Use connection pooling        |

## References

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Percona Blog](https://www.percona.com/blog/)
