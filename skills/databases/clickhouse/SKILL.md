---
name: clickhouse
description: ClickHouse columnar database for analytics. Use for real-time analytics.
---

# ClickHouse

ClickHouse is a columnar DBMS for Online Analytical Processing (OLAP). It is famous for allowing real-time generation of analytical reports using SQL queries on petabytes of data.

## When to Use

- **Real-time Analytics**: User-facing dashboards (Google Analytics style).
- **Log Management**: A cheaper, faster alternative to Elasticsearch/Splunk for logs (Observability).
- **Huge Throughput**: Ingesting millions of rows per second.

## Quick Start

```sql
SELECT
    toStartOfHour(EventTime) as Hour,
    count(),
    avg(Duration)
FROM events
GROUP BY Hour
ORDER BY Hour
```

## Core Concepts

### MergeTree Engine

The default table engine. Features primary keys (for sorting/skipping), data partitioning, and background data replication.

### Columnar Storage

Stores columns separately. If you select 5 columns out of 100, it only reads those 5 files.

### Vectorized Execution

Processes data in blocks (Vectors), maximizing CPU cache and SIMD usage.

## Best Practices (2025)

**Do**:

- **Insert in Batches**: Never insert row-by-row. Batch at least 1,000 rows.
- **Use Materialized Views**: ClickHouse MVs function like insert triggers. They calculate aggregations _on write_.
- **Use LowCardinality**: A data type key for strings with few unique values (Country, OS).

**Don't**:

- **Don't use it for OLTP**: No real transactions, updates/deletes are "mutations" (heavy async background processes).
- **Don't use standard joins for massive tables**: Use dictionaries or `JOIN` carefully (Right table must fit in RAM or use distributed join).

## References

- [ClickHouse Documentation](https://clickhouse.com/docs)
