---
name: deepseek
description: Expert DeepSeek AI assistance covering DeepSeek-R1 reasoning models, DeepSeek-V3, API integration, and local quantization. Use when building cost-effective reasoning agents, code generation, or math/logic solvers.
---

# DeepSeek

DeepSeek provides state-of-the-art open foundation models, including DeepSeek-V3 (Mixture-of-Experts) and DeepSeek-R1 for chain-of-thought mathematical reasoning and agentic workflows.

## When to Use

- **High-Performance Open-Weights Reasoning & Coding**: DeepSeek-R1 and DeepSeek-V3 for mathematical reasoning, agentic logic, and code generation.
- **Self-Hosted & Private LLM Deployments**: Running enterprise reasoning models locally using vLLM, SGLang, or Ollama.
- **Cost-Efficient API Scaling**: Accessing state-of-the-art reasoning at a fraction of proprietary API costs.
- **Chain-of-Thought (CoT) Verification**: Parsing detailed `<think>` reasoning traces for auditability and verification.

## Quick Start

```python
from openai import OpenAI

# DeepSeek exposes an OpenAI-compatible API endpoint
client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-reasoner", # DeepSeek-R1
    messages=[
        {"role": "user", "content": "Solve: How many r's are in strawberry? Think step by step."}
    ]
)

# Reasoning output is provided in reasoning_content
print("Thinking Process:\n", response.choices[0].message.reasoning_content)
print("Final Answer:\n", response.choices[0].message.content)
```

## Core Concepts

### Consuming DeepSeek API with OpenAI SDK Compatibility

Querying DeepSeek models with reasoning token handling:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-reasoner", # DeepSeek-R1 reasoning model
    messages=[
        {"role": "system", "content": "You are a quantitative systems engineer."},
        {"role": "user", "content": "Design an optimal concurrent lock-free queue algorithm in C++."}
    ],
    max_tokens=4096,
    temperature=0.6,
)

# DeepSeek-R1 returns reasoning content separately
reasoning = getattr(response.choices[0].message, 'reasoning_content', None)
final_answer = response.choices[0].message.content

if reasoning:
    print(f"=== Thinking Process ({len(reasoning)} chars) ===")
    print(reasoning[:500] + "...")

print("\n=== Final Response ===")
print(final_answer)
```

### High-Throughput Self-Hosting with vLLM

Deploying DeepSeek-V3 / R1 on multi-GPU nodes with PagedAttention:

```bash
# Launch vLLM server with tensor parallelism across 8 H100 GPUs
vllm serve deepseek-ai/DeepSeek-R1 \
  --tensor-parallel-size 8 \
  --max-model-len 32768 \
  --trust-remote-code \
  --gpu-memory-utilization 0.95 \
  --port 8000
```

### Streaming Reasoning Tokens

Streaming live thinking tokens to the client interface:

```python
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[{"role": "user", "content": "Solve this riddle: ..."}],
    stream=True
)

for chunk in response:
    delta = chunk.choices[0].delta
    if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
        print(f"[Thinking]: {delta.reasoning_content}", end="", flush=True)
    elif delta.content:
        print(delta.content, end="", flush=True)
```

## Common Patterns

### DeepSeek-R1 Reasoning Extraction with Fallback

**Problem**: Handling reasoning steps separately from final response text in client applications.

**Solution**:
Access `reasoning_content` with safe attribute fallback:

```python
msg = response.choices[0].message
thought_process = getattr(msg, 'reasoning_content', None)
final_text = msg.content

if thought_process:
    print(f"Step-by-step logic: {thought_process}")
print(f"Output: {final_text}")
```

## Best Practices

**Do**:

- Separate reasoning output (`reasoning_content`) from final output (`content`) when rendering responses to users.
- Use `temperature=0.6` (recommended default for DeepSeek-R1) to balance logical rigor and exploration.
- Use FP8 or AWQ 4-bit quantizations when self-hosting on hardware with limited VRAM.
- Implement retries with exponential backoff on API endpoints during peak network congestion.

**Don't**:

- Strip `<think>` tags prematurely if debugging algorithmic reasoning failures.
- Provide overly verbose system prompts for DeepSeek-R1; it is trained to reason autonomously.
- Use `temperature=0` with DeepSeek reasoning models; it may cause repetitive reasoning loops.

## Troubleshooting

| Error                                             | Cause                                                              | Solution                                                      |
| :------------------------------------------------ | :----------------------------------------------------------------- | :------------------------------------------------------------ |
| `401 Unauthorized: Invalid API Key`               | Missing or incorrect DeepSeek API key.                             | Verify key at `platform.deepseek.com` and pass via `api_key`. |
| `Base URL not recognized`                         | Client connecting to standard OpenAI endpoint instead of DeepSeek. | Set `base_url="https://api.deepseek.com"`.                    |
| `Timeout / 504 Gateway error during R1 reasoning` | Complex reasoning query exceeding standard client HTTP timeout.    | Increase timeout: `OpenAI(timeout=120.0, ...)`.               |

## References

- [DeepSeek GitHub](https://github.com/deepseek-ai)
