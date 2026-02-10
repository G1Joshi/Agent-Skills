---
name: langchain
description: LangChain LLM application framework with chains and agents. Use for LLM orchestration.
---

# LangChain

LangChain is the standard framework for chaining LLM components. In 2025, the focus shifted to **LangGraph** for building stateful, cyclic agents.

## When to Use

- **Orchestration**: Chaining "Prompt -> LLM -> Parser".
- **Agents**: Using LangGraph to build agents that can loop, retry, and keep state.
- **Integrations**: 1000+ connectors for vector DBs, APIs, and tools.

## Core Concepts

### LangGraph

The successor to `AgentExecutor`. A graph-based way to define agent flows with cycles (loops).

### LCEL (LangChain Expression Language)

The declarative pipe syntax: `prompt | llm | output_parser`.

### LangSmith

Observability platform to trace and debug complex chains.

## Best Practices (2025)

**Do**:

- **Use LangGraph**: For any non-trivial agent. `AgentExecutor` is legacy.
- **Use LCEL**: It enables streaming and async out of the box.
- **Trace everything**: Connect to LangSmith to see _why_ your agent failed.

**Don't**:

- **Don't over-abstract**: If a simple Python function works, don't wrap it in a Chain.

## References

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
