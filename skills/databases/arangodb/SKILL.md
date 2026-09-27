---
name: arangodb
description: Expert ArangoDB multi-model database assistance covering AQL, document collections, graphs, and Foxx microservices. Use when querying graph relationships, joining document stores, or designing multi-model schemas.
---

# ArangoDB

ArangoDB is a native multi-model database. It allows you to store data as Key/Values, JSON Documents, and Graphs, and query them all with a single language (AQL).

## When to Use

- **Multi-Model Data Architectures**: Unifying document (JSON), graph, and key-value models into a single query engine with ACID transactions.
- **Complex Graph Traversals**: Executing high-performance depth-first and breadth-first traversals with edge attributes in AQL.
- **Unified Knowledge Graphs**: Storing entity metadata as rich documents while querying interconnected relationships as graphs.
- **Search & Full-Text Integration**: Leveraging ArangoSearch for integrated full-text indexing, BM25 scoring, and geo-spatial queries.

## Quick Start

```javascript
// AQL (ArangoDB Query Language) - SQL-like
FOR u IN users
  FILTER u.active == true
  FOR order IN OUTBOUND u orders
    RETURN { user: u.name, order: order.product }
```

## Core Concepts

#Multi-Model Document & Edge Collections

Documents store unstructured JSON entities; Edge collections define directed connections between documents using `_from` and `_to` attributes:

```json
// Vertex Document (users/alice)
{ "_key": "alice", "name": "Alice Mercer", "role": "Lead Architect" }

// Edge Document (knows/edge_1)
{ "_from": "users/alice", "_to": "users/bob", "relationship": "mentor", "since": 2024 }
```

#ArangoDB Query Language (AQL) Graph Traversal

Traverses interconnected relationship graphs up to N hops:

```aql
// 1 to 3 hops outward traversal from Alice
FOR v, e, p IN 1..3 OUTBOUND 'users/alice' GRAPH 'socialGraph'
  FILTER e.relationship == 'mentor'
  RETURN {
    colleague: v.name,
    distance: LENGTH(p.edges),
    path: p.vertices[*].name
  }
```

#Distributed Cluster Sharding (OneShard & SmartGraphs)

Ensures interconnected graph vertices and edges are colocated on identical physical DB servers to eliminate network hop penalties:

```javascript
// Creates a SmartGraph partitioned by customer tenant ID
const graph = db._createSmartGraph(
  "tenantSocialGraph",
  [{ collection: "members", from: ["users"], to: ["users"] }],
  { smartGraphAttribute: "tenantId" },
);
```

## Common Patterns

### Graph Traversal with AQL

**Problem**: Querying deeply nested social or hierarchy connections in relational stores requires slow multi-table recursive joins.

**Solution**:
Traverse nodes and edges declaratively with AQL:

```aql
FOR v, e, p IN 1..3 OUTBOUND 'users/alice' GRAPH 'social_graph'
  FILTER v.status == 'active'
  RETURN {
    friend: v.name,
    distance: LENGTH(p.edges),
    path: p.vertices[*].name
  }
```

## Best Practices (2026)

**Do**:

- **Leverage SmartGraphs for Multi-Tenant Clusters**: Colocate graph subtrees on single cluster nodes using `smartGraphAttribute` to eliminate network hop latencies.
- **Use ArangoSearch Views**: Replace separate external Elasticsearch clusters by indexing collections directly with ArangoSearch.
- **Filter Early in Graph Traversals**: Use `PRUNE` and inline `FILTER` conditions to stop traversals down dead-end relationship paths.
- **Bind Parameters in AQL**: Always pass variables as `@param` to prevent AQL injection and maximize query compilation cache reuse.

**Don't**:

- **Don't perform unbounded graph traversals**: Never run `1..99` traversals without a `PRUNE` condition or depth limits.
- **Don't use Edge collections without indexes**: ArangoDB automatically indexes `_from` and `_to`; avoid overriding them with inefficient manual indexes.
- **Don't mix cross-tenant data without SmartGraph keys**: Sharding graphs randomly across nodes causes severe distributed RPC overhead.

## Troubleshooting

| Error                              | Cause                                                    | Solution                                                                             |
| :--------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `[1200] conflict`                  | Optimistic locking collision on document update.         | Retry update using current document `_rev` or use `overwriteMode: 'replace'`.        |
| `[1501] collection not found`      | Attempted query against non-existent collection or typo. | Verify collection names and ensure creation migrations have executed.                |
| `Out of memory in graph traversal` | Unbounded traversal depths on large dense graphs.        | Specify explicit min..max depths and add prune/filter conditions early in traversal. |

## References

- [ArangoDB Documentation](https://docs.arangodb.com/)
