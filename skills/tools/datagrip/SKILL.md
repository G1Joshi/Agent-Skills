---
name: datagrip
description: DataGrip database IDE from JetBrains. Use for database management.
---

# DataGrip

DataGrip is the database IDE. It supports PostgreSQL, MySQL, Redis, Mongo, Snowflake, BigQuery, and more.

## When to Use

- **SQL Development**: Writing complex queries with auto-complete that knows your schema.
- **Data Exploration**: Viewing tables, filtering, exporting to CSV/JSON.
- **Schema Management**: Generating DDL scripts, visualizing diagrams.

## Core Concepts

### Data Sources

Drivers for connections. Auto-downloads JDBC drivers.

### Console

The query editor. Ctrl+Enter executes current statement.

### Introspection

It downloads metadata about tables/columns so auto-complete works offline.

## Best Practices (2025)

**Do**:

- **Use "Compare Structure"**: Diff two databases (e.g. Prod vs Staging) and generate migration scripts.
- **Use Visualizer**: Right click a result set -> "Show Visualization" (Charts).
- **Use Color Settings**: Set "Prod" transparent red to avoid accidental drops.

**Don't**:

- **Don't `UPDATE` without `WHERE`**: DataGrip warns you. Listen to it.

## References

- [DataGrip Documentation](https://www.jetbrains.com/datagrip/documentation/)
