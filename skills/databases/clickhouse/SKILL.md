---
name: clickhouse
description: Expert ClickHouse columnar database assistance covering MergeTree engines, materialized views, vector search, and real-time ingestion. Use when querying analytical telemetry, logs, time-series data, or building analytics APIs.
---

# ClickHouse

ClickHouse is a columnar DBMS for Online Analytical Processing (OLAP). It is famous for allowing real-time generation of analytical reports using SQL queries on petabytes of data.

## When to Use

- **Real-Time OLAP Analytics**: Aggregating billions of rows per second for real-time dashboards, security SIEMs, and web analytics.
- **High-Compression Columnar Storage**: Compressing raw event logs by 80-90% using LZ4 and ZSTD column-level codecs.
- **Ad-Hoc Analytical Queries**: Executing complex aggregations, window functions, and multi-billion-row vector queries in milliseconds.
- **Observability Data Stores**: Powering log and trace storage backends (e.g. replacing Elasticsearch for OpenTelemetry metrics and logs).

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

### MergeTree Engine Family

The foundational storage engine for ClickHouse; writes data in immutable sorted parts and merges them asynchronously in the background:

```sql
CREATE TABLE analytics.page_views
(
    event_time DateTime64(3, 'UTC'),
    site_id UInt32,
    user_id UUID,
    url_path LowCardinality(String),
    response_time_ms UInt16,
    user_agent String CODEC(ZSTD(3))
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (site_id, event_time, user_id)
SETTINGS index_granularity = 8192;
```

### Materialized Views with AggregatingMergeTree

Precomputes rolling aggregations at insertion time with zero background batch job overhead:

```sql
-- Pre-aggregated Hourly Metrics
CREATE TABLE analytics.hourly_traffic
(
    hour DateTime,
    site_id UInt32,
    total_views SimpleAggregateFunction(sum, UInt64),
    unique_visitors AggregateFunction(uniq, UUID)
)
ENGINE = AggregatingMergeTree()
ORDER BY (site_id, hour);

CREATE MATERIALIZED VIEW analytics.hourly_traffic_mv TO analytics.hourly_traffic AS
SELECT
    toStartOfHour(event_time) AS hour,
    site_id,
    count() AS total_views,
    uniqState(user_id) AS unique_visitors
FROM analytics.page_views
GROUP BY hour, site_id;
```

### Vectorized SIMD Query Execution

ClickHouse processes data in vectorized arrays of column primitives, utilizing hardware CPU SIMD instructions to aggregate millions of values per cycle:

```sql
-- Sub-10ms aggregation over 50,000,000 rows
SELECT
    url_path,
    count() AS hits,
    quantile(0.95)(response_time_ms) AS p95_latency
FROM analytics.page_views
WHERE event_time >= now() - INTERVAL 24 HOUR
GROUP BY url_path
ORDER BY hits DESC
LIMIT 10;
```

## Common Patterns

### ReplacingMergeTree for Deduplicated Real-Time Analytics

**Problem**: High-speed real-time event streaming frequently delivers duplicate logs or updated state rows.

**Solution**:
Use `ReplacingMergeTree` with primary sorting key:

```sql
CREATE TABLE telemetry.sensor_metrics (
  sensor_id UInt32,
  recorded_at DateTime64(3),
  reading Float64,
  version UInt64
)
ENGINE = ReplacingMergeTree(version)
ORDER BY (sensor_id, recorded_at);

-- Query latest state across parts
SELECT sensor_id, recorded_at, reading
FROM telemetry.sensor_metrics FINAL
WHERE sensor_id = 101;
```

## Best Practices

**Do**:

- Insert in Large Batches: Stream data in batches of 10,000 to 100,000 rows (or at 1-second intervals) to prevent creating excessive small parts.
- Use `LowCardinality(String)`: Compress string columns with fewer than 10,000 unique values into indexed integer dictionaries.
- Order by Most-Filtered Columns First: Arrange primary sort keys from lowest cardinality to highest cardinality (`site_id`, `event_time`, `user_id`).
- Use `ReplacingMergeTree` for Deduplication: Deduplicate rows based on version numbers during background merges.

**Don't**:

- Perform single-row `INSERT` statements: Inserting single rows overwhelms the MergeTree engine and exhausts filesystem inodes.
- Use ClickHouse for transactional OLTP: ClickHouse does not support ACID row locking, single-record updates, or foreign key cascades.
- Create too many partitions: Keep partition counts under 1,000 per table; partition by month (`toYYYYMM`) rather than day.

## Troubleshooting

| Error                                 | Cause                                                               | Solution                                                                              |
| :------------------------------------ | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------ |
| `Too many parts in all data in table` | Ingesting too many tiny micro-batches instead of large batches.     | Buffer writes into batches of 10,000+ rows or use an asynchronous insert buffer.      |
| `Memory limit exceeded for query`     | Query scanning uncompressed memory without proper partition filter. | Add `WHERE` filter on the primary key sorting prefix, or increase `max_memory_usage`. |
| `DB::Exception: Cannot parse input`   | Schema type mismatch during CSV/JSON ingestion.                     | Verify data format and use `input_format_skip_unknown_fields = 1`.                    |

## References

- [ClickHouse Documentation](https://clickhouse.com/docs)
