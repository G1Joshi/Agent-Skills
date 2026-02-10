---
name: redis
description: Redis in-memory cache, pub/sub, streams, and data structures. Use for caching and real-time data.
---

# Redis

Redis (Remote Dictionary Server) is an in-memory data structure store, used as a database, cache, and message broker. It is incredibly fast.

## When to Use

- **Caching**: The #1 use case. Cache HTML, JSON, or DB results.
- **Session Store**: User sessions (speed + automatic expiry).
- **Queues**: Simple background job queues using Lists (`LPUSH`/`RPOP`).
- **Real-time**: Leaderboards, Counting, Pub/Sub.

## Quick Start

```bash
# Set a value with 10 second expiry
SET session:123 "active" EX 10

# Increment a counter atomically
INCR page:views

# Store a hash (object)
HSET user:100 name "Jeevan" role "admin"
```

## Core Concepts

### Single Threaded

Redis uses a main single thread. Requests are processed sequentially, atomic by design. (Though I/O threading runs in background).

### Persistence (RDB vs AOF)

- **RDB**: Snapshots every X minutes. Fast restart, potential data loss.
- **AOF**: Logs every write. Slower, better durability.

### Data Structures

Strings, Lists, Sets, Sorted Sets (`ZSET`), Hashes, Bitmaps, HyperLogLogs, Geospatial, Streams.

## Best Practices (2025)

**Do**:

- **Use Redis Stack**: Includes extensions like RediSearch (`FT.SEARCH`), RedisJSON, and Bloom Filters.
- **Use Connection Pooling**: Opening connections is expensive.
- **Set `maxmemory-policy`**: Configure what happens when RAM is full (e.g., `allkeys-lru` to delete old data).

**Don't**:

- **Don't use `KEYS *`**: It blocks the server scanning all keys. Use `SCAN`.
- **Don't store huge values**: Redis is for small, fast data.

## References

- [Redis Documentation](https://redis.io/docs/)
