---
name: sqlite
description: SQLite embedded database for local storage and mobile apps. Use for lightweight database needs.
---

# SQLite

Lightweight embedded database for mobile apps and local storage.

## When to Use

- Mobile app local storage (iOS, Android)
- Desktop application databases
- Browser storage (via WebSQL/IndexedDB)
- Development and testing

## Quick Start

```sql
-- Create database and table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Insert and query
INSERT INTO users (email, name) VALUES ('john@example.com', 'John');
SELECT * FROM users WHERE email = 'john@example.com';
```

## Core Concepts

### Data Types

```sql
-- SQLite uses dynamic typing with storage classes
-- NULL, INTEGER, REAL, TEXT, BLOB

CREATE TABLE products (
    id INTEGER PRIMARY KEY,      -- Auto-increment when NULL
    name TEXT NOT NULL,
    price REAL,
    data BLOB,
    is_active INTEGER DEFAULT 1  -- Boolean as 0/1
);
```

### Full-Text Search

```sql
-- Create FTS5 virtual table
CREATE VIRTUAL TABLE posts_fts USING fts5(
    title,
    content,
    content='posts',
    content_rowid='id'
);

-- Search
SELECT * FROM posts_fts WHERE posts_fts MATCH 'search term';

-- Rank results
SELECT *, rank FROM posts_fts
WHERE posts_fts MATCH 'query'
ORDER BY rank;
```

## Common Patterns

### Mobile Usage (Swift)

```swift
import SQLite3

class Database {
    private var db: OpaquePointer?

    func open(path: String) throws {
        guard sqlite3_open(path, &db) == SQLITE_OK else {
            throw DatabaseError.cannotOpen
        }
    }

    func execute(_ sql: String) throws {
        guard sqlite3_exec(db, sql, nil, nil, nil) == SQLITE_OK else {
            throw DatabaseError.executionFailed
        }
    }
}
```

### Mobile Usage (Dart/Flutter)

```dart
import 'package:sqflite/sqflite.dart';

Future<Database> openDatabase() async {
  return openDatabase(
    join(await getDatabasesPath(), 'app.db'),
    onCreate: (db, version) {
      return db.execute('''
        CREATE TABLE users (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL
        )
      ''');
    },
    version: 1,
  );
}
```

## Best Practices

**Do**:

- Use WAL mode for better concurrency
- Use transactions for multiple operations
- Create indexes for search columns
- Use parameterized queries

**Don't**:

- Use for high-concurrency workloads
- Store large blobs (use file system)
- Assume thread safety without WAL
- Forget to close connections

## Troubleshooting

| Issue            | Cause             | Solution         |
| ---------------- | ----------------- | ---------------- |
| Database locked  | Concurrent access | Enable WAL mode  |
| Slow queries     | Missing index     | Add CREATE INDEX |
| Corrupt database | Improper shutdown | Use transactions |

## References

- [SQLite Documentation](https://sqlite.org/docs.html)
- [SQLite for Mobile](https://sqlite.org/android/)
