---
name: timescaledb
description: TimescaleDB PostgreSQL for time-series. Use for time-series on Postgres.
---

# TimescaleDB

TimescaleDB is a time-series database built as an extension on top of PostgreSQL. It gives you the scale of NoSQL time-series with the reliability and tooling of Postgres.

## When to Use

- **SQL familiarity**: You want time-series but already know SQL and use Postgres drivers.
- **Relational + Time**: You need to JOIN your sensor data (Time Series) with Device metadata (Relational Tables).
- **Compression**: Highest-in-class compression (90%+) for historical data.

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

### Hypertables

The abstraction layer. It looks like a single table, but effectively partitions data into chunks by time interval.

### Continuous Aggregates

Real-time materialized views. "Keep a running average of temperature per hour". It updates incrementally.

### Compression

Columnar compression on old chunks. Turns row-based Postgres pages into highly compressed columnar arrays.

## Best Practices (2025)

**Do**:

- **Enable Compression**: It improves query speed (less I/O) and saves massive disk space.
- **Use Tiered Storage**: Keep recent hot data on SSD, move compressed old data to S3 (Bottomless storage in cloud).
- **Join tables**: Use the power of Postgres to join your metrics with your business data.

**Don't**:

- **Don't update compressed chunks**: Updating old, compressed data is slow (Copy-on-write). Design for append-only patterns.

## References

- [TimescaleDB Documentation](https://docs.timescale.com/)
