---
name: snowflake
description: Snowflake cloud data warehouse with data sharing. Use for cloud analytics.
---

# Snowflake

Snowflake is a cloud-native data warehouse. It separates compute ("Virtual Warehouses") from storage, allowing them to scale independently.

## When to Use

- **Data Warehousing**: Central repository for all business data.
- **ELT Workflows**: Load raw data (JSON/CSV) then Transform it via SQL.
- **Data Sharing**: Securely share live data tables with other companies/accounts without copying.

## Quick Start (SQL)

```sql
-- Create warehouse (Compute)
CREATE WAREHOUSE my_wh WITH WAREHOUSE_SIZE = 'X-SMALL';

-- Query JSON directly (Variant type)
SELECT src:sales.order_id::integer
FROM raw_data;
```

## Core Concepts

### Virtual Warehouses

Compute clusters. You can have an XS warehouse for reporting and a 4XL warehouse for heavy ML training running simultaneously on the same data.

### Zero-Copy Cloning

Clone a Multi-Terabyte database in seconds for testing. It points to the same underlying S3 objects until changed.

### Snowpark

Allows writing code in Python/Java/Scala that executes inside Snowflake (for ML/Data Engineering).

## Best Practices (2025)

**Do**:

- **Use auto-suspend**: Shut down warehouses after X minutes of idleness to save money.
- **Use Variant Type**: Load semi-structured data (JSON) as-is into `VARIANT` columns, then parse on read.
- **Use Clustering Keys**: For very large tables (>1TB), manual clustering improves query skipping.

**Don't**:

- **Don't use `INSERT INTO ... VALUES`**: For bulk loading, use `COPY INTO` from S3/Stage. It is much faster.

## References

- [Snowflake Documentation](https://docs.snowflake.com/)
