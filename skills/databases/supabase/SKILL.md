---
name: supabase
description: Supabase PostgreSQL backend-as-a-service with realtime, auth, and edge functions. Use for serverless PostgreSQL.
---

# Supabase

Open-source Firebase alternative with PostgreSQL, realtime, and authentication.

## When to Use

- PostgreSQL with real-time capabilities
- Serverless backend for web/mobile
- Authentication and authorization
- Edge functions and storage

## Quick Start

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Query data
const { data, error } = await supabase
  .from("users")
  .select("*")
  .eq("status", "active")
  .order("created_at", { ascending: false })
  .limit(10);
```

## Core Concepts

### Queries with Relationships

```javascript
// Query with joins
const { data } = await supabase
  .from("posts")
  .select(
    `
    id,
    title,
    author:users(name, email),
    comments(id, content, user:users(name))
  `,
  )
  .eq("status", "published");

// Insert with returning
const { data: user } = await supabase
  .from("users")
  .insert({ name: "John", email: "john@example.com" })
  .select()
  .single();

// Upsert
await supabase.from("profiles").upsert({ id: userId, bio: "Updated bio" });
```

### Real-time Subscriptions

```javascript
// Subscribe to changes
const channel = supabase
  .channel("posts")
  .on(
    "postgres_changes",
    { event: "*", schema: "public", table: "posts" },
    (payload) => {
      console.log("Change:", payload);
    },
  )
  .subscribe();

// Cleanup
channel.unsubscribe();
```

## Common Patterns

### Row Level Security

```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own posts
CREATE POLICY "Users own posts" ON posts
FOR ALL USING (auth.uid() = user_id);

-- Public read, authenticated write
CREATE POLICY "Public read" ON posts
FOR SELECT USING (true);

CREATE POLICY "Auth insert" ON posts
FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
```

### Authentication

```javascript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: "user@example.com",
  password: "password123",
});

// Sign in
const { data } = await supabase.auth.signInWithPassword({
  email: "user@example.com",
  password: "password123",
});

// Get current user
const {
  data: { user },
} = await supabase.auth.getUser();
```

## Best Practices

**Do**:

- Enable Row Level Security on all tables
- Use TypeScript for type safety
- Use Edge Functions for server logic
- Set up proper indexes

**Don't**:

- Expose service role key to client
- Skip RLS policies
- Over-fetch with `select('*')`
- Ignore connection pooling

## Troubleshooting

| Issue             | Cause                | Solution             |
| ----------------- | -------------------- | -------------------- |
| Permission denied | RLS policy           | Check policies, auth |
| Slow query        | Missing index        | Add via SQL editor   |
| Connection limit  | Too many connections | Use pooler mode      |

## References

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase GitHub](https://github.com/supabase/supabase)
