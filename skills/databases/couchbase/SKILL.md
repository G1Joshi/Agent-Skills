---
name: couchbase
description: Couchbase distributed NoSQL database. Use for mobile and edge.
---

# Couchbase

Couchbase works as a Key-Value store (managed memory cache) + Document Database. It is famous for its "memory-first" architecture and N1QL (SQL for JSON).

## When to Use

- **Caching + Persistence**: When you need the speed of Redis but the persistence/querying of MongoDB.
- **Mobile Sync**: Couchbase Mobile / Sync Gateway provides robust offline-sync for mobile apps.
- **SQL on JSON**: N1QL allows using standard SQL (`SELECT * FROM users JOIN orders`) on JSON documents.

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

### Memory First

Writes go to memory first (microseconds), then disk. Reads serve from memory if hot.

### Couchbase Capella

The fully managed Database-as-a-Service (DBaaS) version. Best for 2025 usage.

### Buckets, Scopes, Collections

Hierarchy: Cluster -> Bucket -> Scope -> Collection -> Document. Maps roughly to Database -> Schema -> Table -> Row.

## Best Practices (2025)

**Do**:

- **Index N1QL queries**: Like a relational DB, specific queries need specific GSI (Global Secondary Indexes).
- **Use Vector Search**: 2025 versions support Vector Search for AI apps.

**Don't**:

- **Don't use Views**: Old MapReduce Views are deprecated. Use N1QL.

## References

- [Couchbase Documentation](https://docs.couchbase.com/home/index.html)
