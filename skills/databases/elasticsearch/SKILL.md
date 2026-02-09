---
name: elasticsearch
description: Elasticsearch search and analytics engine with full-text search, aggregations, and logging. Use for search and logging.
---

# Elasticsearch

Distributed search and analytics engine for full-text search and logging.

## When to Use

- Full-text search implementation
- Log aggregation and analysis
- Real-time analytics
- Geospatial search

## Quick Start

```javascript
// Index a document
await client.index({
  index: "products",
  id: "1",
  body: {
    name: "Laptop",
    description: "High-performance laptop",
    price: 999.99,
    category: "electronics",
  },
});

// Search
const { hits } = await client.search({
  index: "products",
  body: {
    query: { match: { description: "laptop" } },
  },
});
```

## Core Concepts

### Mappings

```javascript
await client.indices.create({
  index: "products",
  body: {
    mappings: {
      properties: {
        name: { type: "text", analyzer: "standard" },
        description: { type: "text" },
        price: { type: "float" },
        category: { type: "keyword" },
        tags: { type: "keyword" },
        created_at: { type: "date" },
      },
    },
  },
});
```

### Search Queries

```javascript
// Boolean query
const query = {
  bool: {
    must: [{ match: { description: "laptop" } }],
    filter: [
      { term: { category: "electronics" } },
      { range: { price: { lte: 1000 } } },
    ],
    should: [{ term: { featured: true } }],
  },
};

// Full-text with highlighting
const result = await client.search({
  index: "products",
  body: {
    query: { match: { description: "laptop computer" } },
    highlight: { fields: { description: {} } },
    sort: [{ price: "asc" }],
    from: 0,
    size: 10,
  },
});
```

## Common Patterns

### Aggregations

```javascript
const result = await client.search({
  index: "orders",
  body: {
    size: 0,
    aggs: {
      sales_by_category: {
        terms: { field: "category" },
        aggs: {
          total_revenue: { sum: { field: "amount" } },
          avg_order: { avg: { field: "amount" } },
        },
      },
      monthly_sales: {
        date_histogram: {
          field: "created_at",
          calendar_interval: "month",
        },
      },
    },
  },
});
```

## Best Practices

**Do**:

- Use keyword type for exact matches
- Set appropriate shard count
- Use bulk operations for indexing
- Implement proper mappings upfront

**Don't**:

- Use text type for filtering
- Create too many shards
- Skip index lifecycle management
- Store large documents

## Troubleshooting

| Issue            | Cause                | Solution                    |
| ---------------- | -------------------- | --------------------------- |
| Slow search      | Missing optimization | Check mappings, add filters |
| Mapping conflict | Type mismatch        | Use dynamic templates       |
| Cluster red      | Unassigned shards    | Check disk space, replicas  |

## References

- [Elasticsearch Documentation](https://www.elastic.co/guide/)
- [Elasticsearch Best Practices](https://www.elastic.co/blog/)
