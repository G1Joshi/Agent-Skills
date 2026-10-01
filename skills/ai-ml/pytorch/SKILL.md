---
name: pytorch
description: Expert PyTorch deep learning assistance covering dynamic tensors, autograd, torch.compile, distributed training (DDP), and GPU acceleration. Use when training neural networks and deploying AI research.
---

# PyTorch

PyTorch is the foundational deep learning framework for research and production, featuring dynamic computational graphs, `torch.compile` graph optimization, and distributed GPU training.

## When to Use

- **State-of-the-Art Deep Learning Research & Production**: Training vision, NLP, audio, and generative AI models.
- **Model Compilation with torch.compile()**: Accelerating model inference and training via TorchDynamo and Triton kernels.
- **Distributed Training (DDP / FSDP)**: Scaling models across multi-GPU and multi-node clusters.
- **Hardware Acceleration**: Training and executing on NVIDIA CUDA, Apple Silicon MPS, and AMD ROCm.

## Quick Start

```python
import torch
import torch.nn as nn

# Define simple neural network
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(20, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = MLP().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
```

## Core Concepts

### Modern Neural Network Module with torch.compile

Defining architectures and compiling with TorchDynamo:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class TransformerClassifier(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int, num_classes: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=4, dim_feedforward=256, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(self.encoder_layer, num_layers=2)
        self.fc = nn.Linear(embed_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        embedded = self.embedding(x)
        encoded = self.transformer(embedded)
        pooled = encoded.mean(dim=1) # Global average pooling
        return self.fc(pooled)

device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
model = TransformerClassifier(vocab_size=10000, embed_dim=128, num_classes=5).to(device)

# PyTorch 2.x JIT compilation for Triton / GPU optimization
if torch.cuda.is_available():
    compiled_model = torch.compile(model)
else:
    compiled_model = model
```

### Automatic Mixed Precision (AMP) Training Loop

Accelerating training and halving VRAM usage with bfloat16:

```python
import torch

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
criterion = nn.CrossEntropyLoss()

# Standard training step with AMP
model.train()
dummy_inputs = torch.randint(0, 10000, (32, 64), device=device)
dummy_targets = torch.randint(0, 5, (32,), device=device)

optimizer.zero_grad(set_to_none=True)

# Autocast enables bfloat16/float16 execution on tensor cores
with torch.amp.autocast(device_type=device.type, dtype=torch.bfloat16):
    outputs = compiled_model(dummy_inputs)
    loss = criterion(outputs, dummy_targets)

loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()

print(f"Batch Loss: {loss.item():.4f}")
```

### Saving & Loading Safe Weights with Safetensors

Exporting model weights without arbitrary Python pickle execution:

```python
from safetensors.torch import save_model, load_model

# Save model safely
save_model(model, "transformer_weights.safetensors")

# Load in production
new_model = TransformerClassifier(vocab_size=10000, embed_dim=128, num_classes=5)
load_model(new_model, "transformer_weights.safetensors")
```

## Common Patterns

### Complete Modern Training Loop with torch.compile

**Problem**: Slow training iterations due to Python kernel dispatch overhead on modern GPUs (H100/A100).

**Solution**:
JIT-compile model graph with PyTorch 2.x `torch.compile`:

```python
# Compile model for kernel fusion and 2x speedup
compiled_model = torch.compile(model)

for epoch in range(10):
    compiled_model.train()
    for batch_x, batch_y in dataloader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad(set_to_none=True) # Faster than zero_grad()
        outputs = compiled_model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
```

## Best Practices

**Do**:

- Target PyTorch 2.4+ and apply `torch.compile(model)` to production models for instant speedups.
- Use `optimizer.zero_grad(set_to_none=True)` instead of `zero_grad()` to reduce memory bandwidth overhead.
- Train with Automatic Mixed Precision (`torch.amp.autocast(..., dtype=torch.bfloat16)`) on modern GPUs.
- Save models using `safetensors` instead of Python `pickle` (`torch.save`) to prevent arbitrary code execution vulnerabilities.

**Don't**:

- Move tensors between CPU and GPU inside training loops; prefetch batches on the target device.
- Track computational graphs during inference; wrap evaluation in `with torch.inference_mode():`.
- Use Python lists for tensor aggregations; accumulate loss with scalar float values (`total_loss += loss.item()`).

## Troubleshooting

| Error                                                   | Cause                                                       | Solution                                                                                         |
| :------------------------------------------------------ | :---------------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| `RuntimeError: CUDA out of memory`                      | Model weights and batch activation tensors exceed GPU VRAM. | Lower batch size, enable mixed precision `torch.cuda.amp.autocast()`, or gradient checkpointing. |
| `Expected all tensors to be on the same device`         | Some tensors on CPU and others on CUDA.                     | Call `.to(device)` on all inputs and model parameters.                                           |
| `RuntimeError: size mismatch, m1: [a x b], m2: [c x d]` | Matrix multiplication dimension mismatch in `nn.Linear`.    | Ensure `m1` column count `b` equals `m2` row count `c`.                                          |

## References

- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
