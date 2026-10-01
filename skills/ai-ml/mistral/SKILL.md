---
name: mistral
description: Expert Mistral AI assistance covering Mistral Large/Small, Codestral, Pixtral, function calling, and local deployment via Ollama/vLLM. Use when deploying high-efficiency open foundation models.
---

# Mistral

Mistral AI focuses on **efficiency** and **coding** capabilities. Their "Mixture of Experts" (MoE) architecture (Mixtral) changed the game.

## When to Use

- **High-Performance European & Multilingual LLMs**: Mistral Large, Mistral NeMo, and Codestral for code intelligence and multilingual reasoning.
- **Efficient Function Calling & JSON Enforcement**: Executing structured agentic workflows with low latency.
- **On-Premise & Open-Weights Self-Hosting**: Deploying open weights (Mistral-7B, Mixtral 8x7B/8x22B) with vLLM or Ollama.
- **High-Speed Code Completion**: Integrating Codestral into IDEs with Fill-in-the-Middle (FIM) capabilities.

## Quick Start

```python
from mistralai import Mistral

client = Mistral(api_key="your-mistral-api-key")

response = client.chat.complete(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": "Explain Mixture of Experts (MoE) in two sentences."}]
)

print(response.choices[0].message.content)
```

## Core Concepts

### Chat Completion with Mistral Python Client

Calling Mistral Large with structured configuration:

```python
import os
from mistralai import Mistral

client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

response = client.chat.complete(
    model="mistral-large-latest",
    messages=[
        {"role": "system", "content": "You are an expert security engineer."},
        {"role": "user", "content": "Analyze the security implications of using JWT in local storage."}
    ],
    temperature=0.2,
    max_tokens=1024
)

print(response.choices[0].message.content)
```

### Tool Use & Function Calling

Binding tools to Mistral for multi-turn agent execution:

```python
import json
from mistralai import Mistral

client = Mistral()

tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_dns_records",
            "description": "Query DNS records for a given domain name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "The domain name, e.g. example.com"},
                    "record_type": {"type": "string", "enum": ["A", "AAAA", "MX", "TXT"]}
                },
                "required": ["domain", "record_type"]
            }
        }
    }
]

response = client.chat.complete(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": "Check the MX records for github.com"}],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        print(f"Tool Requested: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
```

### Fill-in-the-Middle (FIM) with Codestral

Completing code between prefix and suffix markers:

```python
from mistralai import Mistral

client = Mistral()

prefix = '''def calculate_tax(income: float) -> float:
    # Validate input
    if income < 0:
        raise ValueError('Income cannot be negative')
'''
suffix = '''    return tax_amount
'''

response = client.fim.complete(
    model="codestral-latest",
    prompt=prefix,
    suffix=suffix,
    temperature=0.1
)

print("Infilled Code:\n", response.choices[0].message.content)
```

## Common Patterns

### Code Generation with Codestral FIM (Fill-in-the-Middle)

**Problem**: Generating code completions that seamlessly fit between existing prefix and suffix code snippets.

**Solution**:
Use Codestral's native FIM endpoint:

```python
response = client.fim.complete(
    model="codestral-latest",
    prompt="def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n",
    suffix="\n    return -1"
)

print(response.choices[0].message.content)
```

## Best Practices

**Do**:

- Target `codestral-latest` for coding tasks and Fill-in-the-Middle (FIM) in-editor completions.
- Use `response_format={"type": "json_object"}` when machine-readable JSON is strictly required.
- Set `temperature=0.1` for code generation and factual extraction tasks.
- Leverage Mixtral Mixture-of-Experts (MoE) architectures for high throughput with reduced active parameter counts.

**Don't**:

- Provide unstructured tool descriptions; define strict JSON schemas with clear parameter types.
- Hardcode `MISTRAL_API_KEY` in scripts; load from environment variables.
- Use large general models when specialized compact models like `ministral-8b` or `mistral-nemo` suffice.

## Troubleshooting

| Error                               | Cause                                              | Solution                                                        |
| :---------------------------------- | :------------------------------------------------- | :-------------------------------------------------------------- |
| `MistralAPIError: 401 Unauthorized` | Invalid or unset API key.                          | Pass valid key via `api_key` or export `MISTRAL_API_KEY`.       |
| `429 Too Many Requests`             | Monthly quota or concurrent request limit reached. | Monitor usage in Mistral Console or self-host weights via vLLM. |
| `Model not found error`             | Deprecated model tag used in API call.             | Use active aliases: `mistral-large-latest`, `codestral-latest`. |

## References

- [Mistral AI Documentation](https://docs.mistral.ai/)
