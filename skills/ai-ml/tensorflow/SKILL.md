---
name: tensorflow
description: TensorFlow machine learning platform with Keras. Use for ML models.
---

# TensorFlow

TensorFlow is Google's mature ML framework. In 2025, it is largely in **maintenance mode** compared to JAX/PyTorch, but remains specific for **TFLite** and legacy production.

## When to Use

- **Mobile (TFLite)**: Deploying to Android/iOS (though `LiteRT` is separating).
- **Legacy Enterprise**: Many Fortune 500s still run TFv2 pipelines.
- **TFX**: Complex MLOps pipelines.

## Core Concepts

### SavedModel

The universal serialization format.

### TFLite

Optimized runtime for edge devices.

### XLA

Accelerated Linear Algebra compiler (now shared with JAX).

## Best Practices (2025)

**Do**:

- **Use Keras 3**: If you must use generic TensorFlow, use Keras 3 as the interface.
- **Migrate to JAX**: For new Google-stack research projects.

**Don't**:

- **Don't start new research in TF**: Use PyTorch or JAX.

## References

- [TensorFlow Documentation](https://www.tensorflow.org/)
