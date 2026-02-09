---
name: redis
description: Redis in-memory cache, pub/sub, streams, and data structures. Use for caching and real-time data.
---

# Redis

In-memory data store for caching, sessions, pub/sub, and real-time features.

## When to Use

- Caching frequently accessed data
- Session storage
- Real-time leaderboards/counters
- Pub/sub messaging
- Rate limiting

## Quick Start

```bash
# String operations
SET user:1 '{"name":"John"}' EX 3600
GET user:1

# Hash operations
HSET user:1 name "John" email "john@example.com"
HGETALL user:1
```

## Core Concepts

### Data Structures

```bash
# Strings
SET key "value"
INCR counter
SETEX session:abc "token" 3600

# Hashes
HSET user:1 name "John" age 30
HGET user:1 name
HINCRBY user:1 age 1

# Lists
LPUSH queue:tasks "task1"
RPOP queue:tasks
LRANGE queue:tasks 0 -1

# Sets
SADD tags:post:1 "redis" "database"
SMEMBERS tags:post:1
SINTER tags:post:1 tags:post:2

# Sorted Sets
ZADD leaderboard 100 "player1" 85 "player2"
ZREVRANGE leaderboard 0 9 WITHSCORES
ZINCRBY leaderboard 5 "player1"
```

### Caching Patterns

```python
# Cache-aside pattern
def get_user(user_id):
    # Try cache first
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    user = db.query(User).get(user_id)

    # Store in cache
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

# Write-through
def update_user(user_id, data):
    db.update(User, user_id, data)
    redis.setex(f"user:{user_id}", 3600, json.dumps(data))
```

## Common Patterns

### Pub/Sub

```python
# Publisher
redis.publish("events", json.dumps({"type": "user_created", "id": 123}))

# Subscriber
pubsub = redis.pubsub()
pubsub.subscribe("events")
for message in pubsub.listen():
    if message["type"] == "message":
        handle_event(json.loads(message["data"]))
```

### Rate Limiting

```python
def rate_limit(key, limit, window):
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, window)
    return current <= limit

# Usage
if not rate_limit(f"api:{user_id}", 100, 60):
    raise RateLimitExceeded()
```

## Best Practices

**Do**:

- Use appropriate data structures
- Set TTL on cache keys
- Use pipelining for bulk operations
- Enable persistence for durability

**Don't**:

- Store large objects (> 1MB)
- Use KEYS command in production
- Forget to handle connection failures
- Use single Redis for everything

## Troubleshooting

| Issue              | Cause                | Solution                 |
| ------------------ | -------------------- | ------------------------ |
| Memory full        | No eviction policy   | Set maxmemory-policy     |
| Slow commands      | Large key operations | Use SCAN instead of KEYS |
| Connection timeout | Network/overload     | Use connection pooling   |

## References

- [Redis Documentation](https://redis.io/docs/)
- [Redis Best Practices](https://redis.io/docs/management/optimization/)
