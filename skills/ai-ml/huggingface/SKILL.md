---
name: huggingface
description: Hugging Face Transformers for NLP, computer vision, and model hub. Use for pretrained models.
---

# Hugging Face

Hub for pretrained models and the Transformers library.

## When to Use

- NLP tasks (classification, NER, QA)
- Using pretrained models
- Fine-tuning transformers
- Model hosting and inference

## Quick Start

```python
from transformers import pipeline

# Zero-shot classification
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
result = classifier("This movie is fantastic!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.99}]
```

## Core Concepts

### Pipelines

```python
from transformers import pipeline

# Text generation
generator = pipeline("text-generation", model="gpt2")
output = generator("Once upon a time", max_length=50)

# Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(long_text, max_length=130, min_length=30)

# Question answering
qa = pipeline("question-answering")
answer = qa(question="What is Python?", context="Python is a programming language...")
```

### Model Loading

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model(**inputs)
```

## Common Patterns

### Fine-tuning with Trainer

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    evaluation_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

### Inference API

```python
import requests

API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

response = requests.post(API_URL, headers=headers, json={"inputs": "Hello"})
```

## Best Practices

**Do**:

- Use Auto classes for flexibility
- Cache models locally
- Use `device_map="auto"` for large models
- Quantize for deployment

**Don't**:

- Load full model if using pipeline
- Ignore tokenizer special tokens
- Skip input validation
- Fine-tune without freezing layers

## Troubleshooting

| Issue          | Cause           | Solution                          |
| -------------- | --------------- | --------------------------------- |
| OOM error      | Model too large | Use quantization or smaller model |
| Slow inference | No GPU          | Enable CUDA or use quantized      |
| Token mismatch | Wrong tokenizer | Use matching tokenizer            |

## References

- [Hugging Face Docs](https://huggingface.co/docs)
- [Model Hub](https://huggingface.co/models)
