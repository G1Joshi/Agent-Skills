---
name: cockroachdb
description: CockroachDB distributed SQL database. Use for geo-distributed data.
---

# CockroachDB

CockroachDB is a cloud-native, distributed SQL database. It survives disk, machine, rack, and even datacenter failures with zero downtime. It speaks PostgreSQL.

## When to Use

- **Global/Multi-Region Apps**: "Geo-partitioning" ties data to specific locations for low latency and compliance (GDPR).
- **Financial Ledgers**: Strong consistency (Serializable Isolation) is the default.
- **Serverless (2025)**: Use CockroachDB Serverless for auto-scaling from zero to millions of requests without managing nodes.

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

### Ranges

Data is broken into 512MB chunks called "Ranges". These are replicated (Raft consensus) across 3+ nodes.

### Geo-Partitioning

You can tell the DB: "Keep German users' data in EU servers, and US users in US servers" using SQL `ALTER TABLE ... PARTITION BY ...`.

### Follow-the-Workload

The database automatically moves "leaseholders" (read/write leaders) close to where the requests are coming from for low latency.

## Best Practices (2025)

**Do**:

- **Use UUIDs**: Sequential keys (1, 2, 3) cause "hot spots" (all writes go to one Range). UUIDs distribute load.
- **Use Serverless**: For most start-ups/mid-size apps, the Serverless consumption model is cheaper and easier than managing nodes.
- **Retry Transactions**: In a distributed system, contention happens. Use client libraries that retry 40001 (serialization failure) errors automatically.

**Don't**:

- **Don't use `SELECT *` without Limits**: In a distributed DB, this might scatter-gather from 100 nodes.
- **Don't use Foreign Keys excessively**: Cross-range FK checks can be expensive.

## References

- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)
