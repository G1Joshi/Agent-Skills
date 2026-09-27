---
name: tensorflow
description: Expert TensorFlow 2.x assistance covering tf.data pipelines, SavedModel serialization, TensorBoard, and multi-GPU distribution strategies. Use when building, training, and deploying production machine learning models.
---

# TensorFlow

TensorFlow is Google's mature ML framework. In 2025, it is largely in **maintenance mode** compared to JAX/PyTorch, but remains specific for **TFLite** and legacy production.

## When to Use

- **Enterprise Production Machine Learning**: End-to-end model deployment with TensorFlow Serving and TFX.
- **Mobile & Embedded Edge Inference**: Compiling models to microcontrollers and mobile apps using TensorFlow Lite (TFLite).
- **High-Performance Data Pipelines with tf.data**: Prefetching, interleaving, and streaming terabyte-scale datasets.
- **Distributed Training Across GPU/TPU Pods**: Scaling multi-worker distributed training with `tf.distribute.MirroredStrategy`.

## Quick Start

```python
import tensorflow as tf

# Define sequential classification model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(30,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
```

## Core Concepts

#High-Throughput Input Pipelines with tf.data

Asynchronous data loading with prefetching and parallel mapping:

```python
import tensorflow as tf

def parse_image_sample(filename, label):
    image_raw = tf.io.read_file(filename)
    image = tf.io.decode_jpeg(image_raw, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = tf.cast(image, tf.float32) / 255.0 # Normalize
    return image, label

def create_dataset(filenames, labels, batch_size=64):
    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
    dataset = dataset.shuffle(buffer_size=1000)
    # Interleave and map in parallel across all CPU cores
    dataset = dataset.map(parse_image_sample, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    # Prefetch batches to GPU memory while current batch trains
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    return dataset
```

#Functional Model & Multi-GPU Distribution

Training models across multiple GPUs with `MirroredStrategy`:

```python
strategy = tf.distribute.MirroredStrategy()
print(f"Number of distributed devices: {strategy.num_replicas_in_sync}")

with strategy.scope():
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')(inputs)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(10, activation='softmax')(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

# model.fit(train_dataset, epochs=10)
```

#Exporting to TensorFlow Lite (TFLite) with INT8 Quantization

Compressing models for mobile deployment:

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert model to quantized TFLite binary
tflite_model = converter.convert()

with open("model_quantized.tflite", "wb") as f:
    f.write(tflite_model)
print("Saved optimized TFLite model.")
```

## Common Patterns

### High-Throughput Input Pipelines with tf.data Prefetching

**Problem**: GPU stays idle waiting for CPU to read, decode, and batch training data.

**Solution**:
Use `tf.data.AUTOTUNE` prefetching:

```python
dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
dataset = (
    dataset.shuffle(buffer_size=10000)
    .batch(64)
    .prefetch(buffer_size=tf.data.AUTOTUNE) # Overlaps preprocessing with GPU compute
)

model.fit(dataset, epochs=10)
```

## Best Practices (2026)

- **Do** always use `num_parallel_calls=tf.data.AUTOTUNE` and `.prefetch(tf.data.AUTOTUNE)` in input pipelines.
- **Do** use `tf.distribute.MirroredStrategy` for seamless single-node multi-GPU data parallelism.
- **Do** wrap heavy computation inside `@tf.function` to compile graphs via AutoGraph for C++ execution speeds.
- **Do** save models in the modern `SavedModel` or `.keras` format rather than legacy checkpoint files.
- **Don't** use Python operations inside `@tf.function`; use `tf.*` operations to ensure clean graph tracing.
- **Don't** execute feed-dict or session APIs; legacy TensorFlow 1.x patterns are completely deprecated.
- **Don't** train on CPU when GPU/TPU acceleration is available; verify devices with `tf.config.list_physical_devices('GPU')`.

## Troubleshooting

| Error                                                | Cause                                                       | Solution                                                                                             |
| :--------------------------------------------------- | :---------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| `ResourceExhaustedError: OOM when allocating tensor` | Batch size or model weights exceed GPU VRAM.                | Reduce batch size or configure memory growth: `tf.config.experimental.set_memory_growth(gpu, True)`. |
| `TensorFlow not detecting GPU`                       | Missing CUDA/cuDNN driver libraries in system library path. | Check detected devices via `tf.config.list_physical_devices('GPU')`.                                 |
| `Graph execution error: Incompatible shapes`         | Input tensor shape mismatch in first model layer.           | Verify input batch dimension matches `input_shape`.                                                  |

## References

- [TensorFlow Documentation](https://www.tensorflow.org/)
