---
name: timescaledb
description: Expert TimescaleDB time-series database assistance covering PostgreSQL hypertables, continuous aggregates, and data retention policies. Use when storing high-volume time-series telemetry, IoT metrics, or financial data.
---

# TimescaleDB

TimescaleDB is a time-series database built as an extension on top of PostgreSQL. It gives you the scale of NoSQL time-series with the reliability and tooling of Postgres.

## When to Use

- **High-Velocity Time-Series on PostgreSQL**: Ingesting and querying millions of metrics, IoT sensor data, and financial ticks within PostgreSQL.
- **Continuous Aggregations & Materialized Views**: Automatically computing real-time 1-minute, hourly, or daily rollups as data arrives.
- **Native Columnar Compression**: Reducing time-series storage footprints by 90%+ using chunk-level columnar compression.
- **Data Retention & Automated Tiering**: Automatically dropping or migrating historical time-series data to cold object storage.

## Quick Start

```sql
-- Convert standard table to hypertable
SELECT create_hypertable('conditions', 'time');

-- Query using standard SQL time-bucket functions
SELECT time_bucket('15 minutes', time) AS bucket,
       avg(temperature)
FROM conditions
GROUP BY bucket
ORDER BY bucket DESC;
```

## Core Concepts

#Hypertables & Automated Time Chunking

A hypertable exposes a unified SQL table interface while partitioning data into time-based chunks automatically in the background:

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE stock_ticks (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    volume INT NOT NULL
);

-- Convert to Hypertable with 1-day chunk intervals
SELECT create_hypertable('stock_ticks', 'time', chunk_time_interval => INTERVAL '1 day');
```

#Continuous Aggregates (Real-Time Rollups)

Maintains incrementally updated aggregate views that combine historical materializations with raw live incoming data:

```sql
CREATE MATERIALIZED VIEW stock_candlestick_1h
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    symbol,
    first(price, time) AS open_price,
    max(price) AS high_price,
    min(price) AS low_price,
    last(price, time) AS close_price,
    sum(volume) AS total_volume
FROM stock_ticks
GROUP BY bucket, symbol;
```

#Columnar Chunk Compression Policy

Automatically compresses chunks older than a specified duration into columnar format:

```sql
ALTER TABLE stock_ticks SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'time DESC'
);

-- Automatically compress data older than 7 days
SELECT add_compression_policy('stock_ticks', INTERVAL '7 days');
```

## Common Patterns

### Continuous Aggregates with Real-Time Materialization

**Problem**: Calculating hourly and daily aggregations across hundreds of millions of raw metric rows causes slow dashboard loading.

**Solution**:
Create a TimescaleDB continuous aggregate view:

```sql
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', recorded_at) AS bucket,
  device_id,
  avg(temperature) as avg_temp,
  max(temperature) as max_temp,
  count(*) as reading_count
FROM device_metrics
GROUP BY bucket, device_id;

-- Add automated refresh policy
SELECT add_continuous_aggregate_policy('metrics_hourly',
  start_offset => INTERVAL '3 days',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '30 minutes');
```

## Best Practices (2026)

**Do**:

- **Size Chunk Intervals to Fit in Memory**: Set `chunk_time_interval` so that the active chunk fits comfortably within the RAM buffer cache.
- **Segment Compression by Entity ID**: Use `compress_segmentby = 'symbol'` to enable rapid column-vector scans on specific entities.
- **Use Continuous Aggregates for Dashboards**: Query continuous aggregate views rather than scanning millions of raw rows in dashboards.
- **Define Automated Retention Policies**: Execute `add_retention_policy('stock_ticks', INTERVAL '90 days')` to purge old data automatically.

**Don't**:

- **Don't use unindexed secondary columns for filtering**: Always index auxiliary columns (`symbol`, `device_id`) used in query filters.
- **Don't mutate historical data in compressed chunks frequently**: Updating compressed chunks requires decompressing them, causing I/O spikes.
- **Don't run TimescaleDB without monitoring chunk count**: Having tens of thousands of tiny chunks degrades query planning performance.

## Troubleshooting

| Error                                            | Cause                                                                  | Solution                                                                        |
| :----------------------------------------------- | :--------------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| `table is not a hypertable`                      | Attempted TimescaleDB function on standard PostgreSQL table.           | Run `SELECT create_hypertable('tablename', 'time_column');`.                    |
| `Continuous aggregate view cannot be refreshed`  | Time column missing NOT NULL constraint or schedule interval conflict. | Ensure partitioning column is NOT NULL and policy offsets do not overlap.       |
| `Disk space exhaustion from uncompressed chunks` | Raw historical data chunks consuming excessive storage.                | Enable native compression: `ALTER TABLE tablename SET (timescaledb.compress);`. |

## References

- [TimescaleDB Documentation](https://docs.timescale.com/)
