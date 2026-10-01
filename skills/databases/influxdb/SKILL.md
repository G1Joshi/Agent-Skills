---
name: influxdb
description: Expert InfluxDB time-series assistance covering Line Protocol, Flux/InfluxQL, retention policies, downsampling, and bucket management. Use when storing IoT metrics, application telemetry, or financial time-series data.
---

# InfluxDB

InfluxDB is a purpos-built time series database. Version 3.0 (IOx) is a complete rewrite in Rust, using Parquet/Arrow for massive performance gains.

## When to Use

- **High-Velocity Time-Series Ingestion**: Ingesting continuous metrics, sensor telemetry, system diagnostics, and financial tick data.
- **Downsampling & Data Retention Policies**: Automatically aggregating high-resolution raw data into long-term rollups while purging raw logs.
- **IoT & Sensor Monitoring**: Storing time-indexed metrics from IoT hardware, energy grids, and manufacturing sensors.
- **DevOps Infrastructure Observability**: Collecting server and container performance metrics via Telegraf and visualizing in Grafana.

## Quick Start

InfluxDB 3.0 supports SQL!

```sql
SELECT room, MEAN(temp)
FROM sensors
WHERE time > now() - 1h
GROUP BY room
```

## Core Concepts

### Line Protocol Data Ingestion

The compact text format for streaming time-series data:

```http
# Syntax: <measurement>,<tag_set> <field_set> <timestamp>
cpu_usage,host=serverA,region=us-east idle=84.2,system=3.8,user=12.0 1727420400000000000
mem_usage,host=serverA,region=us-east used_percent=64.1 1727420400000000000
```

### InfluxQL / SQL Engine Architecture (InfluxDB 3.0 / IOx)

Powered by Apache Arrow and DataFusion, supporting standard SQL over columnar Parquet files:

```sql
-- Query time-series telemetry in InfluxDB 3.0 SQL
SELECT
  date_bin(INTERVAL '5 minutes', time) AS window_time,
  host,
  avg(idle) AS avg_idle_cpu,
  max(user) AS peak_user_cpu
FROM cpu_usage
WHERE time >= now() - INTERVAL '6 hours'
  AND region = 'us-east'
GROUP BY window_time, host
ORDER BY window_time DESC;
```

### Tags vs Fields (Index Cardinality)

- **Tags**: Indexed metadata strings (e.g. `host`, `datacenter`, `environment`). Used for fast filtering and grouping.
- **Fields**: Unindexed metrics values (e.g. `temperature`, `cpu_usage`, `memory_bytes`). Stored as columnar values.

## Common Patterns

### Line Protocol Ingestion with Nanosecond Precision

**Problem**: High-throughput telemetry ingestion bottlenecks when formatted as bloated JSON objects.

**Solution**:
Use compact InfluxDB Line Protocol:

```bash
# Line Protocol syntax: measurement,tag_set field_set timestamp
curl -XPOST "http://localhost:8086/api/v2/write?bucket=telemetry&org=myorg"   -H "Authorization: Token $INFLUX_TOKEN"   --data-raw 'cpu_usage,host=server01,region=us-west cpu_idle=72.5,cpu_system=12.1 1711530000000000000'
```

## Best Practices

**Do**:

- Adopt InfluxDB 3.0: Migrate to the modern Apache Arrow-based InfluxDB 3.0 engine with standard SQL support.
- Keep Tag Cardinality Constrained: Never store high-cardinality values (UUIDs, timestamps, raw URLs) as tags; store them as fields.
- Write in Batches: Transmit points in batches of 1,000 to 5,000 lines over gRPC or HTTP to optimize network throughput.
- Configure Retention Policies: Define retention rules (e.g. 30 days for raw data, 1 year for downsampled rollups) to control disk usage.

**Don't**:

- Store timestamps in fields: The timestamp is a native first-class attribute; use line protocol timestamps.
- Send single-point HTTP writes: Writing individual points creates severe network overhead and CPU thrashing.
- Create unbounded tag keys: High cardinality tags explode memory usage in the time-series index (TSI).

## Troubleshooting

| Error                                      | Cause                                                               | Solution                                                                            |
| :----------------------------------------- | :------------------------------------------------------------------ | :---------------------------------------------------------------------------------- |
| `write: series cardinality limit exceeded` | Creating too many unique tag combinations (e.g. using UUID as tag). | Move high-cardinality values (IDs, hashes) from tags to fields.                     |
| `401 Unauthorized`                         | Missing or invalid InfluxDB 2.x API authentication token.           | Pass header `Authorization: Token <token>` with bucket write permissions.           |
| `rejected line protocol syntax`            | Formatting error in measurement, tag comma, or field type mismatch. | Check string escaping and ensure integers are suffixed with `i` (e.g. `count=42i`). |

## References

- [InfluxDB Documentation](https://docs.influxdata.com/)
