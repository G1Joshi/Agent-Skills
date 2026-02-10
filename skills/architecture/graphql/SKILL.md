---
name: graphql
description: GraphQL API query language with schema. Use for flexible APIs.
---

# GraphQL

GraphQL is a query language for APIs and a runtime for fulfilling those queries with your existing data. It gives clients the power to ask for exactly what they need and nothing more.

## When to Use

- **Mobile Apps**: Minimize bandwidth by fetching only needed fields.
- **Complex Systems**: Fetching related data (User + Orders + Products) in a single request.
- **Rapid Iteration**: Frontend can change data requirements without Backend changes.

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

### Schema First

The schema (`.graphql`) is the contract. Teams agree on the schema before writing code.

### Resolvers

Functions that fetch the data for a specific field in the schema.

### Strong Typing

Every field has a specific type (Int, String, Object). Validation happens automatically.

## Common Patterns

### n+1 Problem

Fetching a list of users and then firing a separate DB query for each user's address.

- **Solution**: **DataLoader**. Batches requests into a single query (`WHERE id IN (...)`).

### Federation

Splitting a single GraphQL graph across multiple services (Microservices). Apollo Federation is the standard.

## Best Practices

**Do**:

- Use **Fragments** on the client to reuse query logic.
- Limit **Query Depth** to prevent DoS attacks (e.g., `user { friends { friends { friends ... } } }`).
- Use **Cursor-based Pagination** for infinite scrolling lists.

**Don't**:

- Don't simply wrap a REST API 1:1. Redesign for the Graph.
- Don't utilize it for simple binary file uploads (use Signed URLs + REST/S3 for that).

## Troubleshooting

| Error                | Cause                     | Solution                                               |
| :------------------- | :------------------------ | :----------------------------------------------------- |
| `Cannot query field` | Typo or field restricted. | Check Schema and Introspection.                        |
| `N+1 Performance`    | Slow response on lists.   | Implement DataLoader.                                  |
| `Caching`            | Hard to cache via HTTP.   | Use Normalized Caching in Client (Apollo Client/Urql). |

## References

- [GraphQL.org](https://graphql.org/)
- [Apollo GraphQL](https://www.apollographql.com/)
