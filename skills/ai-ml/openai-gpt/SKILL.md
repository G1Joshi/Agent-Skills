---
name: openai-gpt
description: Expert OpenAI API assistance covering GPT-4o, GPT-4o-mini, o1/o3 reasoning models, structured outputs, and Function Calling. Use when building enterprise generative AI systems with OpenAI models.
---

# OpenAI GPT

OpenAI GPT models provide leading natural language generation, reasoning, and multimodal understanding via structured outputs, tool-calling APIs, and streaming inference.

## When to Use

- **State-of-the-Art Language & Reasoning Intelligence**: GPT-4o, GPT-4o mini, o1, and o3-mini for reasoning, coding, and comprehension.
- **Guaranteed Structured Outputs**: Utilizing JSON Schema and Pydantic to ensure 100% adherence to complex response models.
- **Autonomous Function Calling & Agentic Loops**: Executing multi-turn workflows invoking tools, APIs, and calculators.
- **Streaming & High-Throughput Production Workloads**: Real-time token streaming with async clients and batch APIs.

## Quick Start

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class EventDetails(BaseModel):
    name: str
    date: str
    participants: list[str]

# Strict structured outputs via Pydantic
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "Alice and Bob are meeting for quarterly planning on Nov 15th."}
    ],
    response_format=EventDetails,
)

event = completion.choices[0].message.parsed
print(event.name, event.date, event.participants)
```

## Core Concepts

### Guaranteed Structured Outputs with Pydantic

Parsing responses with 100% schema reliability:

```python
import os
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class StepByStepPlan(BaseModel):
    summary: str
    steps: list[str]
    estimated_hours: int = Field(description="Estimated implementation effort")
    requires_database_migration: bool

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a principal software architect."},
        {"role": "user", "content": "Outline the steps to migrate our user auth from session cookies to stateless JWTs."}
    ],
    response_format=StepByStepPlan,
)

plan: StepByStepPlan = completion.choices[0].message.parsed
print(f"Summary: {plan.summary} (Est. {plan.estimated_hours}h)")
for i, step in enumerate(plan.steps, 1):
    print(f"{i}. {step}")
```

### Multi-Tool Function Calling & Execution

Supplying tools and handling tool call requests:

```python
import json
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_database_metrics",
            "description": "Get current connection count and CPU utilization of a database instance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "instance_id": {"type": "string"},
                },
                "required": ["instance_id"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Check metrics for db-cluster-primary"}],
    tools=tools,
    tool_choice="auto"
)

tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    for tc in tool_calls:
        print(f"Tool to invoke: {tc.function.name} with args: {tc.function.arguments}")
```

### Streaming Responses with Async Client

Processing tokens in real-time for responsive UIs:

```python
import asyncio
from openai import AsyncOpenAI

async def stream_output():
    aclient = AsyncOpenAI()
    stream = await aclient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Explain zero-copy deserialization in Rust."}],
        stream=True
    )
    async for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)

# asyncio.run(stream_output())
```

## Common Patterns

### Function Calling with Parallel Tool Execution

**Problem**: Executing multiple external API lookups sequentially slows down assistant responses.

**Solution**:
Handle parallel tool call requests in a single round-trip:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the stock price of Apple and Google?"}],
    tools=stock_tools
)

tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    # Execute lookups concurrently in client application
    for tool_call in tool_calls:
        print(f"Executing: {tool_call.function.name}({tool_call.function.arguments})")
```

## Best Practices

**Do**:

- Use `client.beta.chat.completions.parse` with Pydantic models for guaranteed structured responses.
- Choose `gpt-4o-mini` for fast, cost-effective high-volume tasks and `gpt-4o` / `o3-mini` for heavy reasoning.
- Use `temperature=1.0` or default for reasoning models (o1/o3-mini), and `0.0` for structured extraction with GPT-4o.
- Leverage the OpenAI Batch API for non-real-time jobs to reduce costs by 50%.

**Don't**:

- Embed API keys in client-side code; proxy all OpenAI requests through an authenticated backend.
- Use standard completion parsing with regex when Structured Outputs guarantee exact JSON.
- Omit error handling for rate limits (`openai.RateLimitError`); implement exponential backoff.

## Troubleshooting

| Error                                             | Cause                                                           | Solution                                                                         |
| :------------------------------------------------ | :-------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `openai.RateLimitError (429)`                     | Requests per minute (RPM) or tokens per minute (TPM) quota hit. | Implement exponential backoff or use tiered model fallback (e.g. `gpt-4o-mini`). |
| `openai.BadRequestError: Context window exceeded` | Prompt tokens plus max_tokens exceed model context limit.       | Truncate conversation history or summarize previous messages.                    |
| `Refusal error in message`                        | Safety guardrails rejected the query.                           | Check `choice.message.refusal` and adjust prompt framing.                        |

## References

- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
