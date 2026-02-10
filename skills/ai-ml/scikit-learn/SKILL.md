---
name: scikit-learn
description: Scikit-learn machine learning library. Use for classical ML.
---

# Scikit-learn

Scikit-learn is the gold standard for "Classical ML" (Regression, SVM, Random Forest). v1.6 (2025) adds **Array API** support (running on GPUs via PyTorch/CuPy).

## When to Use

- **Tabular Data**: Random Forests / Gradient Boosting.
- **Preprocessing**: `StandardScaler`, `LabelEncoder`.
- **Small Data**: When Deep Learning is overkill.

## Core Concepts

### Estimators

Everything implements `.fit(X, y)` and `.predict(X)`.

### Pipelines

Chaining preprocessing and modeling: `Pipeline([('scaler', StandardScaler()), ('svc', SVC())])`.

### Array API

Passing PyTorch tensors directly to Scikit-learn without converting to NumPy (keeping data on GPU).

## Best Practices (2025)

**Do**:

- **Use Pipelines**: Prevent data leakage during cross-validation.
- **Use `HistGradientBoostingClassifier`**: It is much faster than standard extraction implementation (inspired by LightGBM).

**Don't**:

- **Don't use for Images/Audio**: Use PyTorch/DL for unstructured data.

## References

- [Scikit-learn Documentation](https://scikit-learn.org/)
