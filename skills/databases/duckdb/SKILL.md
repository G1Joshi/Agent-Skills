---
name: duckdb
description: DuckDB analytical database for OLAP workloads. Use for embedded analytics.
---

# DuckDB

DuckDB is "SQLite for Analytics". It is an in-process SQL OLAP database. It runs inside your application process and is blazing fast for analytical queries on local files (Parquet, CSV, JSON).

## When to Use

- **Local Analytics**: Analyze millions of rows on your laptop in seconds.
- **Data Engineering**: Process data in Python/R pipelines (replacement for Pandas).
- **Serverless Data Lake**: Query S3 parquet files directly via Lambda without a running warehouse.

## Quick Start (Python)

```python
import duckdb

# Query local CSV directly
duckdb.sql("SELECT avg(price) FROM 'sales.csv' WHERE region='US'").show()

# Connect to S3
duckdb.sql("INSTALL httpfs; LOAD httpfs;")
duckdb.sql("SELECT count(*) FROM 's3://my-bucket/data.parquet'")
```

## Core Concepts

### Vectorized Execution

Standard DBs process row-by-row. DuckDB processes batches of columns (Vectors), utilizing modern CPU SIMD instructions.

### Universal Format Reader

Can query CSV, JSON, Parquet, Arrow, SQLite, and Postgres tables as if they were local tables.

### Zero Dependencies

Single binary/library.

## Best Practices (2025)

**Do**:

- **Use Parquet**: It is the native language of analytics. DuckDB + Parquet is incredible.
- **Replace Pandas**: For datasets larger than RAM, DuckDB works (Disk spilling) where Pandas crashes.
- **Use explicitly typed SQL**: DuckDB’s SQL dialect is very friendly and standard (Postgres-compatible).

**Don't**:

- **Don't use for Multi-User OLTP**: It handles concurrency poorly (single writer). Use Postgres for that. Use DuckDB for analysis.

## References

- [DuckDB Documentation](https://duckdb.org/docs/)
