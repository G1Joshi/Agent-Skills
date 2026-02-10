---
name: perplexity
description: Perplexity AI search and research. Use for AI search.
---

# Perplexity

Perplexity is an AI search engine. For developers, the **Sonar API** provides grounded, cited answers for building search-enabled apps.

## When to Use

- **Real-time Info**: "What is the stock price of Apple?" (LLMs can't answer this without tools).
- **Research Apps**: Building an app that needs to cite sources.
- **Citations**: You need reliability and links to original data.

## Core Concepts

### Sonar API

API access to Perplexity's online models (`llama-3-sonar-large-32k-online`).

### Citations

API returns a list of citations used to generate the answer.

### Pro Search

Multi-step reasoning search (Googles multiple times to answer complex queries).

## Best Practices (2025)

**Do**:

- **Use for Grounding**: If your chatbot needs current events, route those queries to Perplexity.
- **Use Search Options**: Filter by domain (e.g., search only `reddit.com` or `stackoverflow.com`).

**Don't**:

- **Don't use for creative writing**: It is optimized for facts, not fiction.

## References

- [Perplexity API](https://docs.perplexity.ai/)
