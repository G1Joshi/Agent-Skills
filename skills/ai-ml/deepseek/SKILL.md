---
name: deepseek
description: DeepSeek AI models for coding. Use for code AI.
---

# DeepSeek

DeepSeek (from China) disrupted the market in late 2024/2025 by releasing **DeepSeek-V3** and **R1** (Reasoning) with performance matching Claude/GPT-4 at 1/10th the cost.

## When to Use

- **Cost Efficiency**: The API is incredibly cheap.
- **Reasoning**: **DeepSeek-R1** uses Chain-of-Thought reinforcement learning (like OpenAI o1) but is open weights.
- **Coding**: DeepSeek-Coder-V2 is a top-tier coding model.

## Core Concepts

### MLA (Multi-Head Latent Attention)

Architectural innovation that drastically reduces KV cache memory usage (allowing huge context).

### DeepSeek-R1

A reasoning model that outputs its "thought process" before the final answer.

## Best Practices (2025)

**Do**:

- **Use R1 for Math/Logic**: It rivals o1-preview in math benchmarks.
- **Local Distillations**: Run `DeepSeek-R1-Distill-Llama-70B` locally for private reasoning.

**Don't**:

- **Don't suppress thoughts**: When using R1, the "thought" trace is valuable for debugging the model's logic.

## References

- [DeepSeek GitHub](https://github.com/deepseek-ai)
