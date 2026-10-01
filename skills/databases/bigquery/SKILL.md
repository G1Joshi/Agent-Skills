---
name: bigquery
description: Expert Google Cloud BigQuery assistance covering standard SQL, partitioning, clustering, cost optimization, and ML. Use when running petabyte analytics queries, designing data warehouse schemas, or optimizing BI workloads.
---

# Google BigQuery

BigQuery is Google's serverless, highly scalable, and cost-effective multi-cloud data warehouse. It processes terabytes in seconds.

## When to Use

- **Serverless Enterprise Data Warehousing**: Querying petabytes of structured and semi-structured data with zero infrastructure management.
- **Real-Time Streaming Analytics**: Ingesting and querying millions of events per second with sub-second data freshness.
- **In-Database Machine Learning (BigQuery ML)**: Training and scoring regression, classification, and forecasting models using standard SQL.
- **Federated Multi-Cloud Queries (BigQuery Omni)**: Querying data stored in AWS S3 and Azure Blob Storage directly without egress replication.

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

### Capacitor Columnar Storage & Dremel Query Engine

Data is stored in proprietary Capacitor columnar format with dynamic tree-based Dremel execution slots:

```sql
-- Partitioned & Clustered Table DDL
CREATE OR REPLACE TABLE `my_project.analytics.user_events`
(
  event_id STRING,
  user_id STRING,
  event_name STRING,
  event_timestamp TIMESTAMP,
  metadata JSON
)
PARTITION BY DATE(event_timestamp)
CLUSTER BY user_id, event_name
OPTIONS(
  description="Partitioned clickstream events with clustering for point lookups",
  require_partition_filter=true
);
```

### Semi-Structured Native JSON Querying

Queries nested JSON attributes efficiently without schema migrations:

```sql
SELECT
  user_id,
  JSON_VALUE(metadata.device.os) AS os_name,
  JSON_EXTRACT_SCALAR(metadata, '$.cart.total') AS cart_total
FROM `my_project.analytics.user_events`
WHERE DATE(event_timestamp) = CURRENT_DATE()
  AND JSON_VALUE(metadata.action) = 'checkout';
```

### BigQuery ML Model Training

Trains and evaluates predictive models entirely inside SQL:

```sql
CREATE OR REPLACE MODEL `analytics.churn_prediction_model`
OPTIONS(model_type='logistic_reg', input_label_cols=['has_churned']) AS
SELECT
  total_spend,
  session_count,
  has_churned
FROM `analytics.customer_features`;
```

## Common Patterns

### Partitioning and Clustering for Cost-Optimized Queries

**Problem**: Full table scans across billions of event rows lead to astronomical query costs and high latency.

**Solution**:
Partition by date and cluster by high-cardinality lookup keys:

```sql
CREATE TABLE `project.analytics.events` (
  event_id STRING,
  user_id STRING,
  event_type STRING,
  event_timestamp TIMESTAMP
)
PARTITION BY DATE(event_timestamp)
CLUSTER BY user_id, event_type
OPTIONS (
  require_partition_filter = TRUE,
  partition_expiration_days = 365
);
```

## Best Practices

**Do**:

- Always Enforce `require_partition_filter=true`: Prevent runaway query billing by requiring users to specify date partitions in `WHERE` clauses.
- Cluster by High-Cardinality Filter Columns: Order tables by user ID, customer ID, or category to minimize scanned bytes.
- Use BigQuery Storage Write API: Stream real-time data using the gRPC-based Storage Write API for reduced cost and guaranteed atomicity.
- Inspect `Bytes Billed` in Query Validator: Check dry-run scanned byte estimates before executing heavy exploratory queries.

**Don't**:

- Use `SELECT *`: BigQuery charges per byte scanned; querying all columns drains query budgets.
- Use `ORDER BY` in subqueries: Global sorting requires single-node processing; sort only in the final outer query with `LIMIT`.
- Export large query results to single CSVs: Use partitioned wildcards (`EXPORT DATA OPTIONS(...)`) for multi-part exports.

## Troubleshooting

| Error                                       | Cause                                                                  | Solution                                                                                  |
| :------------------------------------------ | :--------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| `Cannot query without partition filter`     | `require_partition_filter` enabled but query lacked date WHERE clause. | Include `WHERE DATE(event_timestamp) >= 'YYYY-MM-DD'` in query.                           |
| `Resources exceeded during query execution` | Memory exhaustion from large skew in `JOIN` or `ORDER BY`.             | Pre-aggregate data, filter early, and avoid `ORDER BY` without `LIMIT`.                   |
| `Quota exceeded: Exceeded rate limits`      | Too many concurrent DDL/DML mutation queries per table.                | Batch append mutations using BigQuery Storage Write API rather than small single INSERTs. |

## References

- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
