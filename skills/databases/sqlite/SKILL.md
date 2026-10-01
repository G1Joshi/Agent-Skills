---
name: sqlite
description: Expert SQLite embedded database assistance covering WAL mode, PRAGMA tuning, full-text search (FTS5), and concurrency. Use when building desktop/mobile apps, local databases, or high-performance embedded systems.
---

# SQLite

SQLite is an embedded SQL database engine. Unlike most other SQL databases, SQLite does not have a separate server process. It reads and writes directly to ordinary disk files.

## When to Use

- **Embedded Mobile & Desktop Client Applications**: The standard embedded database engine for iOS, Android, macOS, Windows, and Linux apps.
- **Edge Computing & Local Cache**: Running fast relational databases inside Cloudflare D1, Turso, or local container storage.
- **Zero-Configuration Local Development**: Powering unit tests and local prototypes without spinning up external database servers.
- **High-Read Single-Server Web Applications**: Serving millions of read queries per day with SQLite Write-Ahead-Logging (WAL) mode enabled.

## Quick Start

```sql
-- Enable WAL mode for concurrency
PRAGMA journal_mode=WAL;

-- Create table
CREATE TABLE contacts (
	contact_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	phone TEXT NOT NULL UNIQUE
);
```

## Core Concepts

### Single-File Serverless Engine

SQLite runs directly in the host application's memory space, reading and writing to a single cross-platform disk file:

```text
[ Application Process (Python / Go / Node / Swift) ] ──Direct In-Memory Access──→ [ database.sqlite (Single File) ]
```

### Write-Ahead Logging (WAL Mode)

Enables concurrent readers while a writer commits changes simultaneously:

```sql
-- Essential production pragmas for web apps
PRAGMA journal_mode = WAL;          -- Concurrent reads while writing
PRAGMA synchronous = NORMAL;        -- 2-3x write acceleration with durable safety
PRAGMA busy_timeout = 5000;         -- Wait up to 5s on busy locks before erroring
PRAGMA foreign_keys = ON;           -- Enforce relational foreign key constraints
PRAGMA cache_size = -64000;         -- Allocate 64MB memory page cache
```

### Full-Text Search with FTS5

Built-in full-text search engine with BM25 relevancy ranking:

```sql
CREATE VIRTUAL TABLE document_search USING fts5(title, body);

INSERT INTO document_search (title, body) VALUES
('Distributed Systems', 'Consensus protocols and Raft algorithms in modern software.');

-- Fast full-text search
SELECT title, bm25(document_search) AS rank
FROM document_search
WHERE document_search MATCH 'Raft OR Consensus'
ORDER BY rank;
```

## Common Patterns

### WAL Mode and Concurrency Performance PRAGMAs

**Problem**: Default rollback journal locks entire database during writes, causing `database is locked` errors during concurrent reads.

**Solution**:
Enable Write-Ahead Logging (WAL) and memory optimizations at connection initialization:

```sql
-- Enable concurrent readers and writer
PRAGMA journal_mode = WAL;

-- Optimize disk sync frequency for higher write throughput
PRAGMA synchronous = NORMAL;

-- Cache pages in memory (e.g. 64MB)
PRAGMA cache_size = -64000;

-- Store temporary tables and indexes in memory
PRAGMA temp_store = MEMORY;

-- Enable foreign key constraint checking
PRAGMA foreign_keys = ON;
```

## Best Practices

**Do**:

- Always Enable WAL Mode in Production: Run `PRAGMA journal_mode = WAL;` to prevent writers from blocking readers.
- Set a `busy_timeout`: Configure `PRAGMA busy_timeout = 5000;` to avoid `SQLITE_BUSY` errors during concurrent transactions.
- Enable Foreign Keys Explicitly: SQLite disables foreign keys by default; execute `PRAGMA foreign_keys = ON;` on every connection.
- Use Prepared Statements: Eliminate SQL injection and optimize query plan reuse.

**Don't**:

- Run multiple concurrent write transactions: SQLite supports only one writer at a time; queue writes or serialize them.
- Use SQLite over Network Filesystems (NFS/SMB): Network file locking bugs can corrupt SQLite database files.
- Store multi-gigabyte binary files directly: Store media in filesystem directories or object storage; store file paths in SQLite.

## Troubleshooting

| Error                                               | Cause                                                                        | Solution                                                                            |
| :-------------------------------------------------- | :--------------------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `database is locked (SQLITE_BUSY)`                  | Another connection holds a write lock or transaction open too long.          | Enable WAL mode and set busy timeout: `PRAGMA busy_timeout = 5000;`.                |
| `database disk image is malformed (SQLITE_CORRUPT)` | Power loss during non-sync write, hardware fault, or concurrent file access. | Restore from backup, or dump readable rows using `.recover` command in sqlite3 CLI. |
| `FOREIGN KEY constraint failed`                     | Inserted row references non-existent parent foreign key.                     | Verify parent row exists before inserting child row.                                |

## References

- [SQLite Documentation](https://www.sqlite.org/docs.html)
