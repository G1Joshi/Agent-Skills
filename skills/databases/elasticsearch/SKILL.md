---
name: elasticsearch
description: Elasticsearch search and analytics engine with full-text search. Use for search and logging.
---

# Elasticsearch

Elasticsearch is a distributed search and analytics engine built on Apache Lucene. It is the heart of the ELK Stack (Elastic, Logstash, Kibana) and a leading Vector Database for AI.

## When to Use

- **Full-Text Search**: "Did you mean?" suggestions, fuzzy search, relevance scoring.
- **Log Analytics**: Storing terabytes of logs (Observability).
- **Vector Search (2025)**: Storing embeddings for Semantic Search / RAG.

## Quick Start

```bash
# REST API - Search for "bike"
GET /products/_search
{
  "query": {
    "match": {
      "description": "bike"
    }
  }
}
```

## Core Concepts

### Inverted Index

Maps words to documents. "Bike" -> [Doc1, Doc5]. Makes text search nearly instant.

### Shards & Replicas

- **Shard**: A slice of the index. Distributes data across nodes.
- **Replica**: Copy of a shard for High Availability.

### ES|QL (2024+)

Elasticsearch Query Language. A piped language (like SQL/Splunk) to simplify querying.
`FROM logs | WHERE status == 500 | LIMIT 10`

## Best Practices (2025)

**Do**:

- **Use `kNN` Search**: Native vector search support for AI applications.
- **Use ILM (Index Lifecycle Management)**: Move old logs to cheaper cold storage automatically.
- **Use Datastreams**: Optimized abstraction for time-series/logs (append-only).

**Don't**:

- **Don't use as primary source of truth**: It is eventually consistent and partition-tolerant, but relational DBs are safer for "money" data.
- **Don't oversight mapping explosion**: Too many unique fields map crash the cluster.

## References

- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
