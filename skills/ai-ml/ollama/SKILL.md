---
name: ollama
description: Expert Ollama assistance covering local LLM execution, Modelfile customization, REST API integration, and model quantizations. Use when running open models (Llama, Mistral, DeepSeek) locally on CPU/GPU.
---

# Ollama

Ollama bundles model weights, configurations, and runtime dependencies into a streamlined CLI and local server for running open-source LLMs locally with native tool-calling.

## When to Use

- **Local LLM Execution**: Running Llama 3, DeepSeek-R1, Mistral, and Qwen locally with a single CLI command.
- **Zero-Cloud Air-Gapped Deployments**: Privacy-critical enterprise environments requiring 100% on-premise execution.
- **Custom Modelfile Configuration**: Tailoring system prompts, temperature, context length, and stop sequences.
- **REST & OpenAI-Compatible API**: Seamless drop-in replacement for OpenAI SDKs in local test and dev pipelines.

## Quick Start

```bash
# Run open-weight models locally with zero setup
ollama run llama3.2:3b "Write a Python script to compute Fibonacci numbers."
```

```python
# Query local Ollama instance via Python SDK
import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": "Explain zero-trust security."}]
)
print(response['message']['content'])
```

## Core Concepts

### Local Inference with the Python Ollama SDK

Querying local models with streaming and structured JSON output:

```python
import ollama

# Basic chat completion
response = ollama.chat(
    model='llama3.1:8b',
    messages=[
        {'role': 'system', 'content': 'You are an expert DevOps engineer.'},
        {'role': 'user', 'content': 'Write a minimal production Dockerfile for a Go API.'}
    ],
    options={
        'temperature': 0.2,
        'num_ctx': 8192
    }
)

print(response['message']['content'])
```

### Structured Output with Pydantic & JSON Schema

Enforcing typed JSON responses from local models:

```python
from pydantic import BaseModel
import ollama

class ThreatAnalysis(BaseModel):
    threat_level: str
    vulnerabilities: list[str]
    mitigation: str

response = ollama.chat(
    model='llama3.1:8b',
    messages=[
        {'role': 'user', 'content': 'Analyze the security of an unauthenticated Redis instance exposed to 0.0.0.0.'}
    ],
    format=ThreatAnalysis.model_json_schema(),
    options={'temperature': 0.1}
)

analysis = ThreatAnalysis.model_validate_json(response['message']['content'])
print("Threat Level:", analysis.threat_level)
print("Mitigation:", analysis.mitigation)
```

### Custom Modelfile Authoring

Creating tailored local model artifacts:

```dockerfile
# Modelfile
FROM llama3.1:8b

PARAMETER temperature 0.3
PARAMETER num_ctx 16384
PARAMETER stop "<|eot_id|>"

SYSTEM '''
You are Antigravity Code Guardian. You analyze git diffs for security vulnerabilities,
performance regressions, and design pattern anti-patterns. Respond in concise markdown tables.
'''
```

```bash
# Build and register the custom model
ollama create code-guardian -f ./Modelfile
ollama run code-guardian "Review this diff..."
```

## Common Patterns

### Custom System Instructions and Temperature via Modelfile

**Problem**: Re-sending identical system prompts and temperature settings with every API request.

**Solution**:
Create a custom Modelfile:

```dockerfile
FROM llama3.2:3b

# Set model temperature
PARAMETER temperature 0.2

# Set system instruction
SYSTEM """
You are a senior DevOps engineer. Always provide answers as copy-pasteable bash or Terraform snippets.
"""
```

Build model: `ollama create devops-assistant -f ./Modelfile`

## Best Practices

**Do**:

- Set `OLLAMA_NUM_PARALLEL` and `OLLAMA_MAX_LOADED_MODELS` to handle concurrent local requests efficiently.
- Use `format=Schema.model_json_schema()` for reliable structured outputs without regex parsing.
- Offload models to Apple Silicon Metal or NVIDIA CUDA automatically with proper driver setups.
- Utilize `ollama pull` and model tags to test quantized variants (`:q4_K_M`, `:q8_0`).

**Don't**:

- Expose Ollama port (11434) to the public internet without an authenticating reverse proxy (Nginx, Caddy).
- Assume default context is unlimited; explicitly set `num_ctx: 16384` or higher in options if needed.
- Run heavy 70B models on systems with less than 64GB unified memory/RAM.

## Troubleshooting

| Error                                    | Cause                                                  | Solution                                                                      |
| :--------------------------------------- | :----------------------------------------------------- | :---------------------------------------------------------------------------- |
| `Error: could not connect to ollama app` | Ollama daemon not running in background.               | Start daemon with `ollama serve`.                                             |
| `CUDA out of memory on local GPU`        | Model size exceeds discrete GPU VRAM.                  | Pull a smaller quantization (e.g. `q4_0`) or specify CPU layers in Modelfile. |
| `pull model failed: unexpected EOF`      | Network timeout during multi-gigabyte weight download. | Re-run `ollama pull <model>` to resume download from checkpoint.              |

## References

- [Ollama Website](https://ollama.com/)
