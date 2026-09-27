---
name: drizzle
description: Expert Drizzle ORM assistance covering type-safe schema declaration, migrations, relations, and serverless database clients. Use when building performant TypeScript apps with PostgreSQL, MySQL, or SQLite.
---

# Drizzle ORM

Drizzle is the lightweight challenger to Prisma. v0.30+ (2025) focuses on **SQL-like** syntax, zero dependencies at runtime, and extreme cold-start performance.

## When to Use

- **TypeScript-First Object Relational Mapping**: Lightweight, SQL-like ORM with zero code-generation overhead and maximum type safety.
- **Serverless & Edge Runtimes**: Next.js, Cloudflare Workers, Bun, Supabase, and AWS Lambda with zero cold-start penalty.
- **Relational Databases with Precise Control**: PostgreSQL, MySQL, and SQLite requiring explicit query execution and predictable SQL output.
- **Schema-as-Code & Declarative Migrations**: Managing migrations cleanly with `drizzle-kit`.

## Quick Start

```typescript
// schema.ts
import { pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  createdAt: timestamp("created_at").defaultNow(),
});

// query.ts
import { drizzle } from "drizzle-orm/node-postgres";
import { users } from "./schema";

const db = drizzle(process.env.DATABASE_URL);
const allUsers = await db.select().from(users);
```

## Core Concepts

#Declarative Schema Definition with Relationships

Type-safe table schemas and foreign key relations:

```typescript
import {
  pgTable,
  serial,
  text,
  timestamp,
  integer,
  boolean,
} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: text("email").notNull().unique(),
  fullName: text("full_name").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  authorId: integer("author_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  published: boolean("published").default(false).notNull(),
});

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

#Relational Queries & SQL-Like Filtering

Intuitive query API combining SQL syntax with relational loading:

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import { eq, desc, and } from "drizzle-orm";
import { users, posts } from "./schema";

const db = drizzle(process.env.DATABASE_URL!);

// Relational query mode
async function getAuthorWithPosts(userId: number) {
  return await db.query.users.findFirst({
    where: eq(users.id, userId),
    with: {
      posts: {
        where: eq(posts.published, true),
        orderBy: [desc(posts.id)],
      },
    },
  });
}

// SQL-like query builder mode
async function updatePostStatus(postId: number, isPublished: boolean) {
  return await db
    .update(posts)
    .set({ published: isPublished })
    .where(eq(posts.id, postId))
    .returning();
}
```

#Drizzle Kit Migrations & Introspection

Declarative migration generation and application:

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
});
```

## Common Patterns

### Relational Queries with Prepared Statements

**Problem**: Writing complex SQL joins while retaining strict compile-time TypeScript type inference.

**Solution**:
Use Drizzle's Relational Queries API:

```typescript
import { eq } from "drizzle-orm";

const userWithPosts = await db.query.users.findFirst({
  where: eq(users.id, 1),
  with: {
    posts: {
      columns: { title: true, createdAt: true },
      limit: 5,
    },
  },
});
```

## Best Practices (2026)

- **Do** split schemas into modular domain files and export them through a centralized `schema.ts`.
- **Do** use `db.query` for nested relational reads and standard SQL query builder for mutations and bulk operations.
- **Do** run `drizzle-kit check` and `drizzle-kit generate` in CI to detect schema discrepancies before deployment.
- **Do** specify `onDelete` cascades explicitly on all foreign key constraints.
- **Don't** perform multiple round-trips for insert-then-read; use `.returning()` to fetch modified rows immediately.
- **Don't** instantiate multiple database client connections in serverless edge handlers; reuse client instances.
- **Don't** mix multiple SQL dialects in a single schema definition.

## Troubleshooting

| Error                                                     | Cause                                                              | Solution                                                               |
| :-------------------------------------------------------- | :----------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `Error: relation "..." does not exist`                    | Migrations have not been generated or pushed to database.          | Run `npx drizzle-kit generate` and `npx drizzle-kit migrate`.          |
| `Type error: Property 'query' does not exist on type ...` | Schema not passed to `drizzle(client, { schema })` initialization. | Pass your schema object: `drizzle(client, { schema: { ...schema } })`. |
| `duplicate key value violates unique constraint`          | Inserting record with existing unique column value.                | Use `.onConflictDoNothing()` or `.onConflictDoUpdate()`.               |

## References

- [Drizzle ORM Documentation](https://orm.drizzle.team/)
