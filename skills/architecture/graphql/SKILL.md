---
name: graphql
description: GraphQL API design with queries, mutations, and subscriptions. Use for flexible APIs.
---

# GraphQL

Query language for APIs with typed schemas.

## When to Use

- Complex data requirements
- Multiple client types
- Avoiding over-fetching
- Real-time subscriptions

## Quick Start

```typescript
import { ApolloServer } from "@apollo/server";

const typeDefs = `
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }
  
  type Query {
    user(id: ID!): User
    users: [User!]!
  }
`;

const resolvers = {
  Query: {
    user: (_, { id }) => db.users.findUnique({ where: { id } }),
    users: () => db.users.findMany(),
  },
};
```

## Core Concepts

### Schema Definition

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, limit: Int = 10): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  userCreated: User!
}

input CreateUserInput {
  name: String!
  email: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}
```

### Resolvers

```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      return context.dataSources.users.getById(id);
    },
  },

  Mutation: {
    createUser: async (_, { input }, context) => {
      return context.dataSources.users.create(input);
    },
  },

  User: {
    posts: async (parent, _, context) => {
      return context.dataSources.posts.getByUserId(parent.id);
    },
  },
};
```

## Common Patterns

### DataLoader

```typescript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await db.users.findMany({
    where: { id: { in: ids } },
  });
  return ids.map(id => users.find(u => u.id === id) || null);
});

// Resolver
User: {
  author: (post) => userLoader.load(post.authorId),
}
```

### Error Handling

```typescript
import { GraphQLError } from "graphql";

const resolvers = {
  Mutation: {
    createUser: async (_, { input }) => {
      const existing = await db.users.findUnique({
        where: { email: input.email },
      });

      if (existing) {
        throw new GraphQLError("Email already exists", {
          extensions: { code: "BAD_USER_INPUT" },
        });
      }

      return db.users.create({ data: input });
    },
  },
};
```

## Best Practices

**Do**:

- Use DataLoader for batching
- Implement pagination
- Add input validation
- Use proper error codes

**Don't**:

- Return excessive data
- Skip authorization
- Ignore N+1 queries
- Over-complicate schema

## Troubleshooting

| Issue        | Cause              | Solution             |
| ------------ | ------------------ | -------------------- |
| N+1 queries  | Missing DataLoader | Add batching         |
| Slow queries | Deep nesting       | Add depth limiting   |
| Type error   | Schema mismatch    | Check resolver types |

## References

- [GraphQL Documentation](https://graphql.org/learn/)
- [Apollo Server](https://www.apollographql.com/docs/apollo-server/)
