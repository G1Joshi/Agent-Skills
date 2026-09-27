---
name: redis
description: Expert Redis in-memory data store assistance covering data structures, caching, pub/sub, Lua scripts, Redis Streams, and clustering. Use when building ultra-fast caches, rate limiters, session stores, or message queues.
---

# Redis

Redis (Remote Dictionary Server) is an in-memory data structure store, used as a database, cache, and message broker. It is incredibly fast.

## When to Use

- **In-Memory Caching & Sub-Millisecond Reads**: Caching hot database objects, session state, and computed API payloads in RAM.
- **Distributed Locking & Concurrency Control**: Coordinating atomic multi-instance synchronization with Redlock or SET NX PX commands.
- **High-Velocity Queues & Pub/Sub Messaging**: Powering message brokers, task queues (BullMQ, Sidekiq), and real-time event broadcasting.
- **Rate Limiting & Sliding Windows**: Implementing sliding window rate limiters and leaderboards via Redis Sorted Sets (ZSET).

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

#Advanced In-Memory Data Structures

Redis goes far beyond simple string caching, offering rich native data primitives:

| Structure             | Typical Use Case                   | Example Command                               |
| :-------------------- | :--------------------------------- | :-------------------------------------------- |
| **String**            | Cache values, atomic counters      | `INCR counter`, `SET key val EX 3600`         |
| **Hash**              | Object representation (User, Cart) | `HSET user:101 name "Alice" role "Admin"`     |
| **List**              | Job queues, event timelines        | `LPUSH task_queue job1`, `BRPOP task_queue 0` |
| **Set**               | Unique tags, mutual followers      | `SADD tags "web" "api"`, `SINTER setA setB`   |
| **Sorted Set (ZSET)** | Leaderboards, sliding rate limits  | `ZADD leaderboard 4500 "user101"`             |
| **Stream**            | Event sourcing, append-only logs   | `XADD mystream * sensor "temp" val 24.5`      |

#Atomic Distributed Locks (`SET NX PX`)

Acquires safe mutual exclusion locks across distributed nodes:

```typescript
import { Redis } from "ioredis";
const redis = new Redis(process.env.REDIS_URL!);

async function acquireLock(
  lockKey: string,
  ttlMs: number,
): Promise<string | null> {
  const token = crypto.randomUUID();
  const acquired = await redis.set(lockKey, token, "NX", "PX", ttlMs);
  return acquired === "OK" ? token : null;
}

async function releaseLock(lockKey: string, token: string): Promise<boolean> {
  // Lua script ensures atomic check-and-delete
  const luaScript = `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `;
  const result = await redis.eval(luaScript, 1, lockKey, token);
  return result === 1;
}
```

#Sliding Window Rate Limiter with Sorted Sets (ZSET)

Calculates rolling request rates accurately:

```typescript
async function isRateLimited(
  userId: string,
  limit: number,
  windowSeconds: number,
): Promise<boolean> {
  const now = Date.now();
  const clearBefore = now - windowSeconds * 1000;
  const key = `ratelimit:${userId}`;

  const pipeline = redis.pipeline();
  pipeline.zremrangebyscore(key, 0, clearBefore); // Remove expired requests
  pipeline.zadd(key, now, now.toString()); // Add current request
  pipeline.zcard(key); // Count requests in window
  pipeline.expire(key, windowSeconds);

  const results = await pipeline.exec();
  const requestCount = results![2][1] as number;
  return requestCount > limit;
}
```

## Common Patterns

### Distributed Sliding-Window Rate Limiter with Lua Script

**Problem**: Naive rate limit checks with separate GET/SET calls have race conditions that permit request flooding.

**Solution**:
Execute atomic sliding window rate limiting via Lua script:

```lua
-- KEYS[1]: rate limit key (e.g. rate:user123)
-- ARGV[1]: current timestamp in ms
-- ARGV[2]: window size in ms (e.g. 60000)
-- ARGV[3]: max allowed requests

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local clearBefore = now - window

redis.call('ZREMRANGEBYSCORE', key, 0, clearBefore)
local currentRequests = redis.call('ZCARD', key)

if currentRequests < limit then
    redis.call('ZADD', key, now, now)
    redis.call('PEXPIRE', key, window)
    return 1
else
    return 0
end
```

## Best Practices (2026)

**Do**:

- **Always Set an Eviction Policy**: Configure `maxmemory-policy volatile-lru` or `allkeys-lru` to prevent out-of-memory crashes.
- **Use Pipelines for Multi-Key Operations**: Batch commands with `redis.pipeline()` to eliminate network roundtrip latency.
- **Execute Complex Logic with Atomic Lua Scripts**: Use Lua scripts or Redis Functions to guarantee atomic multi-step operations.
- **Namespace Keys Systematically**: Follow standardized key naming conventions (`app:environment:entity:id`).

**Don't**:

- **Don't run the `KEYS *` command in production**: `KEYS` blocks the single-threaded event loop; use `SCAN` instead.
- **Don't store massive multi-megabyte values**: Redis is single-threaded; serializing huge objects delays all concurrent requests.
- **Don't use Redis without persistence configurations**: Ensure RDB snapshots or AOF (`appendonly yes`) are active if data loss is unacceptable.

## Troubleshooting

| Error                                                    | Cause                                                               | Solution                                                                       |
| :------------------------------------------------------- | :------------------------------------------------------------------ | :----------------------------------------------------------------------------- |
| `OOM command not allowed when used memory > 'maxmemory'` | Redis memory limit reached and eviction policy is `noeviction`.     | Configure `maxmemory-policy allkeys-lru` or scale Redis memory.                |
| `LOADING Redis is loading the dataset in memory`         | Server recently restarted and is parsing RDB/AOF persistence file.  | Wait for dataset reload to finish; optimize AOF file size with `BGREWRITEAOF`. |
| `READONLY You can't write against a read only replica`   | Attempted write operation sent to a replica node instead of master. | Check client clustering configuration and verify write routing to master.      |

## References

- [Redis Documentation](https://redis.io/docs/)
