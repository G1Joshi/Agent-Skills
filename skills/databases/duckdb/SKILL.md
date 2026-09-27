---
name: duckdb
description: Expert DuckDB analytical database assistance covering embedded SQL, Parquet querying, Arrow integration, and vectorized execution. Use when running in-process OLAP, analyzing local datasets, or processing pandas/polars data.
---

# DuckDB

DuckDB is "SQLite for Analytics". It is an in-process SQL OLAP database. It runs inside your application process and is blazing fast for analytical queries on local files (Parquet, CSV, JSON).

## When to Use

- **In-Process Fast Analytical SQL (OLAP)**: The "SQLite for Analytics" — running lightning-fast columnar queries directly inside Python, Node.js, or Rust.
- **Direct Parquet, Arrow & CSV Querying**: Querying external Parquet files, S3 buckets, and Arrow tables without importing them into a database.
- **Local Data Science & Jupyter Notebooks**: Replacing complex Pandas/Polars memory-intensive wrangling with blazing-fast vectorized SQL.
- **Zero-Infrastructure Data Pipelines**: Building serverless ETL data transformations in AWS Lambda or local CLI scripts.

## Quick Start

```python
import duckdb

# Query local CSV directly
duckdb.sql("SELECT avg(price) FROM 'sales.csv' WHERE region='US'").show()

# Connect to S3
duckdb.sql("INSTALL httpfs; LOAD httpfs;")
duckdb.sql("SELECT count(*) FROM 's3://my-bucket/data.parquet'")
```

## Core Concepts

#Direct In-Place Parquet & S3 Scanning

DuckDB queries compressed Parquet files directly from local disk or remote S3 without loading them into database storage:

```sql
-- Query millions of rows directly from remote S3 Parquet file
INSTALL httpfs;
LOAD httpfs;

SELECT
  geo_country,
  count() AS visitor_count,
  avg(session_duration) AS avg_duration
FROM read_parquet('s3://my-analytics-bucket/logs/2026/09/*.parquet')
WHERE event_name = 'conversion'
GROUP BY geo_country
ORDER BY visitor_count DESC
LIMIT 10;
```

#Zero-Copy Apache Arrow Integration

Passes data between Python/Pandas/Polars and DuckDB memory structures with zero serialization overhead:

```python
import duckdb
import pyarrow as pa

# Zero-copy query over Arrow Table
table = pa.Table.from_arrays(...)
rel = duckdb.arrow(table)
result_df = rel.filter("revenue > 10000").aggregate("sum(revenue)", "region").df()
```

#Persistent Single-File Database Storage

Stores gigabytes of relational data in a single, high-compression, portable file:

```python
import duckdb

conn = duckdb.connect("analytics.duckdb")
conn.execute("CREATE TABLE users AS SELECT * FROM read_csv_auto('users.csv')")
print(conn.execute("SELECT count(*) FROM users").fetchall())
conn.close()
```

## Common Patterns

### Direct Querying of S3 / Local Parquet Files Without Loading

**Problem**: Converting large Parquet or CSV files into database tables takes unnecessary disk space and time.

**Solution**:
Query remote or local files directly using vectorized scans:

```python
import duckdb

conn = duckdb.connect()

# Query millions of rows directly from globbed Parquet files
df = conn.execute("""
    SELECT
        product_category,
        count(*) as total_orders,
        avg(sale_price) as avg_price
    FROM 'data/sales_*.parquet'
    WHERE order_date >= '2025-01-01'
    GROUP BY product_category
    ORDER BY total_orders DESC
    LIMIT 10
""").df()

print(df)
```

## Best Practices (2026)

**Do**:

- **Query Parquet Files Directly**: Benefit from Parquet metadata column projection and predicate pushdown.
- **Use Memory Limits in Constrained Environments**: Set `SET max_memory = '4GB'` to prevent out-of-memory errors in serverless containers.
- **Leverage Vectorized Execution**: Write declarative analytical aggregations (`SUM`, `AVG`, `WINDOW`) to utilize hardware CPU SIMD parallelism.
- **Use DuckDB Extensions**: Utilize extensions (`httpfs`, `aws`, `spatial`, `json`, `sqlite`) dynamically via `INSTALL` and `LOAD`.

**Don't**:

- **Don't use DuckDB for high-concurrency multi-client OLTP**: DuckDB is an in-process analytical engine; do not run concurrent multi-client web applications on it.
- **Don't read CSV files repeatedly in production loops**: Convert raw CSV files to Parquet once; Parquet queries are 20-50x faster.
- **Don't leave database file handles unclosed**: Ensure `conn.close()` executes to prevent locking the database file on disk.

## Troubleshooting

| Error                                               | Cause                                                          | Solution                                                                                  |
| :-------------------------------------------------- | :------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| `Out of Memory Error: memory limit exceeded`        | Query dataset exceeds default memory limit.                    | Set `conn.execute("SET max_memory = '8GB'")` and enable temp directory for spill-to-disk. |
| `Catalog Error: Table with name ... already exists` | Attempting to recreate persistent table without IF NOT EXISTS. | Use `CREATE TABLE IF NOT EXISTS` or `CREATE OR REPLACE TABLE`.                            |
| `IO Error: Cannot open file`                        | File path typo or missing AWS credentials when querying S3.    | Install `httpfs` extension and configure `s3_region` and credentials.                     |

## References

- [DuckDB Documentation](https://duckdb.org/docs/)
