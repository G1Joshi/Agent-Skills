---
name: arangodb
description: ArangoDB multi-model database with graphs. Use for multi-model workloads.
---

# ArangoDB

ArangoDB is a native multi-model database. It allows you to store data as Key/Values, JSON Documents, and Graphs, and query them all with a single language (AQL).

## When to Use

- **Polyglot Persistence**: When you need Documents AND Graph traversals but don't want to manage two databases (Mongo + Neo4j).
- **GraphRAG (2025)**: ArangoDB 3.12+ has native Vector Search combined with Graph capabilities for AI.
- **Microservices**: Reduces "Database Sprawl" by serving multiple data access patterns from one cluster.

## Quick Start (AQL)

```javascript
// AQL (ArangoDB Query Language) - SQL-like
FOR u IN users
  FILTER u.active == true
  FOR order IN OUTBOUND u orders
    RETURN { user: u.name, order: order.product }
```

## Core Concepts

### Multi-Model Core

One engine, multiple APIs. Storing a specific "Edge" collection turns your Documents into a Graph automatically.

### SmartGraphs

Sharding feature. Keeps related graph data (e.g., Users and their Orders) on the same server to avoid network hops during traversal (Enterprise).

### Foxx

A microservices framework running _inside_ the DB (V8 engine). Write endpoints in JS that run close to data.

## Best Practices (2025)

**Do**:

- **Use AQL**: It is powerful and standardizes Graph and Document queries.
- **Use Edge Collections**: Explicitly define edges to enable graph features.
- **Use Analyzer for Search**: ArangoSearch (integrated) offers full-text search capabilities like Elastic.

**Don't**:

- **Don't ignore sharding**: Graph traversals across network shards are slow. Plan your shard keys (SmartGraphs) carefully.

## References

- [ArangoDB Documentation](https://docs.arangodb.com/)
