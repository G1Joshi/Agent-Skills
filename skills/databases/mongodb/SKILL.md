---
name: mongodb
description: MongoDB document database with aggregation pipeline and Atlas. Use for document storage.
---

# MongoDB

MongoDB is a document database. It stores data in JSON-like documents (BSON). It is the most popular NoSQL database, known for flexibility and scalability.

## When to Use

- **Rapid Prototyping**: Schema-less design allows iterating fast without migrations.
- **Content Management**: Storing diverse assets with varying metadata.
- **Catalogs**: Product catalogs where each product has different attributes (size, color, wattage).

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

### Documents (BSON)

Data is stored in "documents" (JSON objects) inside "collections" (Tables).
`{ "_id": 1, "name": "Apple", "price": 10 }`

### Embedded Data vs References

- **Embed**: Store related data inside the document for fast reads. (e.g., Comments inside a Post).
- **Reference**: Store the ID and look it up (`$lookup`) for many-to-many relationships.

### Sharding

MongoDB scales horizontally by splitting data across multiple servers (shards) based on a "shard key".

## Best Practices (2025)

**Do**:

- **Use Version 8.0+**: For performance gains in time-series and queryable encryption.
- **Index Early**: "Compass" (GUI) or "Atlas Performance Advisor" will tell you when you miss indexes.
- **Limit Array Growth**: Don't use unbounded arrays (e.g., logging every login in the user document).

**Don't**:

- **Don't join everything**: MongoDB supports `$lookup` (JOINS), but overuse kills performance. Embed data if accessed together.
- **Don't ignore Document Size**: Max document size is 16MB.

## References

- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [MongoDB University](https://learn.mongodb.com/)
