---
name: couchdb
description: Expert Apache CouchDB assistance covering HTTP REST APIs, Mango queries, conflict resolution, and offline-first mobile sync. Use when building multi-master replicated apps or PouchDB browser synchronization.
---

# Apache CouchDB

CouchDB is a database that completely embraces the web. It speaks JSON and HTTP. It is unique for its multi-master replication protocol, making it ideal for "Offline First" apps.

## When to Use

- **Offline-First Synchronized Web & Mobile Apps**: Pairing with PouchDB in web browsers to enable full offline operation with automated background sync.
- **RESTful HTTP Document Storage**: Accessing and mutating JSON documents purely through standard HTTP verbs without proprietary drivers.
- **Append-Only Document Versioning**: Tracking document revision histories and managing conflicting edits explicitly.
- **Distributed Peer-to-Peer Replication**: Replicating databases bidirectionally across edge servers, embedded devices, and cloud nodes.

## Quick Start

```bash
# Create a document via REST API
curl -X PUT http://admin:password@127.0.0.1:5984/my_database/doc1 \
     -d '{"key": "value"}'
```

## Core Concepts

### Pure HTTP/RESTful Interface

Every database operation maps directly to standard HTTP methods:

```bash
# 1. Create a document
curl -X POST http://admin:password@127.0.0.1:5984/mydb \
  -H "Content-Type: application/json" \
  -d '{"title": "Offline-First Architectures", "status": "published"}'
# Returns: {"ok": true, "id": "8f3d1e1c...", "rev": "1-a1b2c3d4..."}

# 2. Retrieve document by ID
curl -X GET http://admin:password@127.0.0.1:5984/mydb/8f3d1e1c...
```

### Multiversion Concurrency Control (MVCC) & Revisions (`_rev`)

Updating documents requires passing the active revision tag to prevent accidental overwrites:

```bash
# Update requires passing latest _rev token
curl -X PUT http://admin:password@127.0.0.1:5984/mydb/8f3d1e1c... \
  -H "Content-Type: application/json" \
  -d '{"_rev": "1-a1b2c3d4...", "title": "Updated Title", "status": "draft"}'
```

### Bi-Directional Master-Master Replication

Syncs databases seamlessly between independent nodes:

```json
// POST to /_replicate
{
  "source": "http://edge-node.local:5984/pos_sales",
  "target": "https://admin:pass@cloud.corp.com:5984/pos_sales",
  "continuous": true,
  "create_target": true
}
```

## Common Patterns

### Conflict-Aware Document Updating

**Problem**: Concurrent offline writes in CouchDB create document revision forks (`_conflicts`).

**Solution**:
Fetch existing revision and resolve conflicts deterministically:

```bash
# 1. Fetch current revision
REV=$(curl -s "http://127.0.0.1:5984/mydb/doc1" | jq -r '._rev')

# 2. Update with required _rev header
curl -X PUT "http://127.0.0.1:5984/mydb/doc1"   -H "Content-Type: application/json"   -d "{"_rev": "$REV", "title": "Updated Document", "status": "resolved"}"
```

## Best Practices

**Do**:

- Pair with PouchDB in Browsers: Use PouchDB locally in client IndexedDB; sync automatically with CouchDB on network recovery.
- Run Regular Database Compaction: Execute `POST /mydb/_compact` to clean up old MVCC revision trees and reclaim disk space.
- Design Conflict Resolution Explicitly: Handle deterministic conflict resolution in application code when concurrent offline edits occur.
- Create Mango Indexes: Define JSON indexes (`_index`) to optimize ad-hoc JSON querying via `_find`.

**Don't**:

- Rely on CouchDB for high-throughput OLTP transactions: CouchDB is built for offline sync and eventual consistency, not rapid transactions.
- Ignore the `_rev` parameter: Forgetting to handle 409 Conflict responses causes user updates to drop.
- Expose raw CouchDB admin ports to public networks: Protect port 5984 behind Nginx or Cloudflare reverse proxies.

## Troubleshooting

| Error                                                       | Cause                                                            | Solution                                                                 |
| :---------------------------------------------------------- | :--------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `{"error":"conflict","reason":"Document update conflict."}` | Stale `_rev` submitted during document PUT operation.            | Fetch latest document version and reapply changes with current `_rev`.   |
| `Database size growing excessively`                         | Old revision history retained by MVCC storage engine.            | Run database and view compaction: `POST /mydb/_compact`.                 |
| `Unauthorized (401)`                                        | Server running in non-admin party mode without auth credentials. | Provide Basic Auth header or create session cookie via `POST /_session`. |

## References

- [CouchDB Documentation](https://docs.couchdb.org/en/stable/)
