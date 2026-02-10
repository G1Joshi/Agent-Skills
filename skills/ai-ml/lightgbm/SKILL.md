---
name: lightgbm
description: LightGBM gradient boosting framework. Use for fast ML.
---

# LightGBM

LightGBM is Microsoft's gradient boosting library. It is often **faster** and uses less memory than XGBoost due to leaf-wise tree growth.

## When to Use

- **Huge Datasets**: Optimized for efficiency.
- **Ranking**: `LGBMRanker` is excellent for search/recommendation systems.

## Core Concepts

### Leaf-wise Growth

Grows the tree by splitting the leaf with max loss delta (creates deeper, unbalanced trees) vs Level-wise (balanced).

### Histogram-based

Buckets continuous values into discrete bins for speed.

## Best Practices (2025)

**Do**:

- **Tune `num_leaves`**: The most important parameter for controlling complexity.
- **Use Categorical Features**: Pass indexes of categorical columns directly.

**Don't**:

- **Don't overfit**: Leaf-wise growth overfits easily on small data. Limit `max_depth`.

## References

- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
