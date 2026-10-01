---
name: llama
description: Expert Meta Llama (Llama 3 / 3.2 / 3.3) assistance covering fine-tuning (LoRA/QLoRA), vLLM deployment, and prompt templates. Use when deploying open-weight foundation models locally or in the cloud.
---

# Llama

Meta Llama is the foundation standard for open-weight language models, providing dense and Mixture-of-Experts architectures optimized for fine-tuning, quantization, and local deployment.

## When to Use

- **Local & On-Premise LLM Deployment**: Running Meta Llama 3.1/3.2/3.3 locally without data leaving the private perimeter.
- **High-Efficiency Quantized Inference**: Utilizing GGUF (via llama.cpp) and AWQ/GPTQ on consumer and enterprise GPUs.
- **Fine-Tuning on Custom Domain Data**: Training LoRA/QLoRA adapters with Unsloth or Axolotl.
- **Embedded & Mobile Edge AI**: Running lightweight Llama 3.2 1B and 3B models directly on laptops and mobile devices.

## Quick Start

```bash
# Serve Llama 3 with vLLM for high-throughput OpenAI-compatible inference
vLLM serve meta-llama/Llama-3.2-3B-Instruct \
  --port 8000 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90
```

## Core Concepts

### Local GGUF Inference with llama-cpp-python

Fast, low-latency CPU/GPU inference with zero external network calls:

```python
from llama_cpp import Llama

# Load GGUF model with GPU layer offloading
llm = Llama(
    model_path="./models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
    n_gpu_layers=-1, # Offload all layers to GPU (Metal / CUDA)
    n_ctx=8192,      # Context window
    verbose=False
)

# Chat completion with standard Llama 3 instruction prompt format
response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a concise Unix systems administrator."},
        {"role": "user", "content": "How do I find processes holding open deleted files?"}
    ],
    temperature=0.2,
    max_tokens=256
)

print(response["choices"][0]["message"]["content"])
```

### Serving Llama via vLLM with OpenAI API Compatibility

Deploying Llama 3.1 as an enterprise production endpoint:

```bash
# Launch vLLM server with tensor parallelism and 16k context window
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --dtype bfloat16 \
  --max-model-len 16384 \
  --port 8000
```

### Parameter-Efficient Fine-Tuning with LoRA & PEFT

Adapting Llama to domain specific instructions:

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", device_map="auto")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

peft_model = get_peft_model(model, lora_config)
peft_model.print_trainable_parameters()
```

## Common Patterns

### Official Llama 3 Chat Template Formatting

**Problem**: Incorrect header formatting degrades instruction following and triggers repetition loops.

**Solution**:
Apply tokenizer chat template:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
messages = [
    {"role": "system", "content": "You are a concise programming assistant."},
    {"role": "user", "content": "Write a quicksort function in Python."}
]

prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
# Formats into: <|begin_of_text|><|start_header_id|>system<|end_header_id|>...
```

## Best Practices

**Do**:

- Use GGUF 4-bit (`Q4_K_M`) or 5-bit (`Q5_K_M`) quantization for optimal balance of speed and perplexity.
- Offload all layers (`n_gpu_layers=-1`) to GPU memory whenever VRAM capacity allows.
- Use Meta Llama 3 prompt template formatting (`<|start_header_id|>...<|end_header_id|>`) for accurate instruction following.
- Pin model versions and test against specific release tags (e.g. `Llama-3.1-8B-Instruct`).

**Don't**:

- Run unquantized 16-bit models on consumer GPUs if memory capacity causes swap thrashing.
- Forget to configure appropriate context lengths (`n_ctx`); exceeding default context degrades performance.
- Use chat models without supplying system prompts specifying constraints and formatting rules.

## Troubleshooting

| Error                                        | Cause                                                    | Solution                                                                 |
| :------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------- |
| `403 Client Error: Cannot access repository` | Missing access approval for Llama model on Hugging Face. | Request model access on Meta/HuggingFace and provide Hugging Face token. |
| `Model generating endless repetition tokens` | Missing stop tokens in inference generation config.      | Configure explicit stop tokens: `<\|eot_id\|>` and `<\|end_of_text\|>`.  |
| `CUDA out of memory during vLLM serve`       | KV cache memory allocation exceeds available VRAM.       | Lower `--gpu-memory-utilization` or reduce `--max-model-len`.            |

## References

- [Llama Website](https://www.llama.com/)
