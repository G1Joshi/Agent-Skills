---
name: cosmosdb
description: Expert Azure Cosmos DB assistance covering NoSQL API, partition key design, Request Units (RU/s) optimization, and change feed. Use when building globally distributed, multi-master Azure applications.
---

# Azure Cosmos DB

Cosmos DB is Azure's planetary-scale database. It supports multiple APIs: NoSQL (Core/JSON), MongoDB, PostgreSQL, Cassandra, Gremlin (Graph), and Table.

## When to Use

- **Global Enterprise Applications on Azure**: Fully managed NoSQL database with turnkey multi-region replication and single-digit millisecond latency SLAs.
- **Multi-Model API Compatibility**: Using existing MongoDB, Apache Cassandra, Gremlin (Graph), or PostgreSQL skills via native Cosmos DB APIs.
- **Dynamic Scale & Autoscale Request Units (RU/s)**: Applications with seasonal traffic spikes scaling compute and throughput instantly.
- **Guaranteed Consistency Options**: Tuning consistency across 5 distinct levels (Strong, Bounded Staleness, Session, Consistent Prefix, Eventual).

## Quick Start

```csharp
Container container = database.GetContainer("Items");

Item item = new Item
{
    Id = "1",
    Category = "Personal",
    Name = "Groceries"
};

await container.CreateItemAsync(item, new PartitionKey(item.Category));
```

## Core Concepts

### Request Units (RU/s) Throughput Currency

Throughput is normalized into Request Units; a 1KB point read costs 1 RU:

```typescript
// Azure Cosmos DB Node.js SDK (NoSQL API)
import { CosmosClient } from "@azure/cosmos";

const client = new CosmosClient({
  endpoint: process.env.COSMOS_ENDPOINT!,
  key: process.env.COSMOS_KEY!,
});

const container = client.database("CommerceDb").container("Orders");

// Point read with exact partition key (Cost: 1 RU)
const { resource, requestCharge } = await container
  .item("order_415", "customer_99")
  .read();
console.log(`Retrieved order. Request Charge: ${requestCharge} RUs`);
```

### Partition Key Selection (Physical vs Logical Partitions)

The partition key determines how items are distributed across physical servers; high-cardinality keys ensure even distribution:

```json
// Items must include the partition key property
{
  "id": "order_415",
  "customerId": "customer_99", // Partition Key
  "totalAmount": 149.5,
  "orderStatus": "SHIPPED"
}
```

### Change Feed Microservice Architecture

Streams real-time container mutations to trigger Azure Functions, microservices, or search index updates:

```typescript
// Read Cosmos DB Change Feed
const changeFeedIterator = container.items.changeFeed({
  startTime: new Date(Date.now() - 3600000), // Last hour
});

while (changeFeedIterator.hasMoreResults) {
  const response = await changeFeedIterator.readNext();
  response.result?.forEach((mutatedDoc) =>
    console.log("Changed:", mutatedDoc.id),
  );
}
```

## Common Patterns

### Synthetic Partition Key for Even RU Distribution

**Problem**: Partition hot-spotting occurs when partitioning only by tenant or date, throttling operations with 429 errors.

**Solution**:
Construct synthetic partition keys combining category and hash suffix:

```javascript
const userProfile = {
  id: "order_12345",
  tenantId: "acme",
  // Synthetic key: tenant + hash bucket (0-9)
  partitionKey: `acme_${hashCode("order_12345") % 10}`,
  amount: 250.0,
  createdAt: new Date().toISOString(),
};

await container.items.create(userProfile);
```

## Best Practices

**Do**:

- Choose High-Cardinality Partition Keys: Select partition keys like `userId`, `tenantId`, or `deviceDate` to prevent hot-partition throttle errors (HTTP 429).
- Default to Session Consistency: Use Session consistency for 90% of web apps; it guarantees read-your-own-writes at optimal cost.
- Enable Autoscale RU/s: Configure autoscale (e.g. 1,000 to 10,000 RU/s) for unpredictable production workloads to eliminate manual scaling.
- Leverage the Change Feed: Decouple post-write integrations (sending emails, updating caches) using Cosmos DB Change Feed triggers.

**Don't**:

- Execute cross-partition queries frequently: Queries without a partition key scan all physical partitions, consuming hundreds of RUs.
- Use Cosmos DB for heavy OLAP data warehousing: Use Azure Synapse or Fabric for petabyte analytical batch jobs.
- Leave index policies unoptimized: Exclude unused string paths from indexing to reduce write RU consumption.

## Troubleshooting

| Error                                      | Cause                                                                | Solution                                                                        |
| :----------------------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| `Request rate too large (Status code 429)` | Consumed Request Units exceeded provisioned or autoscale RU/s limit. | Implement exponential backoff, review partition key hot spots, or scale RU/s.   |
| `Resource Not Found (404)`                 | Item queried without providing the required partition key header.    | Always pass both item ID and partition key: `container.item(id, partitionKey)`. |
| `Precondition Failed (412)`                | Optimistic concurrency conflict due to mismatched `_etag`.           | Re-fetch the item, apply modifications to fresh state, and retry write.         |

## References

- [Azure Cosmos DB Documentation](https://learn.microsoft.com/en-us/azure/cosmos-db/)
