---
name: cosmosdb
description: Azure Cosmos DB multi-model database with global distribution. Use for Azure.
---

# Azure Cosmos DB

Cosmos DB is Azure's planetary-scale database. It supports multiple APIs: NoSQL (Core/JSON), MongoDB, PostgreSQL, Cassandra, Gremlin (Graph), and Table.

## When to Use

- **Global Distribution**: Replicate data to any Azure region with a click.
- **Multi-Model**: If you need Mongo or Postgres APIs but want "PaaS" management.
- **Low Latency**: Guaranteed <10ms read/write latency at the 99th percentile.

## Quick Start (NoSQL API)

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

### Request Units (RUs)

The currency of Cosmos DB. Use RUs to pay for throughput. 1 RU ≈ reading a 1KB doc.

### Partition Key

Crucial. Determines how data is distributed. A bad partition key ("Date") creates "Hot Partitions" (bottlenecks). A good key ("UserId") distributes load evenly.

### Consistency Levels

Offers 5 levels: Strong, Bounded Staleness, Session (Default), Consistent Prefix, Eventual. Trade off consistency for availability/latency.

## Best Practices (2025)

**Do**:

- **Use the NoSQL API**: It is the native API with the most features.
- **Use Hierarchical Partition Keys (2025)**: Supports up to 3 keys for better data distribution (TenantId -> UserId -> DeviceId).
- **Use Analytical Store (Synapse Link)**: Run heavy analytics (BI) on your operational data without impacting performance.

**Don't**:

- **Don't ignore RU consumption**: Monitor it. Queries without a partition key ("Cross-partition queries") are expensive.

## References

- [Azure Cosmos DB Documentation](https://learn.microsoft.com/en-us/azure/cosmos-db/)
