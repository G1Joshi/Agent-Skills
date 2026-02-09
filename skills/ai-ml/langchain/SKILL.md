---
name: langchain
description: LangChain framework for building LLM applications with chains and agents. Use for AI orchestration.
---

# LangChain

Framework for building applications with large language models.

## When to Use

- Building chatbots and AI agents
- RAG (Retrieval-Augmented Generation)
- Multi-step LLM workflows
- Tool-using AI agents

## Quick Start

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke([HumanMessage(content="Hello!")])
print(response.content)
```

## Core Concepts

### Chains

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "Summarize this text in {language}: {text}"
)

chain = prompt | ChatOpenAI() | StrOutputParser()

result = chain.invoke({
    "language": "Spanish",
    "text": "Long English text..."
})
```

### RAG Pipeline

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the main topic?")
```

## Common Patterns

### Agents with Tools

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def search_database(query: str) -> str:
    """Search the database for information."""
    return db.search(query)

@tool
def calculate(expression: str) -> str:
    """Calculate a math expression."""
    return str(eval(expression))

tools = [search_database, calculate]
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({"input": "What is 25 * 4?"})
```

### Memory

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

history = ChatMessageHistory()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history,
    input_messages_key="input",
    history_messages_key="history"
)
```

## Best Practices

**Do**:

- Use LCEL for chain composition
- Implement proper error handling
- Add observability with LangSmith
- Cache expensive operations

**Don't**:

- Chain too many models together
- Skip input validation
- Ignore token limits
- Trust agent outputs blindly

## Troubleshooting

| Issue            | Cause                 | Solution                |
| ---------------- | --------------------- | ----------------------- |
| Slow chain       | Multiple LLM calls    | Parallelize or cache    |
| Context overflow | Too many documents    | Implement summarization |
| Agent loops      | Bad tool descriptions | Improve tool docstrings |

## References

- [LangChain Docs](https://python.langchain.com/)
- [LangSmith](https://smith.langchain.com/)
