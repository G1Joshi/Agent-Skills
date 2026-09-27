---
name: catboost
description: Expert CatBoost assistance covering gradient boosting on decision trees, native categorical feature handling, and GPU acceleration. Use when training fast, accurate tabular models without manual one-hot encoding.
---

# CatBoost

CatBoost (Yandex) is arguably the easiest boosting library to use because it handles **Categorical Features** automatically and perfectly without tuning.

## When to Use

- **Tabular Data with Categorical Features**: Automatic target encoding and categorical combination without manual one-hot encoding.
- **Low-Latency Inference**: Fast model scoring on CPU and GPU with minimal memory overhead.
- **Ranking & Classification Tasks**: E-commerce recommendation, fraud detection, and click-through-rate (CTR) prediction.
- **Robustness Against Overfitting**: Symmetric (oblivious) decision trees providing stable predictions on small-to-medium datasets.

## Quick Start

```python
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
import pandas as pd

# Native categorical feature support
df = pd.DataFrame({
    'city': ['London', 'Paris', 'Tokyo', 'London', 'Paris'],
    'age': [25, 40, 30, 22, 55],
    'target': [1, 0, 1, 1, 0]
})

X = df[['city', 'age']]
y = df['target']
cat_features = ['city']

model = CatBoostClassifier(iterations=100, learning_rate=0.1, verbose=20)
model.fit(X, y, cat_features=cat_features)
preds = model.predict(X)
```

## Core Concepts

#Native Categorical Feature Handling

Training CatBoostClassifier directly on raw categorical string columns:

```python
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
import pandas as pd

# Load dataset with categorical features
data = pd.DataFrame({
    'city': ['London', 'Paris', 'Tokyo', 'London', 'Tokyo', 'Berlin'],
    'device': ['mobile', 'desktop', 'mobile', 'tablet', 'desktop', 'mobile'],
    'age': [24, 45, 32, 19, 58, 29],
    'churned': [0, 1, 0, 0, 1, 0]
})

X = data[['city', 'device', 'age']]
y = data['churned']
cat_features = ['city', 'device']

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.33, random_state=42)

train_pool = Pool(X_train, y_train, cat_features=cat_features)
val_pool = Pool(X_val, y_val, cat_features=cat_features)

model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    eval_metric='AUC',
    early_stopping_rounds=30,
    random_seed=42,
    verbose=50
)

model.fit(train_pool, eval_set=val_pool)
```

#Feature Importance & SHAP Values

Interpreting model decisions with Tree SHAP:

```python
import shap

# Compute SHAP values directly from CatBoost
explainer = shap.TreeExplainer(model)
shap_values = explainer(val_pool)

# Summarize feature impact
feature_importance = model.get_feature_importance(val_pool, type='PredictionValuesChange')
for name, score in zip(X.columns, feature_importance):
    print(f"Feature: {name:10s} Importance: {score:.4f}")
```

#Exporting Model to ONNX for High-Speed Serving

Serializing trained models for cross-platform C++/Go/Rust inference:

```python
# Save model in ONNX format
model.save_model("catboost_model.onnx", format="onnx")

# Or native binary format
model.save_model("catboost_model.cbm")
```

## Common Patterns

### Early Stopping with Validation Pool

**Problem**: Overfitting on tabular training data during deep gradient tree boosting.

**Solution**:
Pass validation pool with early stopping rounds:

```python
train_pool = Pool(X_train, y_train, cat_features=cat_features)
eval_pool = Pool(X_val, y_val, cat_features=cat_features)

model = CatBoostClassifier(
    iterations=1000,
    early_stopping_rounds=50,
    eval_metric='AUC',
    random_seed=42
)
model.fit(train_pool, eval_set=eval_pool, verbose=100)
print(f"Best iteration: {model.get_best_iteration()}")
```

## Best Practices (2026)

- **Do** pass categorical columns directly to `cat_features` rather than manual one-hot encoding.
- **Do** use `early_stopping_rounds` with a dedicated validation set to prevent overfitting.
- **Do** train on GPU (`task_type="GPU"`) for datasets exceeding 1 million rows for up to 10x-20x speedup.
- **Do** monitor evaluation metrics using `plot=True` in Jupyter or export training logs to TensorBoard.
- **Don't** label encode high-cardinality categoricals manually; CatBoost's target encoding is statistically superior.
- **Don't** use too large `depth` (> 10) unless explicitly regularized; CatBoost defaults (depth 6) are optimal.
- **Don't** evaluate final performance on the validation set used for early stopping; evaluate on a held-out test set.

## Troubleshooting

| Error                                        | Cause                                                               | Solution                                                                        |
| :------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------ |
| `CatBoostError: Cannot convert ... to float` | Categorical column containing strings not listed in `cat_features`. | Explicitly pass list of categorical column names/indices to `cat_features`.     |
| `CUDA out of memory in GPU training`         | Batch size or tree depth too large for GPU VRAM.                    | Reduce `max_depth` (default 6) or train on CPU with `task_type='CPU'`.          |
| `Metric value is NaN`                        | Label array contains missing values or infinite entries.            | Clean target labels and verify binary classification target values are 0 and 1. |

## References

- [CatBoost Documentation](https://catboost.ai/)
