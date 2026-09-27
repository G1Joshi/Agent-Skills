---
name: fastai
description: Expert fastai deep learning assistance covering high-level learners, vision/tabular/text pipelines, and PyTorch integration. Use when training fast, state-of-the-art neural networks with minimal boilerplate.
---

# fastai

fastai is a layered API on top of PyTorch. It popularized **Transfer Learning** and good defaults (One Cycle Policy).

## When to Use

- **Rapid Deep Learning Prototyping**: Building vision, NLP, and tabular models with layered abstractions on top of PyTorch.
- **Transfer Learning with State-of-the-Art Defaults**: Automated discriminative learning rates, 1cycle scheduling, and mixup data augmentation.
- **Computer Vision Tasks**: Image classification, semantic segmentation, and object detection with minimal boilerplate.
- **Learning Rate Optimization**: Finding optimal learning rates automatically using `lr_find()`.

## Quick Start

```python
from fastai.vision.all import *

# Train state-of-the-art vision classifier in 4 lines
path = untar_data(URLs.PETS)/'images'
def is_cat(x): return x[0].isupper()

dls = ImageDataLoaders.from_name_func(path, get_image_files(path), valid_pct=0.2,
                                     seed=42, label_func=is_cat, item_tfms=Resize(224))

learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)
```

## Core Concepts

#Computer Vision Classifier with DataBlock API

Building an image classification pipeline with automated transforms:

```python
from fastai.vision.all import *

# Define flexible data pipeline
data_block = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(460),
    batch_tfms=aug_transforms(size=224, min_scale=0.75)
)

# Load data from directory
dls = data_block.dataloaders('/path/to/dataset', bs=64)

# Create transfer learning learner with pre-trained ResNet/ConvNeXt
learn = vision_learner(dls, resnet50, metrics=accuracy)

# Find optimal learning rate
suggested_lr = learn.lr_find()
print(f"Optimal Learning Rate: {suggested_lr.valley}")

# Fine-tune using 1cycle policy
learn.fine_tune(epochs=4, base_lr=suggested_lr.valley)
```

#Tabular Deep Learning with Categorical Embeddings

Training neural networks on structured tabular data:

```python
from fastai.tabular.all import *

df = pd.read_csv('customers.csv')

cat_names = ['workclass', 'education', 'marital-status', 'occupation']
cont_names = ['age', 'fnlwgt', 'education-num', 'hours-per-week']
procs = [Categorify, FillMissing, Normalize]

splits = RandomSplitter(valid_pct=0.2)(range_of(df))
to = TabularPandas(df, procs=procs, cat_names=cat_names, cont_names=cont_names, y_names='salary', splits=splits)

dls = to.dataloaders(bs=128)
learn = tabular_learner(dls, layers=[200, 100], metrics=accuracy)
learn.fit_one_cycle(5, 1e-2)
```

#Exporting and Serving Model for Inference

Serializing the learner pipeline into a production artifact:

```python
# Export model and all preprocessing pipelines
learn.export('classifier_model.pkl')

# In production server:
inference_learn = load_learner('classifier_model.pkl')
prediction, pred_idx, probabilities = inference_learn.predict('test_image.jpg')

print(f"Prediction: {prediction}, Confidence: {probabilities[pred_idx]:.4f}")
```

## Common Patterns

### Learning Rate Finder and Discriminative Learning Rates

**Problem**: Picking arbitrary learning rates leads to divergence or slow convergence.

**Solution**:
Use `lr_find()` and fine-tune with slice learning rates:

```python
# 1. Find optimal learning rate
lr_valley = learn.lr_find().valley

# 2. Unfreeze model and train with discriminative learning rates
learn.unfreeze()
learn.fit_one_cycle(4, slice(1e-5, lr_valley))
```

## Best Practices (2026)

- **Do** always run `learn.lr_find()` before training and use `learn.fine_tune()` for pre-trained weights.
- **Do** use `aug_transforms()` with resize-presizing (`item_tfms=Resize(460)`, `batch_tfms=aug_transforms(size=224)`) to minimize blur.
- **Do** call `learn.export()` to package architecture, weights, and pre-processing transforms together.
- **Do** inspect misclassified instances using `ClassificationInterpretation.from_learner(learn).plot_top_losses()`.
- **Don't** train pre-trained models with standard `fit()`; use `fine_tune()` to preserve backbone weights.
- **Don't** process single inference images in raw PyTorch without applying fastai's exported transform pipeline.
- **Don't** ignore class imbalance; supply custom weights to `CrossEntropyLossFlat`.

## Troubleshooting

| Error                                              | Cause                                                           | Solution                                                             |
| :------------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------- |
| `CUDA out of memory in DataLoader`                 | Batch size too large for GPU VRAM.                              | Reduce batch size: `dls = ... bs=32` or `bs=16`.                     |
| `Can't get attribute '...' on <module '__main__'>` | Custom labelling function not pickled during `learn.export()`.  | Define functions in importable module or export before script exits. |
| `RuntimeError: Expected 4D tensor but got 3D`      | Single image passed without batch dimension to `learn.predict`. | Use `learn.predict(img)` directly; it handles batch expansion.       |

## References

- [fast.ai](https://www.fast.ai/)
