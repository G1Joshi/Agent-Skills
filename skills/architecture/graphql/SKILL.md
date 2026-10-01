---
name: graphql
description: Expert GraphQL architecture assistance covering schema definition language (SDL), resolver design, DataLoader batching, schema stitching/federation, and client caching. Use when designing GraphQL APIs, preventing N+1 query problems, building Apollo/Relay schemas, or aggregating data from multiple services.
---

# GraphQL

GraphQL is a query language for APIs and a runtime for fulfilling those queries with your existing data. It gives clients the power to ask for exactly what they need and nothing more.

## When to Use

- **Client-Driven Data Fetching**: Web and mobile clients with drastically different UI layout requirements consuming the same API.
- **Over-Fetching & Under-Fetching Mitigation**: Allowing clients to request the exact fields needed for a view in a single HTTP request.
- **API Aggregation & Federated Supergraphs**: Combining dozens of microservice APIs into a unified GraphQL schema via Apollo Federation.
- **Real-Time Subscriptions**: Streaming live changes to clients over WebSockets or HTTP Server-Sent Events (SSE).

## Quick Start

```graphql
# The Schema
type User {
  id: ID!
  name: String!
  orders: [Order]
}

type Query {
  user(id: ID!): User
}
```

```javascript
// The Query (Client)
query {
  user(id: "123") {
    name
    orders {
      total
      status
    }
  }
}
```

## Core Concepts

### Strongly-Typed Schema Definition (SDL)

Defines types, relationships, queries, and mutations strictly:

```graphql
# schema.graphql
type Query {
  project(id: ID!): Project
}

type Mutation {
  assignTask(input: AssignTaskInput!): Task!
}

type Project {
  id: ID!
  name: String!
  tasks(status: TaskStatus): [Task!]!
}

type Task {
  id: ID!
  title: String!
  assignee: User
}
```

### Resolvers & Hierarchical Execution

Each field on a type maps to an independent resolver function:

```typescript
// resolvers.ts
export const resolvers = {
  Query: {
    project: async (_parent, { id }, ctx) => ctx.db.getProject(id),
  },
  Project: {
    // Resolved only if the client requested the "tasks" field
    tasks: async (project, { status }, ctx) =>
      ctx.db.getTasksForProject(project.id, status),
  },
};
```

### DataLoader Request Batching & Deduplication

Batches individual resolver database lookups into a single SQL `IN` query to prevent N+1 query storms:

```typescript
import DataLoader from "dataloader";

export function createUserDataLoader(db: Database) {
  return new DataLoader(async (userIds: readonly string[]) => {
    const users = await db.query("SELECT * FROM users WHERE id = ANY($1)", [
      userIds,
    ]);
    const userMap = new Map(users.map((u) => [u.id, u]));
    return userIds.map((id) => userMap.get(id) || null);
  });
}
```

## Common Patterns

### DataLoader N+1 Query Prevention

**Problem**: Nested resolvers trigger separate SQL queries for each child record (N+1 database reads).  
**Solution**: Batch and cache database reads using DataLoader.

```typescript
import DataLoader from "dataloader";

// Batch function receives array of IDs collected across concurrent resolvers
const authorLoader = new DataLoader(async (authorIds: readonly string[]) => {
  const authors = await db
    .select()
    .from(authorsTable)
    .where(inArray(authorsTable.id, authorIds as string[]));
  const authorMap = new Map(authors.map((a) => [a.id, a]));
  return authorIds.map((id) => authorMap.get(id) || null);
});

// Resolver consumes DataLoader
export const resolvers = {
  Book: {
    author: (book: { authorId: string }) => authorLoader.load(book.authorId),
  },
};
```

## Best Practices

**Do**:

- Always Use DataLoader for Relational Fields: Never allow nested child resolvers to execute raw database queries in a loop.
- Implement Query Complexity Limits: Use libraries like `graphql-query-complexity` to reject nested query abuse before execution.
- Paginate List Fields with Cursors: Follow the Relay Connection specification (`edges`, `node`, `pageInfo`) for robust infinite scroll.
- Persist Queries in Production: Use Persisted Queries (hashes) to prevent arbitrary unbounded query submission from untrusted clients.

**Don't**:

- Expose internal database schemas directly as GraphQL types: Design domain schemas optimized for frontend views.
- Return generic HTTP 500 errors for business failures: Return structured validation errors inside GraphQL response payloads.
- Ignore HTTP caching: GraphQL POST requests bypass browser caches; use CDN Edge caching with Cache-Control headers.

## Troubleshooting

| Error                | Cause                     | Solution                                               |
| :------------------- | :------------------------ | :----------------------------------------------------- |
| `Cannot query field` | Typo or field restricted. | Check Schema and Introspection.                        |
| `N+1 Performance`    | Slow response on lists.   | Implement DataLoader.                                  |
| `Caching`            | Hard to cache via HTTP.   | Use Normalized Caching in Client (Apollo Client/Urql). |

## References

- [GraphQL.org](https://graphql.org/)
- [Apollo GraphQL](https://www.apollographql.com/)
