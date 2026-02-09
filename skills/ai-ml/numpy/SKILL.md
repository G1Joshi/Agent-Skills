---
name: numpy
description: NumPy numerical computing with arrays and mathematical operations. Use for scientific computing.
---

# NumPy

Numerical computing library for Python with array operations.

## When to Use

- Numerical computations
- Array/matrix operations
- Scientific computing
- ML data preprocessing

## Quick Start

```python
import numpy as np

# Create arrays
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2], [3, 4]])
zeros = np.zeros((3, 3))
ones = np.ones((2, 4))
```

## Core Concepts

### Array Creation

```python
# Various creation methods
arr = np.arange(0, 10, 2)        # [0, 2, 4, 6, 8]
arr = np.linspace(0, 1, 5)       # 5 values between 0-1
arr = np.random.randn(3, 4)      # Random normal
arr = np.eye(3)                   # Identity matrix

# Reshaping
arr = np.arange(12).reshape(3, 4)
arr.T                             # Transpose
arr.flatten()                     # 1D array
```

### Operations

```python
# Vectorized operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

a + b          # [5, 7, 9]
a * b          # [4, 10, 18]
a @ b          # Dot product: 32
np.sqrt(a)     # Element-wise sqrt
np.exp(a)      # Element-wise exp

# Broadcasting
matrix = np.array([[1, 2], [3, 4]])
matrix + 10    # Add 10 to all elements
matrix * [1, 2]  # Multiply each row
```

## Common Patterns

### Indexing & Slicing

```python
arr = np.arange(10)

arr[2:5]           # [2, 3, 4]
arr[::2]           # [0, 2, 4, 6, 8]
arr[-3:]           # [7, 8, 9]

# Boolean indexing
arr[arr > 5]       # [6, 7, 8, 9]

# 2D indexing
matrix = np.arange(12).reshape(3, 4)
matrix[0, :]       # First row
matrix[:, 0]       # First column
matrix[1:, 2:]     # Submatrix
```

### Aggregations

```python
arr = np.random.randn(100, 4)

arr.sum()
arr.mean(axis=0)    # Column means
arr.std(axis=1)     # Row std devs
arr.max()
np.percentile(arr, 95)
np.argmax(arr)      # Index of max
```

## Best Practices

**Do**:

- Use vectorized operations
- Preallocate arrays for loops
- Use appropriate dtypes
- Leverage broadcasting

**Don't**:

- Use Python loops on arrays
- Create many small arrays
- Ignore memory layout
- Copy when view suffices

## Troubleshooting

| Issue              | Cause                | Solution             |
| ------------------ | -------------------- | -------------------- |
| Broadcasting error | Shape mismatch       | Check array shapes   |
| Memory error       | Large array          | Use memmap or chunks |
| Precision issues   | Float representation | Use float64          |

## References

- [NumPy Documentation](https://numpy.org/doc/)
- [NumPy User Guide](https://numpy.org/doc/stable/user/)
