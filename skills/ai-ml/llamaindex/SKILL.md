---
name: llamaindex
description: LlamaIndex data framework for LLMs. Use for RAG applications.
---

# LlamaIndex

LlamaIndex (formerly GPT Index) connects LLMs to your data. 2025 introduces **Workflows**, an event-driven way to build complex RAG pipelines.

## When to Use

- **RAG (Retrieval Augmented Generation)**: Indexing PDFs, Docs, SQL to chat with them.
- **Structured Data**: Querying SQL/Pandas with natural language (`NLSQL`).
- **Agents**: Building research agents that browse the web and summarize.

## Core Concepts

### Workflows

Event-driven architecture for agents. Replace DAGs with event listeners (`@step`).

### Query Engine

High-level API (`index.as_query_engine()`) to ask questions.

### Data Loaders (LlamaHub)

Connectors for Notion, Slack, Discord, PDF, etc.

## Best Practices (2025)

**Do**:

- **Use Workflows**: They are harder to learn but easier to debug than monolithic engines.
- **Use Hybrid Search**: BM25 (Keyword) + Vector Search for best retrieval accuracy.
- **Use Rerankers**: Always rerank retrieved nodes (Cohere/BGE) before sending to LLM.

**Don't**:

- **Don't dump raw text**: Use "Node Parsers" to chunk data intelligently (Markdown, Semantic).

## References

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
