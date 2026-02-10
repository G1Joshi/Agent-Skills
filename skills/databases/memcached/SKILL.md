---
name: memcached
description: Memcached distributed memory caching. Use for simple caching.
---

# Memcached

Memcached is a high-performance, distributed memory object caching system. It is simpler than Redis. It does arguably one thing: Key-Value caching of strings/objects in RAM.

## When to Use

- **Simple Caching**: Pure LRU cache.
- **Multi-Threaded**: Memcached is multi-threaded (Redis is single-threaded). It scales vertically better on massive multicore machines for simple GET/SET throughput.
- **Session Cache**: Storing web sessions.

## Quick Start

```bash
# Telnet interface
set mykey 0 60 4
data
STORED

get mykey
VALUE mykey 0 4
data
END
```

## Core Concepts

### Slab Allocation

Memcached manages memory in "Classes" of chunks (Slabs) to prevent fragmentation.

### LRU (Least Recently Used)

When full, it evicts the oldest unused items.

### No Persistence

If you restart, data is gone.

## Best Practices (2025)

**Do**:

- **Use for huge read-heavy loads**: Facebook uses it heavily.
- **Use Serialization**: Store Protobuf or msgpack for efficiency.

**Don't**:

- **Don't use as a Datastore**: It is a cache _only_.
- **Don't use iterating**: You cannot "List all keys". You must know the key to get the value.
- **Comparison to Redis**: In 2025, Redis is generally preferred for features. Use Memcached if you specifically need multi-threaded scaling for pure String caching.

## References

- [Memcached Wiki](https://github.com/memcached/memcached/wiki)
