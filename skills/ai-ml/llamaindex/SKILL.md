---
name: llamaindex
description: Expert LlamaIndex assistance covering RAG (Retrieval-Augmented Generation), vector store indexes, document chunking, and query engines. Use when connecting LLMs to private enterprise data and document stores.
---

# LlamaIndex

LlamaIndex is a data framework connecting custom data sources to large language models, featuring event-driven Workflows, hybrid retrieval strategies, and production RAG pipelines.

## When to Use

- **Enterprise Document Ingestion & RAG**: Parsing PDFs, Notion docs, Word files, and databases into optimized index structures.
- **Complex Query Routing & Multi-Document Agents**: Routing queries between vector search, SQL databases, and summary indexes.
- **Hierarchical & Parent-Child Indexing**: Preserving granular sentence chunks with links to full parent document contexts.
- **Knowledge Graphs & Hybrid Search**: Combining dense semantic embeddings with sparse BM25 keyword search.

## Quick Start

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents from directory and build searchable in-memory index
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Create query engine and ask questions
query_engine = index.as_query_engine()
response = query_engine.query("What are the key terms in the agreement?")
print(str(response))
```

## Core Concepts

### Ingesting Documents & Building VectorStoreIndex

Building vector index and querying with conversational engine:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure global model settings
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.1)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 512
Settings.chunk_overlap = 64

# Load all documents from directory
documents = SimpleDirectoryReader("./data/knowledge_base").load_data()

# Build vector store index
index = VectorStoreIndex.from_documents(documents)

# Create query engine with response synthesis
query_engine = index.as_query_engine(similarity_top_k=3)
response = query_engine.query("What are the deployment prerequisites for the billing service?")

print("Answer:", str(response))
print("\nSource Nodes:")
for node in response.source_nodes:
    print(f"- [Score: {node.score:.3f}] {node.node.get_text()[:120]}...")
```

### Hybrid Search with BM25 & Dense Reranking

Combining keyword and semantic matching:

```python
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.postprocessor import SentenceTransformerRerank

# Hybrid retriever combining dense vector and sparse BM25
dense_retriever = index.as_retriever(similarity_top_k=5)
bm25_retriever = BM25Retriever.from_defaults(nodes=index.docstore.docs.values(), similarity_top_k=5)

fusion_retriever = QueryFusionRetriever(
    [dense_retriever, bm25_retriever],
    similarity_top_k=5,
    num_queries=1 # Don't generate extra queries
)

# Cross-encoder reranker for precision scoring
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3
)

query_engine = index.as_query_engine(
    retriever=fusion_retriever,
    node_postprocessors=[reranker]
)
```

### Multi-Document Router Agent

Intelligently selecting the right index based on query semantics:

```python
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

# Wrap separate index query engines as tools
tools = [
    QueryEngineTool(
        query_engine=annual_report_engine,
        metadata=ToolMetadata(name="financial_report", description="Contains 2025-2026 financial metrics and revenue figures.")
    ),
    QueryEngineTool(
        query_engine=engineering_engine,
        metadata=ToolMetadata(name="engineering_docs", description="Contains software architecture and API specifications.")
    )
]

router = RouterQueryEngine(selector=LLMSingleSelector.from_defaults(), query_engine_tools=tools)
result = router.query("What was the Q3 gross margin?")
print(result)
```

## Common Patterns

### Hybrid Search with Re-Ranking for Production RAG

**Problem**: Pure vector semantic search misses exact keyword IDs and technical terminology.

**Solution**:
Combine vector and BM25 text search with cross-encoder re-ranking:

```python
from llama_index.core.postprocessor import SentenceTransformerRerank

# Retrieve top 20 candidates, re-rank down to top 3 most relevant nodes
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2",
    top_n=3
)

query_engine = index.as_query_engine(
    similarity_top_k=20,
    node_postprocessors=[reranker]
)
response = query_engine.query("What is error code E-1049?")
```

## Best Practices

**Do**:

- Target LlamaIndex v0.10+ / v0.11+ using `Settings.llm` and `Settings.embed_model` global singletons.
- Use `SentenceSplitter` with explicit `chunk_size` and `chunk_overlap` tailored to your document structure.
- Apply a cross-encoder reranker (`SentenceTransformerRerank`) to improve precision of retrieved context.
- Inspect `response.source_nodes` to audit and debug retrieval relevance.

**Don't**:

- Ingest raw documents without chunking; huge chunks dilute embedding vector specificity.
- Use standard vector search alone when precise keyword lookups (SKUs, IDs) are required; use hybrid search.
- Create separate storage contexts repeatedly without persisting them to disk or a vector DB.

## Troubleshooting

| Error                                                       | Cause                                                                        | Solution                                                                   |
| :---------------------------------------------------------- | :--------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `RateLimitError during index creation`                      | Embedding model hitting OpenAI TPM limit when embedding large document sets. | Use batch embedding or set `embed_model = "local:BAAI/bge-small-en-v1.5"`. |
| `EmptyResponse: No relevant context found`                  | Query threshold too strict or documents not parsed properly.                 | Inspect retrieved source nodes: `response.source_nodes`.                   |
| `ImportError: cannot import name ... from llama_index.core` | Version mismatch between v0.9 legacy and v0.10+ modular packages.            | Update imports to `llama_index.core` and install `llama-index-core`.       |

## References

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
