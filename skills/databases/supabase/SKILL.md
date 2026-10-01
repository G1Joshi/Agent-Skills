---
name: supabase
description: Expert Supabase assistance covering PostgreSQL, Row Level Security (RLS), Edge Functions, Auth, and pgvector. Use when building full-stack web/mobile applications with Postgres backends and instant REST/GraphQL APIs.
---

# Supabase

Supabase is an open source Firebase alternative. It provides a dedicated PostgreSQL database, packaged with Authentication, Realtime subscriptions, Storage, and Edge Functions.

## When to Use

- **Open-Source Firebase Alternative**: Complete backend-as-a-service providing PostgreSQL, Auth, Realtime, Storage, and Edge Functions.
- **Full Relational PostgreSQL Power**: Direct access to real PostgreSQL with extensions (pgvector, PostGIS, pg_cron) and zero proprietary vendor lock-in.
- **Row-Level Security (RLS) Authorization**: Securing multi-tenant client queries directly at the database layer via SQL security policies.
- **Real-Time Database Subscriptions**: Subscribing to PostgreSQL insert, update, and delete events over WebSockets from client apps.

## Quick Start

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient("https://xyz.supabase.co", "public-anon-key");

// Listen to changes
const subscription = supabase
  .channel("public:messages")
  .on(
    "postgres_changes",
    { event: "INSERT", schema: "public", table: "messages" },
    (payload) => {
      console.log("New message:", payload);
    },
  )
  .subscribe();
```

## Core Concepts

### PostgreSQL Row-Level Security (RLS)

Protects data at the database layer so clients can query the database directly from web/mobile apps safely:

```sql
-- Enable RLS on Table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Allow users to read and update only documents they own
CREATE POLICY "Users access own documents"
ON documents
FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

### Modern Supabase JavaScript / TypeScript Client

Type-safe database queries, authentication, and file storage:

```typescript
import { createClient } from "@supabase/supabase-js";
import { Database } from "./types/supabase";

const supabase = createClient<Database>(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!,
);

// Query with automated RLS enforcement
const { data: projects, error } = await supabase
  .from("projects")
  .select("id, title, tasks(id, name, status)")
  .eq("status", "active")
  .order("created_at", { ascending: false });
```

### Real-Time WebSocket Broadcasts & Presence

Streams live changes and synchronizes user presence states:

```typescript
// Subscribe to real-time database changes on orders table
const channel = supabase
  .channel("db-changes")
  .on(
    "postgres_changes",
    { event: "INSERT", schema: "public", table: "orders" },
    (payload) => {
      console.log("New Order Created:", payload.new);
    },
  )
  .subscribe();
```

## Common Patterns

### Row Level Security (RLS) Policy for Multi-Tenant Isolation

**Problem**: APIs accidentally leaking private user records when client queries lack manual tenant filtering.

**Solution**:
Enforce database-level Row Level Security using `auth.uid()`:

```sql
-- Enable RLS
ALTER TABLE user_notes ENABLE ROW LEVEL SECURITY;

-- Restrict reads and writes exclusively to the owning user
CREATE POLICY "Users can only access own notes"
ON user_notes
FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

## Best Practices

**Do**:

- Always Enable Row-Level Security (RLS): Never expose a table to the public API without enabling and testing RLS policies.
- Generate Strict TypeScript Types: Use the Supabase CLI (`supabase gen types typescript`) to keep database schemas strongly typed.
- Index Columns Used in RLS Policies: Add indexes on `user_id` or `organization_id` to prevent slow table scans during policy evaluations.
- Use Edge Functions for Sensitive Logic: Keep private API secrets and payment integrations inside server-side Edge Functions.

**Don't**:

- Expose the `service_role` key in client code: The `service_role` key bypasses all RLS policies; keep it strictly on secure servers.
- Write complex nested subqueries in RLS policies: Slow RLS subqueries multiply latency on every single row check.
- Skip database migrations in Git: Use `supabase migration new` and version control all database DDL changes.

## Troubleshooting

| Error                                       | Cause                                                                     | Solution                                                                              |
| :------------------------------------------ | :------------------------------------------------------------------------ | :------------------------------------------------------------------------------------ |
| `Empty array [] returned from SELECT query` | RLS is enabled on table but no policy matches current authenticated user. | Create appropriate RLS policy or verify client JWT token contains valid user session. |
| `JWT expired / Invalid refresh token`       | User session token expired without refreshing.                            | Call `supabase.auth.refreshSession()` or handle auth state change listener.           |
| `Database connection limit exceeded`        | Serverless edge functions exceeding direct Postgres connections.          | Use Supabase connection pooling (port 6543) via PgBouncer.                            |

## References

- [Supabase Docs](https://supabase.com/docs)
