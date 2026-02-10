---
name: openai-gpt
description: OpenAI GPT models API for chat, completion, and embeddings. Use for AI integration.
---

# OpenAI GPT

GPT (Generative Pre-trained Transformer) is the foundation of the modern AI revolution. In 2025, **GPT-5** offers agentic capabilities, deep reasoning, and native multimodal integration.

## When to Use

- **General Purpose**: It is the baseline for all AI tasks.
- **Complex Reasoning**: GPT-5 excels at multi-step logic and planning.
- **Vision/Voice**: Native "Omni" capabilities (GPT-4o/5) process audio and video with <300ms latency.

## Core Concepts

### Models

- **GPT-5**: The frontier model. Slow but smartest.
- **GPT-4o**: "Omni". Fast, multimodal, cheaper.
- **o1 / o3**: "Reasoning" models that "think" before answering (Chain of Thought).

### Assistants API

Stateful API for building agents. Manages threads, retrieval (RAG), and code interpreter.

### Structured Outputs

Guarantees JSON schema compliance for API responses.

## Best Practices (2025)

**Do**:

- **Use Structured Outputs**: Always define a Zod/JSON schema for production apps.
- **Use `o3-mini` for Code**: It is cheaper and often better at coding than GPT-4o.
- **Batch Requests**: Use the Batch API for 50% discount on non-urgent tasks.

**Don't**:

- **Don't use GPT-3.5**: It is obsolete. Use GPT-4o-mini for cheap tasks.

## References

- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
