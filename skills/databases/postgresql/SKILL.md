---
name: postgresql
description: Expert PostgreSQL assistance covering advanced SQL, JSONB, indexing (B-Tree, GIN, BRIN), query optimization with EXPLAIN ANALYZE, and replication. Use when designing robust relational schemas or tuning performance.
---

# PostgreSQL

PostgreSQL (Postgres) is a powerful, open-source object-relational database system. It is known for its reliability, feature robustness (JSONB, GIS, Full Text Search), and performance.

## When to Use

- **The Default Advanced Relational Database**: The standard, most versatile open-source relational database for modern software engineering.
- **Semi-Structured Document Storage (JSONB)**: Storing, indexing, and querying JSON documents with GIN indexes and JSONPath expressions.
- **AI & Vector Embeddings (pgvector)**: Storing high-dimensional vector embeddings and executing cosine/L2 semantic similarity search.
- **Geospatial Applications (PostGIS)**: Analyzing spatial geometries, geographic boundaries, and GPS coordinates with industry-standard PostGIS.

## Quick Start

```sql
-- JSONB column usage
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB
);

INSERT INTO events (data) VALUES ('{"type": "login", "user": "alice"}');

-- Query JSON directly (indexing supported)
SELECT * FROM events WHERE data->>'user' = 'alice';
```

## Core Concepts

#Advanced JSONB & Generalized Inverted Indexes (GIN)

JSONB stores binary decomposed JSON with full indexing support:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create GIN Index over entire JSONB structure
CREATE INDEX idx_users_profile ON users USING GIN (profile);

-- Fast sub-millisecond containment search
SELECT * FROM users
WHERE profile @> '{"role": "admin", "settings": {"notifications": true}}';
```

#pgvector Semantic Similarity Search

Integrates AI vector embeddings directly alongside relational tables:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE document_embeddings (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536) -- OpenAI embedding dimension
);

-- Create HNSW index for sub-5ms approximate nearest neighbor search
CREATE INDEX idx_embeddings_hnsw ON document_embeddings
USING hnsw (embedding vector_cosine_ops);

-- Find top 5 most semantically similar documents
SELECT id, content, 1 - (embedding <=> '[0.012, -0.045, ...]') AS similarity
FROM document_embeddings
ORDER BY embedding <=> '[0.012, -0.045, ...]'
LIMIT 5;
```

#Multi-Version Concurrency Control (MVCC) & VACUUM

PostgreSQL retains old row versions on update/delete; the autovacuum daemon reclaims dead tuples:

```sql
-- Inspect bloat and dead tuples
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
WHERE relname = 'users';
```

## Common Patterns

### JSONB Ingestion with GIN Indexing for Fast Document Queries

**Problem**: Relational normalization adds too much overhead for variable schema payloads, but standard text search is slow.

**Solution**:
Use PostgreSQL `JSONB` data type with GIN index:

```sql
CREATE TABLE audit_events (
  id BIGSERIAL PRIMARY KEY,
  event_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata JSONB NOT NULL
);

-- GIN index supports fast top-level and nested key existence queries
CREATE INDEX idx_audit_metadata ON audit_events USING GIN (metadata jsonb_path_ops);

-- Fast indexed query matching nested key-value
SELECT * FROM audit_events
WHERE metadata @> '{"action": "LOGIN", "status": "FAILED"}';
```

## Best Practices (2026)

**Do**:

- **Use Connection Poolers (PgBouncer)**: Prevent process-per-connection exhaustion by running PgBouncer in transaction pooling mode.
- **Use `TIMESTAMPTZ` for Date Columns**: Always store timestamps with timezone information (`TIMESTAMPTZ`), never bare `TIMESTAMP`.
- **Create Partial and Expression Indexes**: Index only active rows (`WHERE deleted_at IS NULL`) to keep index sizes compact.
- **Run `EXPLAIN (ANALYZE, BUFFERS)`**: Analyze exact buffer hits and query execution plans before deploying new queries.

**Don't**:

- **Don't use `SERIAL` for new tables**: Use standard SQL identity columns (`GENERATED ALWAYS AS IDENTITY`) or `UUIDv7`.
- **Don't disable Autovacuum**: Disabling autovacuum causes catastrophic table bloat and transaction ID wraparound emergencies.
- **Don't write long-running transactions**: Long open transactions block vacuuming and cause severe table bloat.

## Troubleshooting

| Error                                                                          | Cause                                                                   | Solution                                                                            |
| :----------------------------------------------------------------------------- | :---------------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `FATAL: remaining connection slots are reserved for non-replication superuser` | Max connections exceeded by application instances.                      | Deploy `PgBouncer` connection pooler and tune `max_connections`.                    |
| `Seq Scan on large table in EXPLAIN ANALYZE`                                   | Planner chose sequential scan due to stale statistics or missing index. | Run `ANALYZE tablename;` or create index matching query predicates.                 |
| `deadlock detected (ERROR: 40P01)`                                             | Concurrent transactions acquired locks in opposing order.               | Standardize lock acquisition order across transactions and keep transactions small. |

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [Postgres Weekly](https://postgresweekly.com/)
