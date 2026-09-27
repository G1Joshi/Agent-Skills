---
name: cockroachdb
description: Expert CockroachDB distributed SQL assistance covering global ACID transactions, Raft consensus, multi-region survivability, and geo-partitioning. Use when scaling relational PostgreSQL workloads across multiple clouds or regions.
---

# CockroachDB

CockroachDB is a cloud-native, distributed SQL database. It survives disk, machine, rack, and even datacenter failures with zero downtime. It speaks PostgreSQL.

## When to Use

- **Global Distributed SQL**: Multi-region enterprise applications requiring PostgreSQL compatibility with multi-region write latency optimization.
- **Zero-Downtime Surviving Outages**: Applications requiring automated failover and self-healing data survival across region or datacenter outages.
- **Strict Serializable ACID Transactions**: Systems requiring the highest isolation level (Serializable) to prevent phantom reads and write skews.
- **Horizontal Scaling without Sharding**: Scaling relational databases beyond single-instance limits without manual application-layer sharding.

## Quick Start

```sql
-- Create a table (Primary Key defaults to UUID in 2025 best practices)
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    balance DECIMAL(19,4)
);

-- Distributed Transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'uuid-1';
UPDATE accounts SET balance = balance + 100 WHERE id = 'uuid-2';
COMMIT;
```

## Core Concepts

#Raft Consensus Ranges & Distributed Storage

Tables are automatically split into 64MB ordered contiguous chunks called Ranges, replicated across nodes via Raft:

```
[ Table: orders ]
  ├── Range 1 (Keys: 000-100) ──→ Replicated via Raft (Node 1, Node 2, Node 3)
  └── Range 2 (Keys: 101-200) ──→ Replicated via Raft (Node 2, Node 3, Node 4)
```

#Multi-Region Table Topologies (REGIONAL vs GLOBAL)

Optimizes data locality to keep data close to users and comply with data residency regulations (GDPR):

```sql
-- Multi-region database and table definition
ALTER DATABASE enterprise_crm SET PRIMARY REGION "us-east-1";
ALTER DATABASE enterprise_crm ADD REGION "eu-west-1";
ALTER DATABASE enterprise_crm ADD REGION "ap-southeast-1";

-- Regional table colocates rows in the user's home region
CREATE TABLE enterprise_crm.customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region crdb_region NOT NULL,
    full_name STRING,
    email STRING
) LOCALITY REGIONAL BY ROW AS region;
```

#Strict Serializable Transaction Isolation

CockroachDB runs all transactions at `SERIALIZABLE` isolation using hybrid logical clocks (HLC) and multi-version concurrency control (MVCC):

```sql
BEGIN TRANSACTION PRIORITY HIGH;
UPDATE accounts SET balance = balance - 100 WHERE id = 'acc_1';
UPDATE accounts SET balance = balance + 100 WHERE id = 'acc_2';
COMMIT;
```

## Common Patterns

### Multi-Region Row-Level Geo-Partitioning

**Problem**: Cross-continent latency degrades transactions when data must travel across oceans for consensus.

**Solution**:
Assign multi-region survival goals with regional tables:

```sql
ALTER DATABASE global_store SET PRIMARY REGION "us-east1";
ALTER DATABASE global_store ADD REGION "eu-west1";

CREATE TABLE global_store.accounts (
  account_id UUID DEFAULT gen_random_uuid(),
  region crdb_region NOT NULL,
  balance DECIMAL(15, 2),
  PRIMARY KEY (region, account_id)
) LOCALITY REGIONAL BY ROW AS region;
```

## Best Practices (2026)

**Do**:

- **Use Multi-Region Survivability Goals**: Configure `SURVIVE REGION FAILURE` to allow clusters to operate through entire cloud region outages.
- **Use UUIDs or Hash-Sharded Indexes**: Avoid monotonically increasing primary keys (`SERIAL` / timestamps) which create hot-spot ranges.
- **Implement Client-Side Transaction Retries**: Handle error code `40001` (transaction serialization retry errors) with exponential backoff.
- **Use `AS OF SYSTEM TIME` for Analytical Queries**: Read from historical MVCC snapshots to eliminate read lock contention.

**Don't**:

- **Don't use sequential integer IDs as primary keys**: Sequential IDs force all insert writes onto a single Raft range node.
- **Don't execute massive unbounded transactions**: Transactions affecting millions of rows create heavy memory pressure on the Raft coordinator.
- **Don't ignore table locality configurations**: Missing multi-region locality rules forces cross-continental WAN roundtrips on every commit.

## Troubleshooting

| Error                                           | Cause                                                                | Solution                                                                    |
| :---------------------------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `TransactionRetryWithProtoRefreshError (40001)` | Concurrent transactions modified overlapping key ranges.             | Wrap business logic in an automated retry loop for serialization conflicts. |
| `Node dead / Raft quorum degraded`              | Network partition or host failure dropping available range replicas. | Check CockroachDB DB Console node status and ensure odd number of replicas. |
| `Slow query due to full range scan`             | Secondary index missing for query WHERE predicates.                  | Run `EXPLAIN` and add composite indexes covering lookup columns.            |

## References

- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)
