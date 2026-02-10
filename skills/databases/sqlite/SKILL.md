---
name: sqlite
description: SQLite embedded database for local storage and mobile apps. Use for lightweight database needs.
---

# SQLite

SQLite is an embedded SQL database engine. Unlike most other SQL databases, SQLite does not have a separate server process. It reads and writes directly to ordinary disk files.

## When to Use

- **Mobile Apps**: The standard for iOS/Android local storage.
- **Edge/IoT**: Low memory footprint.
- **App File Format**: Instead of a custom `config.xml`, just use a SQLite db file.
- **Small/Medium Web Apps**: With WAL mode, it handles surprising concurrency (PocketBase, Castopod).

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

### Serverless

There is no "connection" in the TCP sense. You just open the file.

### Dynamic Typing

SQLite uses dynamic typing. A column declared `INTEGER` can actually store a string (though strict tables are now an option).

### WAL Mode (Write-Ahead Logging)

Significantly improves concurrency. Allows multiple readers and one writer simultaneously.

## Best Practices (2025)

**Do**:

- **Use `PRAGMA foreign_keys = ON`**: They are off by default.
- **Use JSONB (SQLite 3.45+)**: Store JSON as efficient binary blobs (`jsonb()`) for 3x faster processing.
- **Use STRICT Tables**: `CREATE TABLE t (...) STRICT` enforces types like a traditional DB.

**Don't**:

- **Don't use over NFS**: File locking on network shares is buggy. Keep the DB file on local disk.
- **Don't use for high-write webservices**: If you have hundreds of concurrent writes, move to Postgres.

## References

- [SQLite Documentation](https://www.sqlite.org/docs.html)
