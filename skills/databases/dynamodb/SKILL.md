---
name: dynamodb
description: AWS DynamoDB serverless NoSQL with streams and global tables. Use for AWS serverless.
---

# Amazon DynamoDB

DynamoDB is a fully managed, serverless, key-value NoSQL database designed to run high-performance applications at any scale (Single-digit millisecond latency).

## When to Use

- **Serverless Apps**: The default DB for AWS Lambda.
- **Infinite Scaling**: Handles petabytes of data without maintenance.
- **Shopping Carts / Sessions**: High throughput, simple key access.

## Quick Start (AWS SDK v3)

```typescript
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({});
const command = new PutItemCommand({
  TableName: "Users",
  Item: {
    PK: { S: "USER#123" },
    SK: { S: "PROFILE" },
    Name: { S: "Alice" },
  },
});
await client.send(command);
```

## Core Concepts

### Partition Key (PK) & Sort Key (SK)

- **PK**: Determines which partition holds the data. Must be unique unless SK is present.
- **SK**: Sorts items with the same PK.
- **Composite Key**: PK + SK together form the primary ID.

### Single Table Design (The "OneTable" Pattern)

Storing multiple entity types (Users, Orders) in one table to enable pre-joining data via item collections. (Less strictly required now, but still common).

### Provisioned vs On-Demand

- **On-Demand**: Pay per request. Good for spiky/unknown loads.
- **Provisioned**: Pay for capacity. Cheaper for predictable loads.

## Best Practices (2025)

**Do**:

- **Access Patterns First**: Design your schema based on _how_ you will query the data. You cannot easily add arbitrary queries later.
- **Use GSI (Global Secondary Index)**: To query by non-key attributes.
- **Use TTL**: To verify old items are deleted automatically (free delete).

**Don't**:

- **Don't Scan**: Scan reads the _entire_ table. It is slow and expensive. Always `Query`.
- **Don't store large blobs**: 400KB limit per item. Store large data in S3 and save the link in Dynamo.

## References

- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
