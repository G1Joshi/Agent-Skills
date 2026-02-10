---
name: couchdb
description: CouchDB document database with sync. Use for offline-first apps.
---

# Apache CouchDB

CouchDB is a database that completely embraces the web. It speaks JSON and HTTP. It is unique for its multi-master replication protocol, making it ideal for "Offline First" apps.

## When to Use

- **Offline First Apps**: PouchDB (in browser) + CouchDB (server) is the gold standard for syncing data.
- **Peer-to-Peer**: Multiple servers can replicate with each other.
- **Reliability**: Crash-resistant architecture (Append-only storage).

## Quick Start

```bash
# Create a document via REST API
curl -X PUT http://admin:password@127.0.0.1:5984/my_database/doc1 \
     -d '{"key": "value"}'
```

## Core Concepts

### Multi-Version Concurrency Control (MVCC)

Documents are versioned (`_rev`). If you update a doc, you must provide the current `_rev`. If it has changed on server, you get a conflict (409).

### CommonJS MapReduce

Views are written in JavaScript functions (Map/Reduce).

### Conflict Resolution

Since replication is multi-master, conflicts happen. CouchDB keeps _all_ conflicting revisions and lets the app execute logic to pick a winner.

## Best Practices (2025)

**Do**:

- **Use PouchDB**: On the client side. It syncs automatically.
- **Use Mango Queries (Find)**: Easier than writing MapReduce views for simple lookups.
- **Compact**: The append-only file grows forever. Run compaction regularly.

**Don't**:

- **Don't use as a generic backend**: It is specialized for sync. If you don't need sync, Postgres/Mongo is often simpler.

## References

- [CouchDB Documentation](https://docs.couchdb.org/en/stable/)
