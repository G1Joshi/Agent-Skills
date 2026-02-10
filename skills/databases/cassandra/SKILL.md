---
name: cassandra
description: Apache Cassandra distributed database for high availability. Use for distributed systems.
---

# Apache Cassandra

Cassandra is a wide-column store database designed for scalability and high availability without compromising performance. Linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data.

## When to Use

- **High Write Throughput**: Ingests millions of writes per second.
- **Always On**: Zero single points of failure. Updates can happen even if nodes are down (Eventual Consistency).
- **Multi-Region**: Active-Active multi-region replication is built-in.

## Quick Start (CQL)

```sql
CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  name text,
  email text
);

INSERT INTO users (user_id, name) VALUES (uuid(), 'Alice');
```

## Core Concepts

### Partition Key & Clustering Key

- **Partition Key**: Determines which node holds the data.
- **Clustering Key**: Sorts data _within_ the partition on disk.

### Tunable Consistency

You choose consistency level per query.

- `ANY`: Fastest, least specific.
- `QUORUM`: Majority must acknowledge. Balanced.
- `ALL`: Slowest, safest.

### Vector Search (5.0+)

Native support for Vector Search (ANN) allows using Cassandra as a Vector DB for AI apps.

## Best Practices (2025)

**Do**:

- **Query by Partition Key**: Always. Scans are prohibited in production.
- **Use SAI (Storage Attached Indexes)**: New in 5.0. Better than old secondary indexes.
- **Denormalize**: Optimize schema for Reads. It is okay to duplicate data into 3 tables to satisfy 3 different query patterns.

**Don't**:

- **Don't use distributed joins**: Cassandra doesn't do joins. Join in the app.
- **Don't use large partitions**: Keep partitions under 100MB to avoid compaction issues.

## References

- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
