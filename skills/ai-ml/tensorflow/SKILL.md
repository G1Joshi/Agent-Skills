---
name: tensorflow
description: TensorFlow deep learning framework with Keras API. Use for ML production and deployment.
---

# TensorFlow

End-to-end machine learning platform with Keras integration.

## When to Use

- Production ML pipelines
- Model deployment (TensorFlow Serving)
- Mobile ML (TensorFlow Lite)
- Large-scale training

## Quick Start

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

## Core Concepts

### Keras Functional API

```python
from tensorflow import keras
from tensorflow.keras import layers

inputs = keras.Input(shape=(784,))
x = layers.Dense(256, activation='relu')(inputs)
x = layers.Dropout(0.2)(x)
x = layers.Dense(128, activation='relu')(x)
outputs = layers.Dense(10, activation='softmax')(x)

model = keras.Model(inputs, outputs, name='classifier')
```

### Custom Training

```python
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

for epoch in range(epochs):
    for x_batch, y_batch in dataset:
        loss = train_step(x_batch, y_batch)
```

## Common Patterns

### Data Pipeline

```python
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
dataset = dataset.shuffle(buffer_size=1024)
dataset = dataset.batch(32)
dataset = dataset.prefetch(tf.data.AUTOTUNE)
```

### Model Saving

```python
# SavedModel format
model.save('saved_model/my_model')

# Load
loaded_model = keras.models.load_model('saved_model/my_model')

# TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_saved_model('saved_model/my_model')
tflite_model = converter.convert()
```

## Best Practices

**Do**:

- Use `@tf.function` for performance
- Use tf.data for data pipelines
- Enable mixed precision training
- Profile with TensorBoard

**Don't**:

- Use Python loops in tf.function
- Create tensors inside training loops
- Ignore eager vs graph mode
- Skip model validation

## Troubleshooting

| Issue         | Cause               | Solution                |
| ------------- | ------------------- | ----------------------- |
| GPU OOM       | Memory limit        | Reduce batch size       |
| Slow training | Not using GPU       | Check device placement  |
| Graph error   | Incompatible shapes | Check tensor dimensions |

## References

- [TensorFlow Documentation](https://www.tensorflow.org/guide)
- [Keras Documentation](https://keras.io/)
