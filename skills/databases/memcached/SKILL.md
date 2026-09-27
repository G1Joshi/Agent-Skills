---
name: memcached
description: Expert Memcached in-memory key-value caching assistance covering slab allocation, multithreaded caching, and binary protocol. Use when caching database queries, session stores, or offloading read traffic.
---

# Memcached

Memcached is a high-performance, distributed memory object caching system. It is simpler than Redis. It does arguably one thing: Key-Value caching of strings/objects in RAM.

## When to Use

- **High-Throughput In-Memory Key-Value Caching**: Caching database query results, HTML fragments, and session tokens with sub-millisecond latency.
- **Pure Ephemeral Caching**: Storing disposable data where eviction under memory pressure is acceptable (LRU eviction).
- **Multi-Threaded Multi-Core Scalability**: Maximizing cache operations on large multi-core servers using Memcached's native multi-threaded architecture.
- **Simple Key-Value Lookups**: Caching simple string and serialized objects where advanced data structures (Redis sets/hashes) are unnecessary.

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

#Multi-Threaded Event Loop & Slab Allocation

Memcached allocates memory in fixed slabs to prevent operating system memory fragmentation:

```
Memory Pool (Slab Allocator)
  ├── Slab Class 1 (Chunk Size: 96 Bytes)  -> Stores small keys & tokens
  ├── Slab Class 2 (Chunk Size: 120 Bytes) -> Stores session snippets
  └── Slab Class N (Chunk Size: 1MB)       -> Maximum item size
```

#Consistent Hashing Client-Side Routing

Clusters scale horizontally by having client drivers calculate server destinations using consistent hashing algorithms (Ketama):

```typescript
// Memcached Consistent Hashing in Node.js
import Memcached from "memcached";

const memcached = new Memcached(
  ["10.0.1.1:11211", "10.0.1.2:11211", "10.0.1.3:11211"],
  {
    retries: 2,
    retry: 10000,
    remove: true, // Automatically remove failed nodes from ring
  },
);

// Set with expiration (seconds)
memcached.set("user:415:profile", JSON.stringify(userData), 3600, (err) => {
  if (err) console.error("Cache set failed:", err);
});
```

#Atomic Binary Protocol Operations (CAS, INCR)

Guarantees thread-safe counters and optimistic concurrency control via Check-and-Set (CAS):

```bash
# Telnet / Binary Protocol command
# add <key> <flags> <exptime> <bytes>
<data>

add lock:daily_report 0 60 1
1

```

## Common Patterns

### Cache-Aside Pattern with Expiration

**Problem**: Database overloaded with identical repetitive reads for user profile data.

**Solution**:
Check cache first, fallback to DB, and populate cache with TTL:

```javascript
import Memcached from "memcached";
const memcached = new Memcached("127.0.0.1:11211");

async function getUserProfile(userId) {
  const cacheKey = `user:${userId}`;
  return new Promise((resolve, reject) => {
    memcached.get(cacheKey, async (err, data) => {
      if (data) return resolve(data);
      const dbUser = await db.users.findById(userId);
      memcached.set(cacheKey, dbUser, 3600, (setErr) => {
        if (setErr) console.error("Memcached set failed", setErr);
      });
      resolve(dbUser);
    });
  });
}
```

## Best Practices (2026)

**Do**:

- **Use Ketama Consistent Hashing**: Ensure clients hash keys across cluster nodes so adding/removing nodes evicts minimal keys.
- **Set Appropriate Item Expirations**: Always assign a TTL; prevent stale cache items from lingering indefinitely.
- **Size Slabs to Match Item Distribution**: Monitor `stats slabs` and tune `-f` (chunk growth factor) to minimize internal slab waste.
- **Enable SASL Authentication**: Secure Memcached instances with SASL authentication and private subnet firewall rules.

**Don't**:

- **Don't store items larger than 1MB**: Memcached defaults to a 1MB maximum item size; split large objects or compress them.
- **Don't treat Memcached as a persistent database**: Memcached is strictly in-memory; all data is lost upon server restart.
- **Don't expose port 11211 to the public internet**: Open ports risk catastrophic UDP reflection DDoS amplification attacks.

## Troubleshooting

| Error                                     | Cause                                                            | Solution                                                         |
| :---------------------------------------- | :--------------------------------------------------------------- | :--------------------------------------------------------------- |
| `SERVER_ERROR object too large for cache` | Item size exceeds default 1MB slab limit.                        | Compress data before caching or start daemon with `-I 2m` flag.  |
| `High cache eviction rate`                | Memory limit `-m` too low for active working set.                | Increase allocated memory pool or optimize item TTL expirations. |
| `Connection timed out`                    | Memcached thread pool saturated or firewall blocking port 11211. | Monitor `stats` output and scale Memcached cluster instances.    |

## References

- [Memcached Wiki](https://github.com/memcached/memcached/wiki)
