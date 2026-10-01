---
name: mongodb
description: Expert MongoDB document database assistance covering aggregation pipelines, compound indexes, replica sets, and sharding. Use when designing flexible JSON schemas, querying geospatial data, or scaling document stores.
---

# MongoDB

MongoDB is a document database. It stores data in JSON-like documents (BSON). It is the most popular NoSQL database, known for flexibility and scalability.

## When to Use

- **Flexible JSON Document Storage**: Modeling evolving, nested domain entities with polymorphic schemas in BSON.
- **High-Velocity Operational Data Stores**: Content management, e-commerce product catalogs, and user personalization platforms.
- **Rich Aggregation Pipelines**: Transforming, joining ($lookup), grouping, and projecting analytical data streams in real time.
- **Global Sharding & Geospatial Indexing**: Scaling collections horizontally across shards and executing 2dsphere geo queries.

## Quick Start

```javascript
// Using Mongoose (Node.js)
const kittySchema = new mongoose.Schema({
  name: String,
});
const Kitten = mongoose.model("Kitten", kittySchema);

const silence = new Kitten({ name: "Silence" });
await silence.save();
```

## Core Concepts

### BSON Documents & Schema Flexibility

Data is stored as binary JSON (BSON), supporting native dates, 64-bit integers, decimals, and geospatial points:

```javascript
// MongoDB Document in collections/orders
{
  "_id": ObjectId("66f6ab42d1e1c3a628a58a98"),
  "orderNumber": "ORD-2026-901",
  "customer": { "id": "cust_12", "email": "alex@example.com" },
  "items": [
    { "sku": "WIDGET-01", "qty": 2, "price": 49.99 }
  ],
  "shippingAddress": {
    "type": "Point",
    "coordinates": [-73.9851, 40.7488] // 2dsphere GeoJSON
  },
  "status": "PROCESSING",
  "createdAt": ISODate("2026-09-27T10:00:00Z")
}
```

### Powerful Multi-Stage Aggregation Framework

Transforms and aggregates documents through sequential pipeline stages:

```javascript
db.orders.aggregate([
  {
    $match: { status: "COMPLETED", createdAt: { $gte: ISODate("2026-01-01") } },
  },
  { $unwind: "$items" },
  {
    $group: {
      _id: "$items.sku",
      totalRevenue: { $sum: { $multiply: ["$items.qty", "$items.price"] } },
      unitsSold: { $sum: "$items.qty" },
    },
  },
  { $sort: { totalRevenue: -1 } },
  { $limit: 5 },
]);
```

### Replica Sets & Automated Failover

Ensures high availability through 3-node primary-secondary elections:

```text
[ Primary (Read/Write) ] ──Oplog Replication (Async)──→ [ Secondary (Read Replicas) ]
                                                              │
                                                              ▼
                                                     [ Secondary (Voter) ]
```

## Common Patterns

### Aggregation Pipeline with Lookup and Facets

**Problem**: Normalizing and joining related documents across collections efficiently in a single query.

**Solution**:
Use `$lookup` with `$project` and pagination `$facet`:

```javascript
db.orders.aggregate([
  {
    $match: { status: "DELIVERED", createdAt: { $gte: ISODate("2025-01-01") } },
  },
  {
    $lookup: {
      from: "users",
      localField: "userId",
      foreignField: "_id",
      as: "customer",
    },
  },
  { $unwind: "$customer" },
  {
    $project: {
      orderId: "$_id",
      totalAmount: 1,
      customerName: "$customer.name",
      customerEmail: "$customer.email",
    },
  },
  { $sort: { totalAmount: -1 } },
  { $limit: 20 },
]);
```

## Best Practices

**Do**:

- Design for Data Access Patterns: Embed data that is read together frequently; reference data when unbounded growth is expected.
- Follow the ESR Rule for Indexes: Order compound indexes by **Equality** first, **Sort** second, and **Range** last.
- Enable JSON Schema Validation: Enforce required fields and types at the collection level via `$jsonSchema`.
- Use Bulk Operations: Batch multiple write operations using `bulkWrite()` to minimize network roundtrips.

**Don't**:

- Create unbounded arrays inside documents: Unbounded arrays degrade performance and can hit the 16MB document size limit.
- Use `$lookup` excessively: MongoDB is not a relational database; heavy multi-collection joins destroy throughput.
- Perform unindexed queries: Run `.explain("executionStats")` to verify queries utilize `IXSCAN` rather than `COLLSCAN`.

## Troubleshooting

| Error                                                            | Cause                                                                        | Solution                                                                                      |
| :--------------------------------------------------------------- | :--------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `Executor error during find command: OperationExceededTimeLimit` | Query performing full collection scan (`COLLSCAN`) without supporting index. | Run `explain('executionStats')` and add compound index matching filter and sort keys.         |
| `WriteConflict error`                                            | Concurrent updates modifying same document concurrently in WiredTiger.       | Implement retry logic in application layer or batch modifications.                            |
| `BSONObj size exceeds maximum allowed size (16MB)`               | Single document exceeded 16MB limit due to unbounded arrays.                 | Refactor schema: move unbounded child arrays into separate collection with parent references. |

## References

- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [MongoDB University](https://learn.mongodb.com/)
