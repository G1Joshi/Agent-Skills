---
name: langchain
description: Expert LangChain and LangGraph assistance covering LCEL pipe syntax, tools, memory, retrievers, and cyclic multi-agent graphs. Use when orchestrating complex LLM chains and autonomous agents.
---

# LangChain

LangChain is the standard framework for chaining LLM components. In 2025, the focus shifted to **LangGraph** for building stateful, cyclic agents.

## When to Use

- **Agentic Workflows & Multi-Turn Problem Solving**: Building autonomous AI agents with LangGraph and tool calling.
- **Complex Retrieval-Augmented Generation (RAG)**: Orchestrating document chunking, embeddings, vector indexing, and reranking.
- **Declarative Chain Composition with LCEL**: Composing streaming, async, and batchable chains via LangChain Expression Language.
- **Enterprise LLM Observability**: Tracking token costs, latency, and step-by-step traces with LangSmith.

## Quick Start

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Declarative LCEL Pipe Syntax
prompt = ChatPromptTemplate.from_template("Summarize this concept in 3 bullet points: {topic}")
model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = prompt | model | parser
result = chain.invoke({"topic": "Distributed Consensus"})
print(result)
```

## Core Concepts

#LangChain Expression Language (LCEL) & Streaming

Declarative pipe-based chain execution with type inference and streaming:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert cloud architect. Answer concisely."),
    ("user", "Explain the difference between {topic_a} and {topic_b}.")
])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
parser = StrOutputParser()

# LCEL Pipeline: prompt | model | parser
chain = prompt | model | parser

# Stream output tokens in real-time
for chunk in chain.stream({"topic_a": "Kubernetes", "topic_b": "Docker Swarm"}):
    print(chunk, end="", flush=True)
```

#Retrieval-Augmented Generation (RAG) Pipeline

Querying vector stores and passing relevant context to LLMs:

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Mock vectorstore retriever
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(
    ["Antigravity IDE is an AI-first coding assistant.", "LangChain v0.3 introduces streamlined core abstractions."],
    embedding=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

rag_prompt = ChatPromptTemplate.from_template(
    "Answer the question based only on context: {context}\nQuestion: {question}"
)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)

response = rag_chain.invoke("What does LangChain v0.3 introduce?")
print(response)
```

#Agentic Workflows with Tool Calling

Binding custom Python functions as agent tools:

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def calculate_shipping(weight_kg: float, destination: str) -> float:
    '''Calculate the shipping fee in USD for a parcel weight and destination.'''
    rate = 12.5 if destination.upper() == "US" else 28.0
    return round(weight_kg * rate, 2)

tools = [calculate_shipping]
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

result = llm.invoke("What is the shipping cost for a 4.5kg package to the US?")
print("Tool Calls:", result.tool_calls)
```

## Common Patterns

### Stateful Agent Workflow with LangGraph

**Problem**: Legacy `AgentExecutor` loops lack checkpointing and cannot recover from partial errors.

**Solution**:
Use LangGraph state graphs with message nodes and conditional edges:

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def call_model(state: AgentState):
    # Process messages with LLM
    return {"messages": [model.invoke(state["messages"])]}

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app = workflow.compile()
```

## Best Practices (2026)

- **Do** target LangChain v0.3+ and construct pipelines using LCEL (`chain = prompt | model | parser`).
- **Do** use LangGraph for multi-turn, stateful, cyclical agent architectures rather than legacy AgentExecutor.
- **Do** configure LangSmith (`LANGCHAIN_TRACING_V2=true`) to monitor latency, cost, and tool calls in development and production.
- **Do** bind tools explicitly with Pydantic type annotations and docstrings for reliable tool call generation.
- **Don't** use deprecated v0.1 import paths (`langchain.chains` or `langchain.agents`); import from `langchain_core` and `langgraph`.
- **Don't** construct prompts using manual string formatting; use `ChatPromptTemplate` to properly handle roles and escapes.
- **Don't** pass unvalidated user input directly to vectorstore retriever filters.

## Troubleshooting

| Error                                    | Cause                                                            | Solution                                                                      |
| :--------------------------------------- | :--------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| `OutputParserException: Failed to parse` | LLM response did not adhere to expected JSON schema format.      | Add retry parser `OutputFixingParser` or use native model structured outputs. |
| `Recursion limit reached in LangGraph`   | Infinite loop in graph conditional edge routing.                 | Inspect routing logic and increase `recursion_limit` in config if expected.   |
| `RateLimitError in streaming chains`     | Too many simultaneous tokens per second requested across chains. | Implement async concurrency throttler or use batching with `.batch()`.        |

## References

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
