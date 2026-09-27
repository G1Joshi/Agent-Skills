---
name: mariadb
description: Expert MariaDB relational database assistance covering Galera Cluster, ColumnStore, Aria storage engine, and SQL replication. Use when running high-availability MySQL-compatible relational databases.
---

# MariaDB

MariaDB is a fork of MySQL, created by the original developers of MySQL. It is guaranteed to stay open source. It lists features that MySQL doesn't have, or adds them faster.

## When to Use

- **High-Performance MySQL Drop-in Replacement**: Upgrading MySQL infrastructure with enhanced performance, Aria storage, and thread pooling.
- **Temporal Data & System-Versioned Tables**: Retaining automatic audit histories of all row modifications using SQL:2011 system versioning.
- **ColumnStore Analytical Processing**: Running hybrid transactional and analytical processing (HTAP) in a single database server.
- **Enterprise Open-Source Relational SQL**: Deploying mission-critical relational databases with enterprise-grade replication (Galera Cluster).

## Quick Start

Same as MySQL usually.

```sql
-- System-Versioned Tables (Time Travel)
CREATE TABLE t (
  x INT,
  PERIOD FOR SYSTEM_TIME (ts_start, ts_end)
) WITH SYSTEM VERSIONING;

-- Query history
SELECT * FROM t FOR SYSTEM_TIME AS OF TIMESTAMP '2024-01-01 00:00:00';
```

## Core Concepts

#System-Versioned Tables (Automatic Audit Trails)

Tracks complete historical lifecycles of rows automatically without application triggers:

```sql
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2)
) WITH SYSTEM VERSIONING;

-- Query historical state as of yesterday
SELECT * FROM employees
FOR SYSTEM_TIME AS OF (NOW() - INTERVAL 1 DAY)
WHERE department = 'Engineering';
```

#Galera Cluster Synchronous Multi-Master Replication

Enforces synchronous multi-node replication with zero replication lag and automated node joining:

```
[ Node 1 (Primary) ] ──Synchronous Write Certification (wsrep)──→ [ Node 2 (Primary) ]
                                      │
                                      ▼
                             [ Node 3 (Primary) ]
```

#Modern Thread Pooling for High Concurrency

Maintains stable throughput during connection spikes using server-side thread pools:

```ini
# /etc/mysql/mariadb.conf.d/50-server.cnf
[mariadb]
thread_handling=pool-of-threads
thread_pool_size=16
thread_pool_max_threads=1000
```

## Common Patterns

### Galera Multi-Master High Availability Configuration

**Problem**: Master-slave failover delays cause downtime and split-brain risks during network disruptions.

**Solution**:
Configure synchronous multi-master replication in `server.cnf`:

```ini
[galera]
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_cluster_name="galera_cluster"
wsrep_cluster_address="gcomm://10.0.0.1,10.0.0.2,10.0.0.3"
wsrep_node_name="node1"
wsrep_node_address="10.0.0.1"
binlog_format=ROW
default_storage_engine=InnoDB
```

## Best Practices (2026)

**Do**:

- **Leverage System-Versioned Tables for Compliance**: Use native versioning rather than complex manual audit trigger scripts.
- **Use InnoDB as Default Storage Engine**: Reserve Aria storage for temporary tables and ColumnStore for analytical queries.
- **Enable the Thread Pool Plugin**: Handle thousands of concurrent web connections without thread creation overhead.
- **Configure Automated Galera Cluster Quorum**: Deploy odd numbers of nodes (minimum 3) to prevent split-brain conditions.

**Don't**:

- **Don't use legacy MyISAM tables**: MyISAM lacks crash safety and row-level locking.
- **Don't treat Galera Cluster as a multi-region WAN database**: High cross-region latency degrades synchronous write throughput.
- **Don't skip slow query logging**: Enable `slow_query_log` and `long_query_time = 1.0` to identify missing indexes.

## Troubleshooting

| Error                                                           | Cause                                                                | Solution                                                                     |
| :-------------------------------------------------------------- | :------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `Deadlock found when trying to get lock (Galera certification)` | Concurrent writes to same row across different Galera cluster nodes. | Route write traffic to a single primary node and use read replicas.          |
| `WSREP has not yet prepared node for application use`           | Node currently in State Snapshot Transfer (SST) synchronization.     | Wait for joiner node to finish syncing or check `wsrep_local_state_comment`. |
| `Table is marked as crashed and should be repaired`             | Improper shutdown or disk corruption on Aria/MyISAM tables.          | Run `REPAIR TABLE tablename;` or migrate to InnoDB storage engine.           |

## References

- [MariaDB Knowledge Base](https://mariadb.com/kb/en/)
