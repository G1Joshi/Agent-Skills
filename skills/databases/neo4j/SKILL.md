---
name: neo4j
description: Expert Neo4j graph database assistance covering Cypher query language, node/edge labeling, graph algorithms, and APOC. Use when modeling connected data, recommendation engines, fraud detection, or knowledge graphs.
---

# Neo4j

Neo4j is a native graph database. It stores data as nodes and relationships, not tables or documents. It is essential for "connected data" problems where relationships are as important as the data itself.

## When to Use

- **Complex Interconnected Relationships**: Social networks, recommendation engines, identity and access management (IAM), and supply chains.
- **Fraud Detection & Graph Analytics**: Detecting ring fraud, circular payment transfers, and money laundering paths in milliseconds.
- **Knowledge Graphs & Graph RAG**: Connecting enterprise knowledge bases to LLMs using Graph Retrieval-Augmented Generation.
- **Real-Time Pathfinding & Network Routing**: Calculating shortest paths, dependency trees, and network topology bottlenecks.

## Quick Start

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

### Labeled Property Graph (LPG) Model

Vertices are Nodes with Labels; connections are directed Relationships with Types; both store arbitrary key-value Properties:

```text
(:Person {name: "Alice"}) ──[:MANAGES {since: 2023}]──→ (:Person {name: "Bob"})
```

### Cypher Query Language Graph Matching

Declarative pattern matching queries relationships visually:

```cypher
// Discover friends of friends who like Graph Databases but Alice does not know yet
MATCH (alice:Person {name: 'Alice'})-[:FRIEND]->(f:Person)-[:FRIEND]->(fof:Person)
WHERE NOT (alice)-[:FRIEND]->(fof) AND alice <> fof
MATCH (fof)-[:INTERESTED_IN]->(:Topic {name: 'Neo4j'})
RETURN fof.name AS recommendation, count(f) AS mutualFriends
ORDER BY mutualFriends DESC
LIMIT 10;
```

### Graph Data Science (GDS) Algorithms

Executes graph algorithms (PageRank, Community Detection, Shortest Path) natively in memory:

```cypher
// Run PageRank on projected graph projection
CALL gds.pageRank.stream('fraudNetwork')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).accountNumber AS account, score
ORDER BY score DESC
LIMIT 20;
```

## Common Patterns

### Shortest Path and Relationship Scoring with Cypher

**Problem**: Finding optimal network paths or fraud rings across deeply interconnected entity networks.

**Solution**:
Use Cypher shortestPath matching:

```cypher
MATCH (origin:Account {id: 'acc_123'}), (destination:Account {id: 'acc_999'})
MATCH path = shortestPath((origin)-[:TRANSFERRED_TO*..6]->(destination))
RETURN path,
       length(path) as hops,
       reduce(total = 0, r in relationships(path) | total + r.amount) as totalTransferred;
```

## Best Practices

**Do**:

- Use Relationship Types Meaningfully: Name relationships with active verbs (`[:PURCHASED]`, `[:FOLLOWS]`) to eliminate ambiguity.
- Create Schema Constraints: Create uniqueness constraints (`CREATE CONSTRAINT FOR (u:User) REQUIRE u.id IS UNIQUE`) for index lookups.
- Profile Cypher Queries with `PROFILE`: Inspect execution operators, memory allocations, and DB hits to optimize graph navigations.
- Use Parameters in Cypher: Always pass query variables as `$params` to allow Neo4j to cache compiled execution plans.

**Don't**:

- Create "Supernodes" with millions of relationships: Supernodes cause massive memory overhead during traversals; refactor into intermediate nodes.
- Run unbounded relationship traversals: Never run `MATCH (a)-[*]->(b)`; set explicit depth bounds (`MATCH (a)-[*1..4]->(b)`).
- Use Neo4j for bulk tabular aggregations: Graph databases excel at traversals; use columnar databases for wide table analytics.

## Troubleshooting

| Error                                   | Cause                                                                     | Solution                                                                                      |
| :-------------------------------------- | :------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------- |
| `Neo.ClientError.Statement.SyntaxError` | Invalid Cypher syntax or outdated keyword.                                | Check query syntax and wrap keywords in backticks if used as property names.                  |
| `OutOfMemoryError: Java heap space`     | Unbounded Cartesian product (`MATCH (a), (b)`) loading millions of paths. | Enforce relationship directions and limit variable-length relationship depths (e.g. `*1..4`). |
| `ConstraintValidationFailed`            | Attempted to create node violating uniqueness constraint.                 | Use `MERGE` instead of `CREATE` when idempotent upsert behavior is required.                  |

## References

- [Neo4j Documentation](https://neo4j.com/docs/)
