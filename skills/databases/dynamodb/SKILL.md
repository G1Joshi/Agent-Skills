---
name: dynamodb
description: AWS DynamoDB serverless NoSQL with streams, global tables, and single-table design. Use for AWS serverless.
---

# DynamoDB

AWS serverless NoSQL database with single-table design and global distribution.

## When to Use

- AWS serverless applications
- High-scale read/write workloads
- Global multi-region deployment
- Event-driven architectures

## Quick Start

```javascript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  PutCommand,
  GetCommand,
} from "@aws-sdk/lib-dynamodb";

const client = DynamoDBDocumentClient.from(new DynamoDBClient({}));

// Put item
await client.send(
  new PutCommand({
    TableName: "Users",
    Item: {
      pk: "USER#123",
      sk: "PROFILE",
      name: "John",
      email: "john@example.com",
    },
  }),
);

// Get item
const { Item } = await client.send(
  new GetCommand({
    TableName: "Users",
    Key: { pk: "USER#123", sk: "PROFILE" },
  }),
);
```

## Core Concepts

### Single-Table Design

```javascript
// One table, multiple entity types
const items = [
  // User
  { pk: "USER#123", sk: "PROFILE", name: "John", type: "User" },

  // User's orders
  { pk: "USER#123", sk: "ORDER#001", total: 99.99, type: "Order" },
  { pk: "USER#123", sk: "ORDER#002", total: 149.99, type: "Order" },

  // Order lookup (GSI)
  { pk: "ORDER#001", sk: "USER#123", total: 99.99, type: "Order" },
];
```

### Queries

```javascript
import { QueryCommand } from "@aws-sdk/lib-dynamodb";

// Get all user's orders
const { Items } = await client.send(
  new QueryCommand({
    TableName: "MyTable",
    KeyConditionExpression: "pk = :pk AND begins_with(sk, :sk)",
    ExpressionAttributeValues: {
      ":pk": "USER#123",
      ":sk": "ORDER#",
    },
  }),
);

// Query with filter
const result = await client.send(
  new QueryCommand({
    TableName: "MyTable",
    IndexName: "GSI1",
    KeyConditionExpression: "gsi1pk = :type",
    FilterExpression: "price > :minPrice",
    ExpressionAttributeValues: {
      ":type": "PRODUCT",
      ":minPrice": 100,
    },
  }),
);
```

## Common Patterns

### Transactions

```javascript
import { TransactWriteCommand } from "@aws-sdk/lib-dynamodb";

await client.send(
  new TransactWriteCommand({
    TransactItems: [
      {
        Update: {
          TableName: "Table",
          Key: { pk: "ACCOUNT#1", sk: "BALANCE" },
          UpdateExpression: "SET amount = amount - :amt",
          ExpressionAttributeValues: { ":amt": 100 },
        },
      },
      {
        Update: {
          TableName: "Table",
          Key: { pk: "ACCOUNT#2", sk: "BALANCE" },
          UpdateExpression: "SET amount = amount + :amt",
          ExpressionAttributeValues: { ":amt": 100 },
        },
      },
    ],
  }),
);
```

## Best Practices

**Do**:

- Use single-table design
- Design access patterns first
- Use sparse GSIs efficiently
- Enable point-in-time recovery

**Don't**:

- Scan tables in production
- Create table per entity type
- Ignore hot partition keys
- Use filter as primary query

## Troubleshooting

| Issue      | Cause            | Solution                |
| ---------- | ---------------- | ----------------------- |
| Throttling | Hot partition    | Better key distribution |
| Slow scan  | Full table scan  | Use Query with GSI      |
| High cost  | Over-provisioned | Use on-demand mode      |

## References

- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [DynamoDB Book](https://www.dynamodbbook.com/)
