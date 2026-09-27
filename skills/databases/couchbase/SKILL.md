---
name: couchbase
description: Expert Couchbase NoSQL assistance covering N1QL/SQL++ queries, memory-first caching, document scopes, and cross-datacenter replication (XDCR). Use when building ultra-low latency JSON document platforms.
---

# Couchbase

Couchbase works as a Key-Value store (managed memory cache) + Document Database. It is famous for its "memory-first" architecture and N1QL (SQL for JSON).

## When to Use

- **Memory-First NoSQL Document Store**: Applications requiring sub-millisecond document lookups powered by an integrated managed memory cache.
- **SQL for JSON (N1QL / SQL++)**: Querying JSON documents using familiar SQL syntax with joins, nested arrays, and subqueries.
- **Distributed Key-Value + Full-Text Search**: Unifying key-value caching, document storage, and vector/full-text search in a single cluster.
- **Mobile Edge Data Sync (Couchbase Lite)**: Synchronizing embedded mobile database instances with cloud clusters using Sync Gateway.

## Quick Start

```sql
-- N1QL Query
SELECT u.name, ARRAY_AGG(o.item) as orders
FROM `travel-sample`.inventory.users u
JOIN `travel-sample`.inventory.orders o ON u.id = o.user_id
WHERE u.city = "Paris"
GROUP BY u.name;
```

## Core Concepts

#Memory-First VBucket Architecture

Documents are mapped across 1024 virtual buckets (vBuckets), cached directly in RAM before being asynchronously written to disk:

```
[ Application Client ] ──Sub-Millisecond Read/Write──→ [ Managed Memory Cache (RAM) ]
                                                                 │ (Async Flush)
                                                                 ▼
                                                        [ Append-Only Disk Storage ]
```

#SQL++ (N1QL) Declarative JSON Queries

Executes full SQL expressions over schemaless JSON structures:

```sql
-- Query nested JSON orders in Couchbase SQL++
SELECT
  meta().id AS orderId,
  customer.email,
  ARRAY_SUM(items[*].price) AS totalAmount
FROM `commerce`.`orders` AS o
WHERE status = 'PAID'
  AND ANY item IN items SATISFIES item.category = 'Electronics' END
ORDER BY totalAmount DESC
LIMIT 20;
```

#Scopes and Collections Multi-Tenancy

Organizes documents into logical namespaces mimicking relational databases:

```
[ Bucket: enterprise ]
  ├── [ Scope: billing ]
  │   ├── [ Collection: invoices ]
  │   └── [ Collection: payments ]
  └── [ Scope: catalog ]
      └── [ Collection: products ]
```

## Common Patterns

### SQL++ (N1QL) Secondary Indexing and Querying

**Problem**: Ad-hoc JSON document filtering results in slow primary index table scans.

**Solution**:
Build covering secondary GSI indexes for high-throughput queries:

```sql
CREATE INDEX idx_orders_status ON `ecommerce`.`sales`.`orders` (customerId, orderStatus, orderDate)
WHERE orderStatus != 'cancelled';

SELECT customerId, orderDate, total
FROM `ecommerce`.`sales`.`orders`
WHERE customerId = "cust_987" AND orderStatus = "completed"
ORDER BY orderDate DESC;
```

## Best Practices (2026)

**Do**:

- **Use Sub-Document API for Partial Mutations**: Mutate specific JSON array items or attributes without fetching/resaving the entire document.
- **Create Global Secondary Indexes (GSI) Covering Queries**: Index the exact fields in `WHERE` and `SELECT` to enable index-only scans.
- **Leverage Key-Value Operations for Hot Lookups**: Use `get()` and `upsert()` key-value APIs for sub-millisecond reads rather than N1QL queries.
- **Size Bucket RAM Quotas Carefully**: Allocate sufficient RAM to ensure high active working set cache-hit ratios.

**Don't**:

- **Don't use Primary Indexes in Production**: Avoid `CREATE PRIMARY INDEX`; primary scans scan all documents in the collection.
- **Don't store massive binary blobs in documents**: Keep documents under 1MB; store images and media in object storage.
- **Don't ignore Cross-Datacenter Replication (XDCR) lag**: Monitor XDCR replication queues when synchronizing across multi-region clusters.

## Troubleshooting

| Error                               | Cause                                                                | Solution                                                                              |
| :---------------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `No index available for query`      | Missing secondary index matching the WHERE predicate in SQL++ query. | Create an index covering query filter and projection columns.                         |
| `Temporary failure / Out of memory` | Couchbase bucket memory quota exhausted by high item count.          | Increase bucket RAM quota or configure eviction policy (value-only vs full eviction). |
| `DocumentExistsException`           | Key already exists in bucket during insert operation.                | Use `upsert` instead of `insert` if overwrite semantics are intended.                 |

## References

- [Couchbase Documentation](https://docs.couchbase.com/home/index.html)
