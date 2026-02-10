---
name: pytorch
description: PyTorch deep learning framework with dynamic graphs. Use for neural networks.
---

# PyTorch

PyTorch is the dominant framework for research and production AI. v2.5 (2025) solidifies **`torch.compile`** and introduces **FlexAttention**.

## When to Use

- **Research**: 99% of new papers (Arxiv) use PyTorch.
- **Production**: Recommended for almost all new DL projects.
- **Performance**: `torch.compile` provides C++ level speed with Python ease.

## Core Concepts

### `torch.compile`

Just-in-Time (JIT) compilation of your model.
`model = torch.compile(model)` -> 2x speedup.

### Dynamic Graphs (Eager Mode)

Debug line-by-line (`print(tensor.shape)` works).

### Fabric / Lightning

High-level wrappers to simplify training loops and multi-GPU setup.

## Best Practices (2025)

**Do**:

- **Use `torch.compile`**: It is now stable and essential for H100 performance.
- **Use `FlashAttention`**: Use the scaled dot product attention (SDPA) kernel for Transformers.
- **Use PyTorch 2.x**: PyTorch 1.x is legacy.

**Don't**:

- **Don't code `.cuda()` manually**: Use `.to(device)` or Fabric to handle device placement.

## References

- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
