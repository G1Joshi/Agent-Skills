---
name: influxdb
description: InfluxDB time-series database for metrics and IoT. Use for time-series data.
---

# InfluxDB

InfluxDB is a purpos-built time series database. Version 3.0 (IOx) is a complete rewrite in Rust, using Parquet/Arrow for massive performance gains.

## When to Use

- **IoT Metrics**: Sensor data from millions of devices.
- **DevOps Monitoring**: CPU, RAM, Disk usage over time.
- **Financial Ticks**: High frequency trading data.

## Quick Start (InfluxQL / SQL)

InfluxDB 3.0 supports SQL!

```sql
SELECT room, MEAN(temp)
FROM sensors
WHERE time > now() - 1h
GROUP BY room
```

## Core Concepts

### Push vs Pull

InfluxDB is "Push" based (Telegraf agents push data to it). Prometheus is "Pull" based.

### High Cardinality (v3)

The old InfluxDB struggled if you had too many "Tags" (Cardinality). The new IOx engine (Parquet-based) handles unlimited cardinality.

### Downsampling

Automatically aggregating high-resolution data (1s) into lower resolution (1m, 1h) to save space.

## Best Practices (2025)

**Do**:

- **Use SQL**: InfluxDB 3.0 prioritizes SQL (FlightSQL) over the old Flux language.
- **Use Parquet**: Understand that data is stored in Parquet (Object Storage friendly).
- **Tag wisely**: Even though v3 handles cardinality, proper schema design (Measurement vs Tag vs Field) still matters for query speed.

**Don't**:

- **Don't use Flux for new projects**: It is being deprecated in favor of SQL and Python.

## References

- [InfluxDB Documentation](https://docs.influxdata.com/)
