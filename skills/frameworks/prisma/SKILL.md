---
name: prisma
description: Expert Prisma ORM assistance covering Prisma schema, migrations, type-safe queries, relation filters, and Accelerate. Use when modeling databases and querying SQL in TypeScript/JavaScript.
---

# Prisma

Prisma is a next-generation Node.js and TypeScript ORM featuring declarative schema modeling, automated type-safe database queries, and robust migration tooling.

## When to Use

- **TypeScript-First Database Modeling**: Declarative data models with automated migrations and end-to-end type safety.
- **Next.js & Node.js Enterprise Backends**: Developing web services with Prisma Client and PostgreSQL/MySQL/SQLite/MongoDB.
- **Safe Relational Query Composition**: Fluent queries with deeply nested relations, filtering, and pagination.
- **Prisma Accelerate & Pulse**: Edge caching, connection pooling, and real-time database change-event subscriptions.

## Quick Start

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  posts Post[]
}

model Post {
  id        Int     @id @default(autoincrement())
  title     String
  authorId  Int
  author    User    @relation(fields: [authorId], references: [id])
}
```

```typescript
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

const users = await prisma.user.findMany({ include: { posts: true } });
```

## Core Concepts

### Declarative Schema Definition with Relations

Defining entities, indexes, and referential constraints:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int       @id @default(autoincrement())
  email     String    @unique
  name      String?
  posts     Post[]
  createdAt DateTime  @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId  Int

  @@index([authorId])
}
```

### Type-Safe CRUD & Nested Relational Queries

Reading and writing related data in single operations:

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function createUserWithPost() {
  const user = await prisma.user.create({
    data: {
      email: "alex@example.com",
      name: "Alex Rivera",
      posts: {
        create: [{ title: "Getting Started with Prisma", published: true }],
      },
    },
    include: {
      posts: true,
    },
  });

  return user;
}
```

### Interactive Transactions with $transaction

Executing multi-step operations with ACID guarantees:

```typescript
async function transferFunds(
  fromUserId: number,
  toUserId: number,
  amount: number,
) {
  return await prisma.$transaction(async (tx) => {
    const sender = await tx.account.update({
      where: { userId: fromUserId },
      data: { balance: { decrement: amount } },
    });

    if (sender.balance < 0) {
      throw new Error("Insufficient funds");
    }

    const receiver = await tx.account.update({
      where: { userId: toUserId },
      data: { balance: { increment: amount } },
    });

    return { sender, receiver };
  });
}
```

## Common Patterns

### Interactive Transactions with Rollback Safety

**Problem**: Updating multiple tables where failure of any step must roll back previous changes.

**Solution**:
Use `$transaction` closure:

```typescript
const result = await prisma.$transaction(async (tx) => {
  const sender = await tx.account.update({
    where: { id: fromAccountId },
    data: { balance: { decrement: amount } },
  });

  if (sender.balance < 0) {
    throw new Error("Insufficient funds for transfer");
  }

  const recipient = await tx.account.update({
    where: { id: toAccountId },
    data: { balance: { increment: amount } },
  });

  return { sender, recipient };
});
```

## Best Practices

**Do**:

- Instantiate a single `PrismaClient` instance globally in development to prevent connection pool exhaustion.
- Use `select` clauses in queries to fetch only necessary columns instead of full rows.
- Run `prisma migrate deploy` in CI/CD production deployment pipelines.
- Leverage interactive transactions (`prisma.$transaction(async (tx) => ...)`) for ACID workflows.

**Don't**:

- Create new `PrismaClient()` instances inside serverless request handler functions.
- Run `prisma db push` in production; use `prisma migrate` to preserve migration history.
- Use `$queryRawUnsafe` with concatenated user strings; use parameterized `$queryRaw`.

## Troubleshooting

| Error                                                           | Cause                                                           | Solution                                                     |
| :-------------------------------------------------------------- | :-------------------------------------------------------------- | :----------------------------------------------------------- |
| `PrismaClientInitializationError: Can't reach database server`  | Database offline, network partition, or invalid `DATABASE_URL`. | Check database connection string and network reachability.   |
| `PrismaClientKnownRequestError: P2002 Unique constraint failed` | Attempting to insert a duplicate value for a `@unique` column.  | Catch code `P2002` and return user-friendly duplicate error. |
| `Prisma Client not initialized / outdated types`                | Schema was modified without regenerating client.                | Run `npx prisma generate` after modifying `schema.prisma`.   |

## References

- [Prisma Documentation](https://www.prisma.io/)
