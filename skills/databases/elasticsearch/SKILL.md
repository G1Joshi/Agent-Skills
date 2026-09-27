---
name: elasticsearch
description: Expert Elasticsearch assistance covering full-text search, inverted indexes, mappings, aggregations, and cluster lifecycle. Use when building search engines, analyzing logs (ELK), or implementing autocomplete search.
---

# Elasticsearch

Elasticsearch is a distributed search and analytics engine built on Apache Lucene. It is the heart of the ELK Stack (Elastic, Logstash, Kibana) and a leading Vector Database for AI.

## When to Use

- **Enterprise Full-Text Search**: Autocomplete, typo tolerance, synonyms, and relevancy ranking across millions of unstructured documents.
- **Log Analytics & SIEM (ELK Stack)**: Ingesting, indexing, and visualizing server logs, metrics, and security audit trails.
- **Dense Vector Semantic Search**: Storing machine-learning embeddings and performing hybrid semantic + lexical search.
- **Real-Time Analytical Aggregations**: Computing multi-level nested aggregations, histograms, and geolocation bounding boxes.

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

#Inverted Index & Tokenization Pipeline

Analyzers split text into tokens, normalize casing, apply stemming, and build inverted term-to-document indexes:

```
"The quick brown fox" ──Analyzer──→ ['quick', 'brown', 'fox']
Inverted Index:
  'brown' -> [Doc 1, Doc 4]
  'fox'   -> [Doc 1, Doc 2]
```

#Query DSL (Bool, Match, Multi-Match)

Constructs rich boolean relevancy queries:

```json
POST /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "multi_match": { "query": "wireless noise cancelling", "fields": ["title^3", "description"] } }
      ],
      "filter": [
        { "term": { "in_stock": true } },
        { "range": { "price": { "lte": 350.00 } } }
      ]
    }
  },
  "aggs": {
    "popular_brands": { "terms": { "field": "brand.keyword", "size": 5 } }
  }
}
```

#Index Lifecycle Management (ILM) & Hot-Warm-Cold Tiers

Automates moving aging indices across storage tiers to reduce infrastructure costs:

```
[ Hot Tier (Fast NVMe SSDs) ] ──30 Days──→ [ Warm Tier (Standard SSD) ] ──90 Days──→ [ Cold Tier / S3 Snapshot ]
```

## Common Patterns

### Multi-Match Search with Field Boosting and Fuzziness

**Problem**: Search queries fail to return relevant results due to minor typos or lack of ranking priority.

**Solution**:
Use multi_match queries with fuzziness and title field boosting (`^3`):

```json
POST /products/_search
{
  "query": {
    "multi_match": {
      "query": "wirless headphone",
      "fields": ["title^3", "brand^2", "description"],
      "fuzziness": "AUTO",
      "prefix_length": 2
    }
  },
  "aggs": {
    "categories": {
      "terms": { "field": "category.keyword" }
    }
  }
}
```

## Best Practices (2026)

**Do**:

- **Use `keyword` Type for Exact Matching**: Use `keyword` fields for filtering, sorting, and aggregations; use `text` for full-text search.
- **Place Filters Inside the `filter` Context**: Filter clauses do not calculate BM25 relevancy scores and are cached automatically.
- **Implement Index Lifecycle Management (ILM)**: Rollover indices based on size (50GB) and age rather than arbitrary calendar dates.
- **Tune `refresh_interval` During Bulk Ingestion**: Increase `refresh_interval` to `30s` or `-1` when streaming bulk data to boost throughput.

**Don't**:

- **Don't create too many small shards**: Keep shard sizes between 20GB and 50GB; excessive small shards exhaust cluster heap memory.
- **Don't use `wildcard` queries with leading asterisks (`*keyword`)**: Leading wildcards force full inverted index scans.
- **Don't use Elasticsearch as a primary system-of-record database**: Replicate data from primary relational databases (PostgreSQL/MySQL).

## Troubleshooting

| Error                                                 | Cause                                                                          | Solution                                                                     |
| :---------------------------------------------------- | :----------------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `circuit_breaking_exception: [parent] Data too large` | JVM heap exhaustion during large aggregation or unbounded wildcard query.      | Increase cluster heap, reduce aggregation bucket sizes, or scale data nodes. |
| `Cluster status is RED`                               | Primary shards unassigned due to node failure or storage exhaustion.           | Check shard allocation explain API: `GET /_cluster/allocation/explain`.      |
| `Fielddata is disabled on text fields`                | Attempting to aggregate or sort on a `text` field without `keyword` sub-field. | Update query to target `fieldname.keyword`.                                  |

## References

- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
