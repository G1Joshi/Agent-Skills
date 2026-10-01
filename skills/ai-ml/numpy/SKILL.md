---
name: numpy
description: Expert NumPy numerical computing assistance covering ndarrays, broadcasting, linear algebra, vectorization, and memory views. Use when writing ultra-fast scientific calculations and array operations in Python.
---

# NumPy

NumPy is the foundational library for scientific computing in Python, providing multidimensional array objects, vectorized mathematical operations, and unified C/C++ API bindings.

## When to Use

- **High-Performance Numerical Computation**: Vectorized array arithmetic and multi-dimensional tensor manipulation.
- **Scientific Computing & Linear Algebra**: Matrix decompositions (SVD, QR, Cholesky), eigenvalues, and inversions via `np.linalg`.
- **Foundational Data Layer for AI/ML**: Serving as the memory buffer standard for PyTorch, TensorFlow, OpenCV, and Scikit-learn.
- **NumPy 2.0+ Modern Standard**: Utilizing improved typing, standardized C-API, and optimized array constructors.

## Quick Start

```python
import numpy as np

# Vectorized matrix operations with broadcasting
a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
b = np.array([10, 20, 30])

# Broadcast addition across rows
c = a + b
print("Result shape:", c.shape)
print("Row-wise sum:", np.sum(c, axis=1))
```

## Core Concepts

### Vectorization, Broadcasting & Masking

Eliminating slow Python loops through vector operations:

```python
import numpy as np

# Fast random number generation with modern Generator API
rng = np.random.default_rng(seed=42)

# Generate 2D array of sensor readings
readings = rng.normal(loc=25.0, scale=3.0, size=(1000, 5))

# Broadcasting: subtract sensor baseline offsets (shape (5,)) from matrix (1000, 5)
baselines = np.array([24.0, 25.0, 24.5, 25.5, 26.0])
calibrated = readings - baselines

# Boolean masking: identify readings exceeding alert threshold
anomaly_mask = np.abs(calibrated) > 6.0
anomaly_count = np.count_nonzero(anomaly_mask)

print(f"Total readings: {readings.size}, Anomalies detected: {anomaly_count}")
```

### Linear Algebra & Matrix Decomposition with np.linalg

Solving linear equations and singular value decomposition:

```python
# System of equations: Ax = b
A = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([9.0, 8.0])

# Solve for x: [x0, x1]
x = np.linalg.solve(A, b)
print("Solution x:", x)

# Singular Value Decomposition (SVD)
U, S, Vt = np.linalg.svd(A)
print("Singular values:", S)
```

### Memory Layouts: Views vs. Copies

Understanding strides and C-contiguous memory:

```python
arr = np.arange(12, dtype=np.int32).reshape((3, 4))
print("C-Contiguous:", arr.flags['C_CONTIGUOUS'])

# Slice creates a view (shared memory buffer)
sub_view = arr[:2, :2]
sub_view[0, 0] = 999
print("Original modified via view:", arr[0, 0] == 999) # True

# Explicit copy allocates independent memory
safe_copy = arr[:2, :2].copy()
safe_copy[0, 0] = 0
print("Original unchanged by copy:", arr[0, 0] == 999) # True
```

## Common Patterns

### Efficient Memory Views and Strided Slicing

**Problem**: Unnecessary memory duplication when working with sub-arrays of large numerical datasets.

**Solution**:
Leverage NumPy non-copying array views and boolean indexing:

```python
data = np.arange(1_000_000)

# Creates a view, not a memory copy
view = data[::2]
print(view.base is data) # True - shares identical memory buffer

# Fast boolean masking without Python loops
positive_values = data[data > 500_000]
```

## Best Practices

**Do**:

- Target NumPy 2.0+ conventions and use `np.random.default_rng()` instead of legacy `np.random.seed()`.
- Utilize vectorization and boolean array indexing instead of iterating with `for` loops in Python.
- Specify appropriate `dtype` (e.g. `np.float32` vs `np.float64`) to minimize memory footprint in deep learning pipelines.
- Check `arr.flags['C_CONTIGUOUS']` before passing arrays to C/C++/Cython extensions.

**Don't**:

- Use `np.matrix`; it is deprecated—use standard 2D `np.ndarray` and the `@` matrix multiplication operator.
- Mutate sliced arrays without knowing whether they are views or independent copies.
- Append elements to arrays in loops with `np.append()`; allocate pre-sized arrays with `np.empty()` or `np.zeros()`.

## Troubleshooting

| Error                                                              | Cause                                                          | Solution                                                                   |
| :----------------------------------------------------------------- | :------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `ValueError: operands could not be broadcast together with shapes` | Incompatible array dimensions along non-singleton axes.        | Align shapes using `np.newaxis` or `.reshape(-1, 1)`.                      |
| `MemoryError: Unable to allocate array with shape`                 | Array size exceeds available system RAM in standard precision. | Use lower precision dtype (e.g. `np.float32` or `np.int16`) or use memmap. |
| `IndexError: too many indices for array`                           | Accessing 2D index on 1D array.                                | Check array dimensions with `arr.ndim` and `arr.shape`.                    |

## References

- [NumPy Documentation](https://numpy.org/)
