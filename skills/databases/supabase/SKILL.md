---
name: supabase
description: Supabase PostgreSQL backend-as-a-service with realtime. Use for serverless PostgreSQL.
---

# Supabase

Supabase is an open source Firebase alternative. It provides a dedicated PostgreSQL database, packaged with Authentication, Realtime subscriptions, Storage, and Edge Functions.

## When to Use

- **Rapid Application Development**: Get Auth + DB + APIs in 5 minutes.
- **Postgres Power**: Unlike Firebase, you have full SQL power (JOINs, aggregation).
- **Realtime**: Subscribe to DB changes via WebSockets.
- **Vector/AI**: Highly integrated `pgvector` support for AI apps.

## Quick Start (JS)

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

### Row Level Security (RLS)

Supabase exposes the DB directly to the frontend (via PostgREST). RLS is **critical** to secure data.

```sql
CREATE POLICY "Users can see own data" ON "profiles"
FOR SELECT USING (auth.uid() = user_id);
```

### PostgREST

Automatically turns your Database Tables into RESTful APIs.

### Extensions

Supabase makes enabling Postgres extensions easy (PostGIS, pgvector, pg_cron).

## Best Practices (2025)

**Do**:

- **Enable RLS immediately**: Never launch without RLS policies.
- **Use Supabase CLI**: For local development and migrations. Develop locally, push to prod.
- **Use Generated Types**: `supabase gen types typescript` generates accurate TS definitions from your DB schema.

**Don't**:

- **Don't access `service_role` key in client**: Allows bypassing RLS. Server-side only.
- **Don't put business logic in triggers**: Hard to debug. Use Database Webhooks or Edge Functions.

## References

- [Supabase Docs](https://supabase.com/docs)
