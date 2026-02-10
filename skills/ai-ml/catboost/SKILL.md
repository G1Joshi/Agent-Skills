---
name: catboost
description: CatBoost gradient boosting with categoricals. Use for tabular ML.
---

# CatBoost

CatBoost (Yandex) is arguably the easiest boosting library to use because it handles **Categorical Features** automatically and perfectly without tuning.

## When to Use

- **Categorical Data**: If you have many strings/IDs, CatBoost is king.
- **Default Params**: Works incredibly well out of the box.

## Core Concepts

### Ordered Boosting

A technique to avoid target leakage (overfitting) during training.

### Symmetric Trees

Builds balanced trees, which are faster at inference time.

## Best Practices (2025)

**Do**:

- **Use pool**: `Pool()` is efficient for data loading.
- **Use GPU**: CatBoost's GPU implementation is highly optimized.

**Don't**:

- **Don't One-Hot Encode**: Let CatBoost handle it natively.

## References

- [CatBoost Documentation](https://catboost.ai/)
