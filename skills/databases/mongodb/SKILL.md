---
name: mongodb
description: MongoDB document database with aggregation pipeline, indexing, schema design, and Atlas. Use for document storage and NoSQL.
---

# MongoDB

Document database development with aggregation pipelines and schema design.

## When to Use

- Working with document-oriented data
- Flexible schema requirements
- Real-time analytics with aggregation
- Geospatial queries

## Quick Start

```javascript
// Insert document
db.users.insertOne({
  email: "john@example.com",
  name: "John Doe",
  profile: { age: 30, city: "NYC" },
  tags: ["developer", "nodejs"],
  createdAt: new Date(),
});

// Query with projection
db.users.find({ "profile.city": "NYC" }, { name: 1, email: 1 });
```

## Core Concepts

### Aggregation Pipeline

```javascript
db.orders.aggregate([
  {
    $match: { status: "completed", createdAt: { $gte: ISODate("2024-01-01") } },
  },
  {
    $group: {
      _id: "$customerId",
      totalAmount: { $sum: "$amount" },
      orderCount: { $count: {} },
      avgOrder: { $avg: "$amount" },
    },
  },
  {
    $lookup: {
      from: "customers",
      localField: "_id",
      foreignField: "_id",
      as: "customer",
    },
  },
  { $unwind: "$customer" },
  {
    $project: {
      customerName: "$customer.name",
      totalAmount: 1,
      orderCount: 1,
    },
  },
  { $sort: { totalAmount: -1 } },
  { $limit: 10 },
]);
```

### Indexing

```javascript
// Single field index
db.users.createIndex({ email: 1 }, { unique: true });

// Compound index
db.orders.createIndex({ customerId: 1, createdAt: -1 });

// Text index for search
db.products.createIndex({ name: "text", description: "text" });

// TTL index for auto-expiry
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 });
```

## Common Patterns

### Schema Design

```javascript
// Embedding for 1:few
{
  _id: ObjectId("..."),
  name: "John",
  addresses: [
    { type: "home", city: "NYC" },
    { type: "work", city: "Boston" }
  ]
}

// References for 1:many
{
  _id: ObjectId("..."),
  name: "John",
  orderIds: [ObjectId("..."), ObjectId("...")]
}

// Bucket pattern for time-series
{
  sensorId: "temp-001",
  date: ISODate("2024-01-15"),
  readings: [
    { time: ISODate("..."), value: 22.5 },
    { time: ISODate("..."), value: 23.1 }
  ]
}
```

## Best Practices

**Do**:

- Design schema based on query patterns
- Use compound indexes for common queries
- Enable retryable writes
- Use Atlas for managed hosting

**Don't**:

- Create unbounded arrays
- Use $where with user input
- Over-normalize (denormalize for reads)
- Ignore write concern for important data

## Troubleshooting

| Issue              | Cause             | Solution                  |
| ------------------ | ----------------- | ------------------------- |
| Slow query         | Missing index     | Use explain(), add index  |
| Document too large | Exceeds 16MB      | Use GridFS or restructure |
| High memory usage  | Large working set | Scale up or shard         |

## References

- [MongoDB Documentation](https://docs.mongodb.com/)
- [MongoDB University](https://university.mongodb.com/)
