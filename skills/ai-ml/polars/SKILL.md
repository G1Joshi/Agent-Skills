---
name: polars
description: Expert Polars data manipulation assistance covering blazing-fast Rust-native execution, LazyFrames, expressions, and zero-copy Arrow memory. Use when processing millions of tabular rows in Python with minimal latency.
---

# Polars

Polars is the fast successor to Pandas. Written in Rust, query-optimized, and parallelized. v1.0 (2024) signaled production readiness.

## When to Use

- **High-Performance In-Memory & Streaming Dataframes**: Rust-backed, multi-threaded columnar data processing 5x-30x faster than Pandas.
- **Out-of-Core Larger-Than-Memory Analytics**: Streaming datasets larger than RAM with the Polars Lazy API (`collect(streaming=True)`).
- **Parallel Query Execution**: Automatic query optimization, predicate pushdown, and projection pushdown via the Catalyst-like engine.
- **Zero-Copy Apache Arrow Interoperability**: Seamlessly sharing memory with PyTorch, DuckDB, and Parquet readers.

## Quick Start

```python
import polars as pl

# Fast lazy query execution pipeline
lazy_df = (
    pl.scan_csv("sales_data.csv")
    .filter(pl.col("amount") > 100)
    .group_by("region")
    .agg([
        pl.col("amount").sum().alias("total_sales"),
        pl.col("customer_id").n_unique().alias("unique_customers")
    ])
    .sort("total_sales", descending=True)
)

# Optimize and execute in parallel across all CPU cores
result = lazy_df.collect()
print(result)
```

## Core Concepts

#Lazy Execution & Query Optimization

Building optimized query graphs that execute only when requested:

```python
import polars as pl

# Create LazyFrame scanning Parquet files without immediate loading
lazy_query = (
    pl.scan_parquet("s3://warehouse/transactions/*.parquet")
    .filter(pl.col("status") == "completed")
    .filter(pl.col("transaction_date") >= pl.date(2026, 1, 1))
    .with_columns([
        (pl.col("amount_cents") / 100.0).alias("amount_usd"),
        pl.col("transaction_date").dt.month().alias("month")
    ])
    .group_by(["month", "merchant_category"])
    .agg([
        pl.col("amount_usd").sum().alias("total_revenue"),
        pl.col("amount_usd").mean().alias("avg_transaction"),
        pl.len().alias("transaction_count")
    ])
    .sort("total_revenue", descending=True)
)

# Inspect optimized execution plan
print(lazy_query.explain())

# Execute query in parallel and return eager DataFrame
result_df = lazy_query.collect()
print(result_df)
```

#Expressive Column Expressions (pl.col)

Composing clean, vector operations inside expressions:

```python
df = pl.DataFrame({
    "user_id": [101, 102, 103, 104, 105],
    "spend": [120.0, 450.0, 89.0, 950.0, 210.0],
    "tier": ["silver", "gold", "bronze", "platinum", "silver"]
})

# Add conditional flags and normalized scores
enhanced_df = df.with_columns([
    pl.when(pl.col("spend") > 400.0)
      .then(pl.lit("VIP"))
      .otherwise(pl.lit("Standard"))
      .alias("customer_segment"),
    ((pl.col("spend") - pl.col("spend").mean()) / pl.col("spend").std()).alias("z_score")
])
print(enhanced_df)
```

#Streaming Mode for Terabyte-Scale Datasets

Processing larger-than-RAM files in memory-managed batches:

```python
# Streaming mode processes data in chunks through CPU cache
streamed_metrics = (
    pl.scan_csv("massive_web_logs.csv")
    .group_by("ip_address")
    .agg(pl.len().alias("hit_count"))
    .collect(streaming=True) # Enables streaming out-of-core engine
)
```

## Common Patterns

### High-Speed Expression Contexts (Select, With_Columns, When/Then)

**Problem**: Writing complex row-wise condition logic without Python loop performance degradation.

**Solution**:
Use Polars native `when / then / otherwise` expression trees:

```python
df = pl.DataFrame({
    "price": [10.0, 50.0, 150.0, 20.0],
    "quantity": [1, 2, 5, 0]
})

result = df.with_columns(
    tier=pl.when(pl.col("price") > 100).then(pl.lit("Premium"))
           .when(pl.col("price") > 25).then(pl.lit("Standard"))
           .otherwise(pl.lit("Budget")),
    total=(pl.col("price") * pl.col("quantity"))
)
```

## Best Practices (2026)

- **Do** favor `pl.scan_parquet()` / `pl.scan_csv()` and LazyFrames over eager `pl.read_*()` for large workloads.
- **Do** use `collect(streaming=True)` for datasets that approach or exceed system RAM limits.
- **Do** compose transformations inside a single `.with_columns()` or `.select()` call to enable automatic parallelization.
- **Do** use Polars native expressions (`pl.col(...)`) instead of Python lambdas or `.map_elements()`.
- **Don't** use `.map_elements()` or `.apply()` unless strictly necessary; Python callbacks break Rust parallel execution.
- **Don't** convert Polars DataFrames to Pandas unless required by a legacy library; use PyArrow for zero-copy transfers.
- **Don't** call `.collect()` repeatedly inside loops; accumulate the query graph and evaluate once.

## Troubleshooting

| Error                                                         | Cause                                                                 | Solution                                                         |
| :------------------------------------------------------------ | :-------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `ComputeError: cannot evaluate expression on empty dataframe` | Query filter removed all rows before subsequent non-null computation. | Check filter criteria or guard with `if len(df) > 0:`.           |
| `SchemaMismatchError during concat`                           | Concatenating LazyFrames with differing column types.                 | Cast column types explicitly with `pl.col('id').cast(pl.Int64)`. |
| `Out of memory in collect()`                                  | Entire dataset loaded into memory simultaneously.                     | Enable streaming engine: `lazy_df.collect(streaming=True)`.      |

## References

- [Polars Documentation](https://pola.rs/)
