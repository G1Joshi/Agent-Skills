---
name: claude
description: Expert Anthropic Claude API assistance covering Claude 3.5 Sonnet / Haiku / Opus, tool use, prompt caching, and long-context processing. Use when integrating Anthropic models into LLM applications.
---

# Claude

Claude (by Anthropic) is OpenAI's main competitor. It is famous for its **large context window** (200k+), low hallucination rates, and "Artifacts" UI.

## When to Use

- **Advanced Reasoning & Complex Analysis**: Claude 3.5 Sonnet / Opus for intricate coding, mathematics, and logic.
- **Prompt Caching on Large Contexts**: Slashing latency and cost by up to 90% for repeated documentation, codebases, and books.
- **Reliable Tool & Function Calling**: Multi-turn agentic workflows invoking APIs and external tools with strict schema adherence.
- **Vision & Document Intelligence**: Transcribing, analyzing, and extracting data from charts, screenshots, and PDFs.

## Quick Start

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are an expert software architect.",
    messages=[
        {"role": "user", "content": "Explain event sourcing in 2 sentences."}
    ]
)

print(message.content[0].text)
```

## Core Concepts

### Tool Use (Function Calling) with Anthropic SDK

Exposing structured tools to Claude for agentic execution:

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "lookup_user_balance",
        "description": "Retrieve current account balance and active currency for a customer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "The unique customer UUID"},
            },
            "required": ["customer_id"],
        },
    }
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What is the balance for customer cust_98234?"}
    ]
)

# Inspect tool use request
for content in response.content:
    if content.type == "tool_use":
        print(f"Tool Requested: {content.name}")
        print(f"Arguments: {content.input}")
```

### Prompt Caching for Massive Contexts

Caching system prompts and large documentation blocks:

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": "You are an expert enterprise API assistant with deep knowledge of internal specs...",
        },
        {
            "type": "text",
            "text": "LARGE_API_DOCUMENTATION_BLOB_HERE...",
            "cache_control": {"type": "ephemeral"} # Cache this block
        }
    ],
    messages=[
        {"role": "user", "content": "How do I authenticate with the v2 billing endpoint?"}
    ]
)

print(f"Cached tokens read: {response.usage.cache_read_input_tokens}")
print(f"Cached tokens created: {response.usage.cache_creation_input_tokens}")
```

### Streaming Responses with Python Async Client

Consuming token streams in real-time:

```python
import asyncio
from anthropic import AsyncAnthropic

async def stream_completion():
    client = AsyncAnthropic()
    async with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Draft a refactoring plan for a monolith to microservices."}],
        model="claude-3-5-sonnet-20241022",
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

# asyncio.run(stream_completion())
```

## Common Patterns

### Structured Tool Calling with JSON Schema

**Problem**: Extracting structured parameters reliably from conversational LLM responses.

**Solution**:
Define tool definitions and parse returned tool_use blocks:

```python
tools = [{
    "name": "lookup_weather",
    "description": "Get current weather for a city",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        },
        "required": ["city"]
    }
}]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)

for block in response.content:
    if block.type == "tool_use":
        print(f"Tool called: {block.name}, Args: {block.input}")
```

## Best Practices

**Do**:

- Target `claude-3-5-sonnet` for the optimal balance of intelligence, coding proficiency, and speed.
- Apply `cache_control: {"type": "ephemeral"}` to static prompts exceeding 1,024 tokens to save 90% in costs.
- Provide clear, explicit descriptions and JSON schemas for all tools to minimize hallucinations.
- Use system prompts with clear persona guidelines, constraints, and XML tags (`<context>`, `<rules>`).

**Don't**:

- Concatenate user input into system instructions without sanitization; use XML tags to prevent injection.
- Leave temperature unconfigured; use `temperature=0` for structured extraction/coding, `0.7` for creative writing.
- Hardcode API keys; retrieve them from environment variables or secret vaults.

## Troubleshooting

| Error                                        | Cause                                                         | Solution                                                                          |
| :------------------------------------------- | :------------------------------------------------------------ | :-------------------------------------------------------------------------------- |
| `anthropic.RateLimitError (429)`             | Concurrency or token per minute (TPM) limit reached.          | Implement exponential backoff retry logic or use Prompt Caching to reduce tokens. |
| `Invalid request: max_tokens must be <= ...` | Requested output tokens exceed model maximum output capacity. | Set `max_tokens` within model limits (e.g. 4096 or 8192).                         |
| `anthropic.AuthenticationError (401)`        | Missing or invalid `ANTHROPIC_API_KEY`.                       | Export valid key: `export ANTHROPIC_API_KEY="sk-ant-..."`.                        |

## References

- [Anthropic Documentation](https://docs.anthropic.com/)
