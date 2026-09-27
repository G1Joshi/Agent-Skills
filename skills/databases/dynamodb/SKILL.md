---
name: dynamodb
description: Expert AWS DynamoDB assistance covering single-table design, Partition and Sort keys, GSIs, DynamoDB Streams, and TTL. Use when designing serverless NoSQL applications, high-scale key-value stores, or event-driven pipelines.
---

# Amazon DynamoDB

DynamoDB is a fully managed, serverless, key-value NoSQL database designed to run high-performance applications at any scale (Single-digit millisecond latency).

## When to Use

- **Single-Digit Millisecond Key-Value at Any Scale**: AWS managed NoSQL database scaling horizontally to millions of requests per second.
- **Serverless Web Backends (AWS Lambda)**: Applications requiring serverless pay-per-request pricing and zero connection-pool management.
- **Single-Table Design Architectures**: Modeling complex one-to-many and many-to-many relationships in a single unified DynamoDB table.
- **Global Multi-Region Replication**: Deploying active-active multi-region applications with DynamoDB Global Tables.

## Quick Start

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

#Partition Key (PK) & Sort Key (SK) Architecture

The Partition Key determines physical partition routing; the Sort Key dictates B-Tree ordering within the partition:

```
[ Single DynamoDB Table ]
  ├── PK: USER#101 | SK: METADATA        -> User Profile Record
  ├── PK: USER#101 | SK: ORDER#2026-0901 -> Order Record 1
  └── PK: USER#101 | SK: ORDER#2026-0925 -> Order Record 2
```

#Global Secondary Indexes (GSI) Inversion

Enables reverse lookups without scanning the entire table:

```typescript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, QueryCommand } from "@aws-sdk/lib-dynamodb";

const ddbDoc = DynamoDBDocumentClient.from(
  new DynamoDBClient({ region: "us-east-1" }),
);

// Query using GSI (Inverted Index: Find all users belonging to an organization)
const { Items } = await ddbDoc.send(
  new QueryCommand({
    TableName: "EnterpriseTable",
    IndexName: "GSI_1",
    KeyConditionExpression:
      "GSI1_PK = :orgId AND begins_with(GSI1_SK, :prefix)",
    ExpressionAttributeValues: {
      ":orgId": "ORG#enterprise_corp",
      ":prefix": "USER#",
    },
  }),
);
```

#DynamoDB Streams & Event-Driven Processing

Captures item-level change events to trigger asynchronous AWS Lambda functions:

```
[ Table Write ] ──Capture Mutation──→ [ DynamoDB Streams ] ──Trigger──→ [ Lambda Worker ] ──→ [ OpenSearch Sync ]
```

## Common Patterns

### Single-Table Design with Composite Sort Keys

**Problem**: Traditional multi-table relational designs in DynamoDB require expensive multi-query joins.

**Solution**:
Store multiple entity types in a single table using generic PK/SK keys:

```json
[
  {
    "PK": "USER#1001",
    "SK": "METADATA",
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  {
    "PK": "USER#1001",
    "SK": "ORDER#2025-03-01#9981",
    "status": "SHIPPED",
    "total": 149.99
  }
]
```

```javascript
// Query user and recent orders in a single round-trip
const params = {
  TableName: "StoreData",
  KeyConditionExpression: "PK = :pk AND SK begins_with(:orderPrefix)",
  ExpressionAttributeValues: {
    ":pk": "USER#1001",
    ":orderPrefix": "ORDER#",
  },
};
```

## Best Practices (2026)

**Do**:

- **Adopt Single-Table Design**: Group related entity types into a single table to fetch parent and children in a single `Query` call.
- **Always Prefer `Query` Over `Scan`**: Never run `Scan` operations in production application code paths; scans consume massive RCU/WCU.
- **Use On-Demand Capacity for Variable Workloads**: Avoid provisioned throttling errors by starting with On-Demand billing.
- **Configure Time to Live (TTL)**: Automatically expire session records, temporary tokens, and transient logs at zero cost.

**Don't**:

- **Don't use low-cardinality Partition Keys**: Keys like `gender` or `status` route all traffic to a single partition, triggering hot-partition throttling.
- **Don't project all attributes into GSIs (`ALL`)**: Project only needed attributes (`KEYS_ONLY` or `INCLUDE`) to reduce storage and write costs.
- **Don't execute transactions (`TransactWriteItems`) unnecessarily**: Transactions cost double the write capacity units of standard puts.

## Troubleshooting

| Error                                                     | Cause                                                          | Solution                                                                         |
| :-------------------------------------------------------- | :------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `ProvisionedThroughputExceededException`                  | Consumed capacity exceeded table or GSI provisioned RCUs/WCUs. | Switch to On-Demand capacity or implement exponential backoff retry logic.       |
| `ValidationException: Item size has exceeded 400KB limit` | Document payload exceeds maximum DynamoDB item limit.          | Compress payload or store large binaries in S3, keeping only S3 URI in DynamoDB. |
| `TransactionCanceledException`                            | One condition check failed in `TransactWriteItems`.            | Check condition expressions across all transactional items.                      |

## References

- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
