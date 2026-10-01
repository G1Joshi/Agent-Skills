---
name: lightgbm
description: Expert LightGBM assistance covering leaf-wise tree growth, histogram-based gradient boosting, and GPU acceleration. Use when training fast, memory-efficient tabular models on large datasets.
---

# LightGBM

LightGBM is Microsoft's gradient boosting library. It is often **faster** and uses less memory than XGBoost due to leaf-wise tree growth.

## When to Use

- **High-Speed Tabular Machine Learning**: Ultra-fast gradient boosting on large tabular datasets using histogram-based algorithms.
- **Massive Row-Count Datasets**: Training efficiently on millions of rows with low memory consumption (GOSS and EFB).
- **Ranking & Recommendation Systems**: LambdaMART ranking algorithms for search engines and recommendation feeds.
- **Automated Hyperparameter Optimization**: Tuning learning rates, num_leaves, and subsampling with Optuna.

## Quick Start

```python
import lightgbm as lgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

params = {
    'objective': 'binary',
    'metric': 'auc',
    'learning_rate': 0.05,
    'num_leaves': 31
}

model = lgb.train(params, train_data, num_boost_round=100, valid_sets=[val_data])
```

## Core Concepts

### High-Speed Classification with Early Stopping

Training LightGBM on tabular datasets with categorical feature support:

```python
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import pandas as pd
import numpy as np

# Create sample dataset
X = pd.DataFrame({
    'feature_1': np.random.randn(10000),
    'feature_2': np.random.rand(10000),
    'category_col': pd.Series(np.random.choice(['A', 'B', 'C'], 10000), dtype='category')
})
y = (X['feature_1'] + X['feature_2'] > 0.5).astype(int)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train using Scikit-Learn API
clf = lgb.LGBMClassifier(
    n_estimators=1000,
    learning_rate=0.03,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Early stopping callback
callbacks = [
    lgb.early_stopping(stopping_rounds=30),
    lgb.log_evaluation(period=50)
]

clf.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='auc',
    callbacks=callbacks
)

preds = clf.predict_proba(X_val)[:, 1]
print("Validation AUC:", roc_auc_score(y_val, preds))
```

### Feature Importance & Visualization

Extracting gain-based feature contributions:

```python
# Gain reflects the relative contribution of each feature to the model
importance_gain = clf.booster_.feature_importance(importance_type='gain')
features = X.columns

for feat, imp in sorted(zip(features, importance_gain), key=lambda x: x[1], reverse=True):
    print(f"Feature: {feat:15s} Gain: {imp:.2f}")
```

### Saving Model & ONNX Conversion

Persisting trained booster for fast inference:

```python
# Save native booster text format
clf.booster_.save_model("lightgbm_model.txt")

# Load model in production
loaded_booster = lgb.Booster(model_file="lightgbm_model.txt")
test_preds = loaded_booster.predict(X_val)
```

## Common Patterns

### Fast Categorical Feature Binning

**Problem**: High-cardinality categorical variables cause deep sparse trees when one-hot encoded.

**Solution**:
Pass categorical feature names directly to LightGBM dataset for native optimal split finding:

```python
import pandas as pd
df = pd.DataFrame({
    'category': pd.Series(['A', 'B', 'C', 'A']).astype('category'),
    'feature': [1.2, 3.4, 2.1, 4.5],
    'target': [0, 1, 0, 1]
})

train_data = lgb.Dataset(df[['category', 'feature']], label=df['target'],
                         categorical_feature=['category'])
```

## Best Practices

**Do**:

- Cast categorical columns to pandas `category` dtype; LightGBM handles them natively without one-hot encoding.
- Control tree complexity via `num_leaves` (should be smaller than `2^(max_depth)`) to prevent severe overfitting.
- Use `lgb.early_stopping()` and `lgb.log_evaluation()` callbacks during model training.
- Use `device="gpu"` when training datasets with more than 100 features and 1 million rows.

**Don't**:

- Set `max_depth` without tuning `num_leaves`; in LightGBM, `num_leaves` is the primary complexity parameter.
- One-hot encode high-cardinality categorical variables; use native categorical support.
- Evaluate final model performance on the validation split used for early stopping.

## Troubleshooting

| Error                                                             | Cause                                                             | Solution                                                                                     |
| :---------------------------------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| `LightGBMError: Do not support special characters in column name` | Feature names contain JSON/CSV characters like `[`, `]`, or `:`.  | Rename columns using regex: `df.columns = [re.sub(r'[\[\]:]', '_', c) for c in df.columns]`. |
| `Overfitting on small datasets`                                   | Default `num_leaves=31` growing too deep for small sample counts. | Reduce `num_leaves` to 15 and increase `min_child_samples` to 20+.                           |
| `No OpenCL device found`                                          | Running with `device='gpu'` on machine without OpenCL drivers.    | Install OpenCL runtime or switch to CPU: `params['device'] = 'cpu'`.                         |

## References

- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
