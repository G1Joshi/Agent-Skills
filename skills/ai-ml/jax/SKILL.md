---
name: jax
description: Expert JAX assistance covering Autograd, XLA compilation (`jit`), vectorization (`vmap`), and parallelization (`pmap`). Use when building high-performance numerical computing and cutting-edge deep learning research.
---

# JAX

JAX combines composable function transformations with automatic differentiation (Autograd) and Accelerated Linear Algebra (XLA) compilation for high-throughput machine learning research.

## When to Use

- **High-Performance Numerical & Scientific Computing**: Autograd and XLA compilation for accelerated linear algebra on GPU/TPU.
- **Custom Deep Learning Research**: Building neural networks with Flax, Haiku, or Equinox without framework bloat.
- **Composable Function Transformations**: Seamlessly chaining `jit` (compilation), `grad` (derivatives), and `vmap` (vectorization).
- **Multi-Device Distributed Training**: Parallelizing computation across clusters using `pmap` and shard maps (`jax.experimental.shard_map`).

## Quick Start

```python
import jax
import jax.numpy as jnp

# JIT-compiled matrix multiplication and automatic differentiation
@jax.jit
def loss_fn(w, x, y):
    pred = jnp.dot(x, w)
    return jnp.mean((pred - y) ** 2)

# Compute value and gradients simultaneously
grad_fn = jax.grad(loss_fn)

w = jnp.array([1.0, 2.0])
x = jnp.array([[1.0, 0.5], [2.0, 1.0]])
y = jnp.array([2.0, 4.0])

grads = grad_fn(w, x, y)
print("Gradients:", grads)
```

## Core Concepts

### Composable Function Transformations: jit, grad & vmap

Combining just-in-time compilation, automatic differentiation, and automated batching:

```python
import jax
import jax.numpy as jnp

# Pure function definition
def loss_fn(w, x, y):
    pred = jnp.dot(x, w)
    return jnp.mean((pred - y) ** 2)

# Transform 1: Automatic gradient with respect to weights
grad_fn = jax.grad(loss_fn)

# Transform 2: JIT compilation via XLA for extreme GPU speedup
fast_grad_fn = jax.jit(grad_fn)

# Transform 3: Automatic vectorization across batches
# batch_loss_fn handles 2D matrices automatically without loops
vmapped_loss = jax.vmap(loss_fn, in_axes=(None, 0, 0))

# Sample computation
key = jax.random.PRNGKey(42)
w = jax.random.normal(key, (3,))
x = jnp.array([[1.0, 2.0, 3.0]])
y = jnp.array([5.0])

grad_val = fast_grad_fn(w, x, y)
print("Computed Gradient:", grad_val)
```

### Explicit PRNG Key Management

State-free pseudorandom number generation:

```python
import jax

# Initialize root PRNG key
key = jax.random.PRNGKey(2026)

# JAX keys must be explicitly split; never reused
key, subkey1, subkey2 = jax.random.split(key, 3)

data_normal = jax.random.normal(subkey1, shape=(4, 4))
data_uniform = jax.random.uniform(subkey2, shape=(4, 4))

print("Normal sample mean:", jnp.mean(data_normal))
```

### Stateful Model with Equinox & Pure Functions

Expressive, object-oriented neural networks built on pure JAX functions:

```python
import equinox as eqx
import jax
import jax.numpy as jnp

class SimpleMLP(eqx.Module):
    linear1: eqx.nn.Linear
    linear2: eqx.nn.Linear

    def __init__(self, in_features, out_features, key):
        k1, k2 = jax.random.split(key)
        self.linear1 = eqx.nn.Linear(in_features, 64, key=k1)
        self.linear2 = eqx.nn.Linear(64, out_features, key=k2)

    def __call__(self, x):
        x = jax.nn.relu(self.linear1(x))
        return self.linear2(x)

key = jax.random.PRNGKey(0)
model = SimpleMLP(in_features=10, out_features=2, key=key)
sample_input = jnp.ones((10,))
output = model(sample_input)
print("Model output:", output)
```

## Common Patterns

### Batch Vectorization with vmap

**Problem**: Writing manual Python loops to evaluate functions over batches slows down execution.

**Solution**:
Use `jax.vmap` to automatically vectorize single-example functions:

```python
def predict_single(w, x):
    return jnp.dot(x, w)

# Automatically vectorize across batch dimension (axis 0 of x)
predict_batch = jax.vmap(predict_single, in_axes=(None, 0))

batch_x = jnp.ones((100, 10))
weights = jnp.ones(10)
predictions = predict_batch(weights, batch_x) # Output shape: (100,)
```

## Best Practices

**Do**:

- Write purely functional code: zero side effects, no in-place array mutations (`x.at[idx].set(val)` instead of `x[idx] = val`).
- Wrap performance-critical functions with `@jax.jit` to trigger XLA compilation.
- Split PRNG keys explicitly (`jax.random.split(key)`) every time random numbers are generated.
- Use modern high-level libraries like Equinox or Flax Linen rather than writing raw parameter dictionaries.

**Don't**:

- Use standard Python conditionals (`if x > 0:`) inside JIT functions on dynamic tracers; use `jax.lax.cond`.
- Reuse PRNG keys; reusing keys generates statistically correlated random numbers.
- Mutate global variables inside functions transformed with `jit`, `grad`, or `vmap`.

## Troubleshooting

| Error                                                                    | Cause                                                                          | Solution                                                                        |
| :----------------------------------------------------------------------- | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| `ConcretizationTypeError: Abstract tracer value used in Python if/while` | Python conditional branching depends on dynamic JAX array values inside `jit`. | Use `jax.lax.cond` or `jax.lax.while_loop` instead of standard Python `if`.     |
| `JAX arrays are immutable`                                               | In-place assignment attempted (`arr[0] = 5`).                                  | Use functional update syntax: `arr = arr.at[0].set(5)`.                         |
| `PRNGKey reuse warning / identical randomness`                           | Reusing identical PRNG key produces identical random numbers.                  | Split keys before each random operation: `key, subkey = jax.random.split(key)`. |

## References

- [JAX Documentation](https://jax.readthedocs.io/)
