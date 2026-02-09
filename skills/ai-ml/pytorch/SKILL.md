---
name: pytorch
description: PyTorch deep learning framework with tensors, autograd, and neural networks. Use for ML research.
---

# PyTorch

Deep learning framework for research and production.

## When to Use

- Deep learning research
- Custom neural network architectures
- GPU-accelerated training
- Model prototyping

## Quick Start

```python
import torch
import torch.nn as nn

# Simple model
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)

x = torch.randn(32, 784)  # Batch of 32
output = model(x)
```

## Core Concepts

### Tensors & Autograd

```python
import torch

# Create tensors
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = torch.randn(3, 4, device='cuda')  # GPU tensor

# Operations
z = x @ torch.randn(3, 4)  # Matrix multiply
z = torch.softmax(z, dim=-1)

# Autograd
loss = z.sum()
loss.backward()
print(x.grad)  # Gradients
```

### Custom Modules

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model)
        )
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        attn_out, _ = self.attention(x, x, x)
        x = self.norm1(x + attn_out)
        x = self.norm2(x + self.ff(x))
        return x
```

## Common Patterns

### Training Loop

```python
model = MyModel().to('cuda')
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss()

for epoch in range(epochs):
    model.train()
    for batch in dataloader:
        inputs, targets = batch
        inputs, targets = inputs.to('cuda'), targets.to('cuda')

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

# Save model
torch.save(model.state_dict(), 'model.pt')
```

## Best Practices

**Do**:

- Use `torch.no_grad()` for inference
- Move data to GPU efficiently
- Use mixed precision training
- Profile with torch.profiler

**Don't**:

- Forget to call `model.eval()` for inference
- Skip gradient zeroing
- Create tensors in loops
- Ignore CUDA memory management

## Troubleshooting

| Issue         | Cause              | Solution               |
| ------------- | ------------------ | ---------------------- |
| CUDA OOM      | Memory exhausted   | Reduce batch size      |
| NaN loss      | Gradient explosion | Lower learning rate    |
| Slow training | CPU bottleneck     | Use DataLoader workers |

## References

- [PyTorch Documentation](https://pytorch.org/docs/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
