---
name: hbase
description: Expert Apache HBase assistance covering wide-column storage, RegionServers, ZooKeeper, row key design, and compaction. Use when scaling petabyte distributed tables on top of Hadoop HDFS.
---

# Apache HBase

HBase is the Hadoop database. It is a distributed, scalable, big data store. It provides random, real-time read/write access to your Big Data.

## When to Use

- **Billion-Row Distributed Big Data Storage**: Storing petabytes of structured/semi-structured data on top of Hadoop HDFS.
- **Real-Time Read/Write Access on Big Data**: Serving random, real-time read and write lookups against massive Hadoop datasets.
- **Sparse Wide-Column Datasets**: Managing tables with millions of columns where individual rows populate only a small subset of fields.
- **Tight Apache Hadoop / Spark Ecosystem Integration**: Running distributed map-reduce and Spark streaming jobs natively over HBase tables.

## Quick Start

Uses Java API or Shell.

```bash
create 'users', 'info', 'data'
put 'users', 'row1', 'info:name', 'Alice'
get 'users', 'row1'
```

## Core Concepts

#Master-RegionServer & HDFS Architecture

Tables are split into Regions, managed by RegionServers, and backed persistently by HDFS HFiles:

```
[ HBase Master (Coordination via ZooKeeper) ]
        ├── [ RegionServer 1 ] ──→ Region A (Keys: A-M) ──→ Writes to HDFS WAL & MemStore
        └── [ RegionServer 2 ] ──→ Region B (Keys: N-Z) ──→ Flushes to HFiles on HDFS
```

#RowKey, Column Families, and Timestamps

Coordinates are addressed via `(RowKey, ColumnFamily, ColumnQualifier, Timestamp)`:

```bash
# HBase Shell Commands
create 'telemetry_events', 'sensor_data', 'metadata'

# Put data into Column Family
put 'telemetry_events', 'sensor_101_20260927', 'sensor_data:temp', '24.5'
put 'telemetry_events', 'sensor_101_20260927', 'metadata:location', 'Building A'
```

#LSM-Tree Write Path (WAL & MemStore to HFile)

Writes append to Write-Ahead-Log (WAL), buffer in memory (MemStore), and flush to immutable HFiles:

```
[ Client Write ] ──→ [ Write Ahead Log (WAL) ] ──→ [ In-Memory MemStore ] ──Flush──→ [ On-Disk HFile ]
```

## Common Patterns

### Salted Row Keys to Avoid RegionServer Hot-Spotting

**Problem**: Monotonically increasing timestamps as row keys cause all writes to hit a single active RegionServer.

**Solution**:
Prepend a hash salt or reverse timestamp prefix to distribute writes:

```java
// Row key: Salt(0-9) + TenantId + ReversedTimestamp
String salt = String.valueOf(Math.abs(tenantId.hashCode() % 10));
long reversedTime = Long.MAX_VALUE - System.currentTimeMillis();
byte[] rowKey = Bytes.toBytes(salt + "_" + tenantId + "_" + reversedTime);

Put put = new Put(rowKey);
put.addColumn(Bytes.toBytes("metrics"), Bytes.toBytes("cpu"), Bytes.toBytes(95.4));
table.put(put);
```

## Best Practices (2026)

**Do**:

- **Salt or Hash RowKeys**: Prepend a hash or bucket prefix (`hash(id) + id`) to distribute writes evenly and prevent hotspotting single RegionServers.
- **Keep Column Family Names Short**: Column family names are repeated in every cell on disk; use concise names (`d` for data, `m` for meta).
- **Pre-Split Tables on Creation**: Pre-split regions based on expected rowkey distributions to avoid sudden region split pauses during bulk loads.
- **Use Scan Caching and Batching**: Set `scan.setCaching(500)` when iterating over large ranges to reduce RPC roundtrips.

**Don't**:

- **Don't use monotonically increasing rowkeys (timestamps)**: Appending timestamps causes all writes to strike a single RegionServer at any moment.
- **Don't create more than 2-3 Column Families**: HBase is optimized for 1-2 column families; multiple families cause uneven flush behavior.
- **Don't neglect ZooKeeper health**: ZooKeeper manages RegionServer heartbeats; cluster instability results if ZooKeeper loses quorum.

## Troubleshooting

| Error                          | Cause                                                            | Solution                                                                    |
| :----------------------------- | :--------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `RegionServerOutOfMemoryError` | Large BlockCache and MemStore allocations exceeding JVM heap.    | Tune `hbase.regionserver.global.memstore.size` and use G1 GC collector.     |
| `ZooKeeper session expired`    | Long GC pauses on RegionServer causing ZooKeeper heartbeat loss. | Optimize JVM garbage collection parameters and increase ZK session timeout. |
| `TableNotEnabledException`     | Table in disabled state during maintenance or schema update.     | Run `enable 'tablename'` in HBase shell.                                    |

## References

- [Apache HBase Reference Guide](https://hbase.apache.org/book.html)
