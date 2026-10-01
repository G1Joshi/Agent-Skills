---
name: cassandra
description: Expert Apache Cassandra assistance covering CQL, partition keys, clustering columns, tombstone avoidance, and nodetool. Use when designing linear scale data stores, high-write ingestion engines, or tuning consistency levels.
---

# Apache Cassandra

Cassandra is a wide-column store database designed for scalability and high availability without compromising performance. Linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data.

## When to Use

- **High-Velocity Write Ingestion**: Logging millions of writes per second across IoT sensor streams, messaging systems, and time-series metrics.
- **Zero-Downtime Multi-Datacenter Replication**: Geographically distributed systems requiring peer-to-peer active-active masterless replication.
- **Linear Horizontal Scalability**: Scaling throughput predictably by adding commodity hardware nodes without cluster downtime.
- **Predictable Query Latency**: Serving high-concurrency key-value and partition-key lookups under 5 milliseconds.

## Quick Start

```sql
CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  name text,
  email text
);

INSERT INTO users (user_id, name) VALUES (uuid(), 'Alice');
```

## Core Concepts

### Masterless Ring Architecture & Consistent Hashing

Every node in the cluster is identical; partition tokens dictate which nodes own primary and replica data:

```text
[ Node 1 (Token: 0) ] ────→ [ Node 2 (Token: 33) ] ────→ [ Node 3 (Token: 66) ]
          ▲                                                           │
          └───────────────────────────────────────────────────────────┘
```

### Partition Keys vs Clustering Columns (CQL)

The partition key determines physical node placement; clustering columns determine on-disk sorting within the partition:

```sql
-- Sensor Telemetry Schema
CREATE KEYSPACE telemetry_data
WITH replication = {'class': 'NetworkTopologyStrategy', 'us-east': 3, 'eu-west': 3};

CREATE TABLE telemetry_data.sensor_readings (
    sensor_id UUID,
    recorded_date DATE,
    recorded_at TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE,
    PRIMARY KEY ((sensor_id, recorded_date), recorded_at)
) WITH CLUSTERING ORDER BY (recorded_at DESC);
```

### Tunable Consistency Levels (CAP Theorem)

Balance latency against strict consistency on a per-query basis:

```sql
-- Read and Write Consistency Levels
CONSISTENCY LOCAL_QUORUM; -- Strong consistency within the local datacenter
SELECT * FROM telemetry_data.sensor_readings
WHERE sensor_id = 8f3d1e1c-3a62-47cf-a98b-7d12a9e32049
  AND recorded_date = '2026-09-27'
LIMIT 50;
```

## Common Patterns

### Query-First Primary Key Design

**Problem**: Cassandra cannot perform relational joins or arbitrary filtering without scanning whole partitions.

**Solution**:
Design primary keys composed of partition key (distribution) and clustering columns (sorting):

```sql
CREATE KEYSPACE ecommerce WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'us-east': 3
};

CREATE TABLE ecommerce.orders_by_user (
  user_id uuid,
  order_time timestamp,
  order_id uuid,
  total_cents bigint,
  PRIMARY KEY ((user_id), order_time, order_id)
) WITH CLUSTERING ORDER BY (order_time DESC);
```

## Best Practices

**Do**:

- Design Tables Around Queries (Query-First Modeling): Create dedicated denormalized tables for each specific query requirement.
- Keep Partition Sizes Under 100MB: Ensure partition rows do not grow indefinitely; incorporate time buckets (date, month) into composite partition keys.
- Use `LOCAL_QUORUM` for Multi-DC Clusters: Guarantee strong consistency locally without incurring cross-ocean WAN latency.
- Run Regular Repair Jobs with Reaper: Run incremental repairs to reconcile tombstones and out-of-sync replicas.

**Don't**:

- Use `ALLOW FILTERING` in production queries: Scanning across multiple node partitions destroys Cassandra's sub-millisecond guarantees.
- Perform bulk deletions: Deletions create tombstone markers that degrade read performance and cause JVM garbage collection pauses.
- Use Cassandra as an analytical SQL database: Avoid joins, aggregation queries, and ad-hoc multi-table scans.

## Troubleshooting

| Error                                                 | Cause                                                                  | Solution                                                                    |
| :---------------------------------------------------- | :--------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `ReadTimeoutException`                                | Node failed to respond within timeout under heavy load or replica lag. | Tune consistency level (e.g. `LOCAL_QUORUM`) and check GC pauses on nodes.  |
| `Overwhelming tombstone cells count`                  | High frequency of deletes or null inserts causing read degradation.    | Avoid writing `null` columns; tune `gc_grace_seconds` and compact SSTables. |
| `UnavailableException: Not enough replicas available` | Cluster cannot satisfy required consistency level due to node outages. | Check nodetool status and bring failed nodes online or use `LOCAL_ONE`.     |

## References

- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
