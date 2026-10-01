---
name: keras
description: Expert Keras 3 assistance covering multi-backend execution (JAX, PyTorch, TensorFlow), Sequential/Functional APIs, and custom training loops. Use when building deep learning models with clean, modular Python abstractions.
---

# Keras

Keras 3 is a game changer: it is now **multi-backend**. You can write Keras code and run it on top of **JAX, PyTorch, or TensorFlow**.

## When to Use

- **Multi-Backend Deep Learning (Keras 3)**: Writing models that run interchangeably on JAX, PyTorch, or TensorFlow.
- **Rapid Neural Network Prototyping**: Developing vision, NLP, and tabular architectures with clean, intuitive APIs.
- **Production Model Deployment**: Exporting models to ONNX, TensorRT, or TensorFlow Lite.
- **Custom Layers & Loss Functions**: Subclassing `keras.layers.Layer` with backend-agnostic `keras.ops`.

## Quick Start

```python
import os
os.environ["KERAS_BACKEND"] = "torch" # Choose: jax, torch, or tensorflow
import keras
from keras import layers

# Build classifier using Functional API
inputs = keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(32, kernel_size=(3, 3), activation="relu")(inputs)
x = layers.MaxPooling2D(pool_size=(2, 2))(x)
x = layers.Flatten()(x)
outputs = layers.Dense(10, activation="softmax")(x)

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
```

## Core Concepts

### Multi-Backend Functional Model Architecture

Building deep learning architectures compatible with PyTorch, JAX, and TensorFlow:

```python
import os
# Configure backend before importing keras: 'jax', 'torch', or 'tensorflow'
os.environ["KERAS_BACKEND"] = "jax"

import keras
from keras import layers, ops

# Functional API model definition
def create_residual_classifier(input_shape, num_classes):
    inputs = layers.Input(shape=input_shape)

    # Feature extraction block
    x = layers.Dense(128, activation="relu")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)

    # Residual skip connection
    residual = x
    x = layers.Dense(128, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.add([x, residual])

    outputs = layers.Dense(num_classes, activation="softmax")(x)
    return keras.Model(inputs=inputs, outputs=outputs, name="res_classifier")

model = create_residual_classifier(input_shape=(64,), num_classes=10)
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model.summary()
```

### Custom Layer with Backend-Agnostic ops

Writing custom layers using universal `keras.ops`:

```python
import keras
from keras import layers, ops

class ScaleAndShiftLayer(layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self, input_shape):
        self.scale = self.add_weight(
            shape=(input_shape[-1],),
            initializer="ones",
            trainable=True,
            name="scale"
        )
        self.shift = self.add_weight(
            shape=(input_shape[-1],),
            initializer="zeros",
            trainable=True,
            name="shift"
        )

    def call(self, inputs):
        # ops works transparently across JAX, PyTorch, and TensorFlow
        return ops.add(ops.multiply(inputs, self.scale), self.shift)
```

### Robust Training with Modern Callbacks

Automating early stopping, learning rate reduction, and model checkpointing:

```python
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=3,
        min_lr=1e-6
    ),
    keras.callbacks.ModelCheckpoint(
        filepath="best_model.keras",
        monitor="val_accuracy",
        save_best_only=True
    )
]

# model.fit(x_train, y_train, validation_split=0.2, epochs=50, callbacks=callbacks)
```

## Common Patterns

### Custom Layer Subclassing with Backend-Agnostic Operations

**Problem**: Writing custom layers that run seamlessly across JAX, PyTorch, and TensorFlow backends.

**Solution**:
Subclass `keras.layers.Layer` using `keras.ops`:

```python
import keras
from keras import ops

class SimpleDense(keras.layers.Layer):
    def __init__(self, units=32):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(shape=(input_shape[-1], self.units), initializer="glorot_uniform")
        self.b = self.add_weight(shape=(self.units,), initializer="zeros")

    def call(self, inputs):
        return ops.matmul(inputs, self.w) + self.b
```

## Best Practices

**Do**:

- Target Keras 3 with multi-backend compatibility (`os.environ["KERAS_BACKEND"] = "jax"` or `"torch"`).
- Use `keras.ops` instead of backend-specific tensor libraries (`torch.*` or `tf.*`) in custom layers.
- Save models in the native `.keras` zip-based format (`model.save("model.keras")`).
- Always include `EarlyStopping` with `restore_best_weights=True` to prevent overfitting.

**Don't**:

- Use legacy `keras` 2.x patterns tied exclusively to `tf.keras`.
- Write custom training loops unless necessary; `model.compile()` and `model.fit()` provide high optimization.
- Save models using legacy H5 (`.h5`) format; use modern `.keras`.

## Troubleshooting

| Error                                                          | Cause                                                                         | Solution                                                                   |
| :------------------------------------------------------------- | :---------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `Backend mismatch error in Keras 3`                            | Changing `KERAS_BACKEND` after importing Keras.                               | Set `os.environ["KERAS_BACKEND"]` _before_ importing keras.                |
| `ValueError: Shapes (None, 1) and (None, 10) are incompatible` | Loss function mismatch (e.g. `categorical_crossentropy` with integer labels). | Use `sparse_categorical_crossentropy` for integer class labels.            |
| `Layer ... was called on an input with incompatible shape`     | Input dimension does not match `input_shape` of the first layer.              | Inspect model architecture using `model.summary()` to verify layer shapes. |

## References

- [Keras Documentation](https://keras.io/)
