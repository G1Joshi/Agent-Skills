---
name: neo4j
description: Neo4j graph database with Cypher query language. Use for graph-based data.
---

# Neo4j

Neo4j is a native graph database. It stores data as nodes and relationships, not tables or documents. It is essential for "connected data" problems where relationships are as important as the data itself.

## When to Use

- **Knowledge Graphs**: Connecting silos of data (Users, Docs, Concepts).
- **Fraud Detection**: Finding "Rings" of users sharing IDs/Devices.
- **Recommendation Engines**: "People who bought X also bought Y" (Collaborative Filtering).
- **GraphRAG (2025)**: Enhancing LLM context by traversing a knowledge graph instead of just vector similarity.

## Quick Start (Cypher)

```cypher
-- Create nodes and relationships
CREATE (alice:Person {name: 'Alice'})
CREATE (bob:Person {name: 'Bob'})
CREATE (alice)-[:KNOWS {since: 2024}]->(bob);

-- Query friends of friends
MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(friend)-[:KNOWS]->(fof)
RETURN fof.name;
```

## Core Concepts

### Cypher

The SQL of Graphs. It uses ASCII-art patterns `(node)-[RELATIONSHIP]->(node)`.

### Index-Free Adjacency

In Neo4j, every node physically points to the next node. "Joins" are pre-computed pointers. Traversing 1 million relationships is O(1) per step, not O(Log N) like B-Trees.

### Graph Data Science (GDS)

Library for algorithms like PageRank, Louvain (Community Detection), and Path Finding.

## Best Practices (2025)

**Do**:

- **Use GraphRAG**: Combine Vector Search (Semantic) with Graph Traversal (Structural) for better AI answers.
- **Model Relationships Richly**: Put properties on relationships (e.g., `[:REVIEWED {rating: 5, date: ...}]`).
- **Use Labels**: Always label nodes (`:Person`) to optimize scans.

**Don't**:

- **Don't create Supernodes**: A node with 1 Million edges (e.g., `(Justin Bieber)-[:FOLLOWED_BY]->(...)`) hurts traversal performance.
- **Don't use it for simple lookups**: If you just need `ByKey` or `Range`, use a K-V store.

## References

- [Neo4j Documentation](https://neo4j.com/docs/)
