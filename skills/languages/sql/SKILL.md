---
name: sql
description: SQL database queries, joins, aggregations, subqueries, and optimization. Use for .sql files and database operations.
---

# SQL

Standard language for storing, manipulating and retrieving data in databases.

## When to Use

- Relational data modeling
- Complex queries and aggregations
- Data integrity enforcement (ACID)
- Standardized data access

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

### DDL (Data Definition Language)

Commands to define database schemas (CREATE, ALTER, DROP).

### DML (Data Manipulation Language)

Commands to manipulate data (SELECT, INSERT, UPDATE, DELETE).

### Joins

Combining rows from two or more tables based on a related column.

- **INNER JOIN**: Matches in both tables.
- **LEFT JOIN**: All from left, matches from right.

## Best Practices

**Do**:

- Use parameterized queries (prevent SQL Injection)
- Index columns used in WHERE and JOIN clauses
- Use transactions for atomic operations

**Don't**:

- Use `SELECT *` in production (fetch only what you need)
- Store logic in triggers if possible (hard to debug)
- Ignore execution plans for slow queries

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
