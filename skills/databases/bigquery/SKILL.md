---
name: bigquery
description: Google BigQuery for analytics, ML, and data warehousing. Use for large-scale analytics.
---

# Google BigQuery

BigQuery is Google's serverless, highly scalable, and cost-effective multi-cloud data warehouse. It processes terabytes in seconds.

## When to Use

- **Serverless Analytics**: No infrastructure to manage. Just run SQL.
- **Real-time Analytics**: High-speed streaming ingestion.
- **ML Integration**: `CREATE MODEL` lets you train ML models using standard SQL (BigQuery ML).

## Quick Start

```sql
-- Standard SQL
SELECT name, COUNT(*) as count
FROM `bigquery-public-data.usa_names.usa_1910_2013`
GROUP BY name
ORDER BY count DESC
LIMIT 10;
```

## Core Concepts

### Slots and Reservations

A "Slot" is a unit of computational capacity. BigQuery autoscales slots, or you can reserve them for flat-rate pricing.

### Columnar Storage (Capacitor)

Optimized for aggregation queries. Reading one column is much cheaper/faster than reading all columns (`SELECT *` is expensive).

### Partitioning & Clustering

- **Partitioning**: Splits table by Date/Int (e.g., Daily partitions). Prunes data scanning massive cost savings.
- **Clustering**: Sorts data within partitions for faster filtering.

## Best Practices (2025)

**Do**:

- **Partition by Date**: Almost mandatory for time-series logs.
- **Use BigQuery ML**: Train models (Regression, K-Means) directly where data lives.
- **Estimate Cost**: `Dry Run` your query to see how many bytes it will scan before running it.

**Don't**:

- **Don't run `SELECT *`**: You pay per column read. Select only what you need.
- **Don't treat it like an OLTP**: Single row inserts are slow (unless using Streaming API). It is for bulk analytics.

## References

- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
