---
name: huggingface
description: Expert Hugging Face assistance covering Transformers, datasets, pipelines, Hub model loading, and tokenizers. Use when downloading, fine-tuning, and deploying open-source machine learning models.
---

# Hugging Face

Hugging Face is the GitHub of AI. It hosts 1M+ models. 2025 sees massive growth in **Multimodal** models and **Robotics** (LeRobot).

## When to Use

- **Pretrained Model Discovery & Inference**: Utilizing thousands of open-source vision, NLP, and audio models via `transformers`.
- **Parameter-Efficient Fine-Tuning (PEFT)**: Fine-tuning LLMs with LoRA / QLoRA using `peft` and `bitsandbytes`.
- **Dataset Management & Streaming**: Accessing multi-gigabyte datasets without memory exhaustion via `datasets`.
- **Production Model Deployment**: Deploying containerized endpoints with Hugging Face Text Generation Inference (TGI).

## Quick Start

```python
from transformers import pipeline

# One-line inference with modern pre-trained models
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

result = classifier("This framework makes NLP development seamless and fast!")
print(result) # [{'label': 'POSITIVE', 'score': 0.9998}]
```

## Core Concepts

#Inference Pipeline with Transformers & PyTorch

Loading state-of-the-art transformer models with automatic tokenization:

```python
from transformers import pipeline
import torch

# Create accelerated text-classification pipeline
classifier = pipeline(
    task="text-classification",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    device=0 if torch.cuda.is_available() else -1
)

results = classifier([
    "This new AI development platform accelerates productivity significantly.",
    "The legacy system crashed repeatedly under moderate load."
])

for res in results:
    print(f"Label: {res['label']}, Score: {res['score']:.4f}")
```

#4-Bit Model Quantization with BitsAndBytes

Loading large LLMs on consumer hardware using 4-bit NormalFloat (NF4):

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model_id = "meta-llama/Llama-3.2-3B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)

inputs = tokenizer("Explain quantum computing in one sentence:", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

#Streaming Massive Datasets with Datasets Library

Iterating over terabyte-scale datasets without downloading all files upfront:

```python
from datasets import load_dataset

# Stream dataset lazily without full disk download
dataset = load_dataset('allenai/c4', 'en', split='train', streaming=True)

# Iterate through samples
for i, sample in enumerate(dataset.take(3)):
    print(f"Sample {i+1}: {sample['text'][:100]}...\n")
```

## Common Patterns

### Quantized Model Loading with BitsAndBytes (4-bit / 8-bit)

**Problem**: 7B-70B parameter models exceed single-GPU VRAM limits in FP16 precision.

**Solution**:
Load with 4-bit NF4 quantization using `BitsAndBytesConfig`:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

model_id = "meta-llama/Llama-3.2-3B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)
```

## Best Practices (2026)

- **Do** use `BitsAndBytesConfig` (`nf4`) or AWQ quantization to run open-weight LLMs with low memory consumption.
- **Do** set `device_map="auto"` when loading large models to distribute layers automatically across available GPUs and RAM.
- **Do** use `datasets.load_dataset(..., streaming=True)` for datasets that exceed local storage capacity.
- **Do** pass `torch_dtype=torch.bfloat16` when running inference on modern Ampere/Hopper GPU architectures.
- **Don't** load entire models onto CPU before moving to GPU; instantiate directly with `device_map`.
- **Don't** hardcode Hugging Face access tokens in code; authenticate via `huggingface-cli login` or `HF_TOKEN`.
- **Don't** run unquantized 70B+ parameter models on consumer hardware; use quantized GGUF, EXL2, or 4-bit NF4.

## Troubleshooting

| Error                                   | Cause                                                                        | Solution                                                                     |
| :-------------------------------------- | :--------------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `Gated repo error / 403 Forbidden`      | Accessing gated model (e.g. Llama/Mistral) without accepting license on Hub. | Accept license on HuggingFace and run `huggingface-cli login`.               |
| `CUDA Out of Memory in from_pretrained` | Model weights exceed GPU memory in FP32.                                     | Use `device_map="auto"`, `torch_dtype=torch.float16`, or 4-bit quantization. |
| `KeyError in tokenizer output`          | Mismatched tokenizer and model configurations.                               | Always load tokenizer and model from the identical `model_id`.               |

## References

- [Hugging Face Documentation](https://huggingface.co/docs)
