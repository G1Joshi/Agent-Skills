---
name: xgboost
description: Expert XGBoost assistance covering extreme gradient boosting, tree pruners, DMatrix, GPU hist tree method, and early stopping. Use when training high-accuracy tabular models for competitions and production.
---

# XGBoost

XGBoost is the winningest algorithm in Kaggle history for tabular data. v2.1 (2025) brings native **Blackwell** GPU support and Polars integration.

## When to Use

- **Tabular Data Competitions & Industry Production**: High-performance gradient boosted decision trees for classification and regression.
- **GPU-Accelerated Tree Building**: Training massive datasets on NVIDIA GPUs with `tree_method="hist"` and `device="cuda"`.
- **Handling Missing Values & Sparsity**: Automatic direction assignment for missing values without manual imputation.
- **Monotonic Feature Constraints**: Enforcing domain-specific rules (e.g., higher credit score must never increase interest rate).

## Quick Start

```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scikit-learn compatible API with GPU histogram support
model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=6,
    tree_method="hist", # Ultra-fast histogram method
    device="cuda" if xgb.rabit.get_rank() >= 0 else "cpu"
)

model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"XGBoost Test Accuracy: {accuracy:.4f}")
```

## Core Concepts

#High-Performance XGBClassifier with Early Stopping

Training XGBoost using Scikit-Learn API with GPU acceleration:

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import pandas as pd
import numpy as np

# Sample dataset
X = pd.DataFrame(np.random.randn(20000, 10), columns=[f"feat_{i}" for i in range(10)])
y = (X["feat_0"] + X["feat_1"] * 2 > 0.5).astype(int)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Configure modern XGBoost 2.x classifier
clf = xgb.XGBClassifier(
    n_estimators=1000,
    learning_rate=0.03,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    tree_method="hist",
    device="cuda" if xgb.rabit.is_distributed() else "cpu",
    early_stopping_rounds=30,
    eval_metric="auc",
    random_state=42
)

clf.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=50
)

preds = clf.predict_proba(X_val)[:, 1]
print(f"Validation AUC: {roc_auc_score(y_val, preds):.4f}")
```

#Enforcing Monotonic Constraints

Ensuring predictions strictly increase or decrease with specific features:

```python
# Feature 0 must have positive monotonic relationship (+1), Feature 1 negative (-1)
monotonic_rules = (1, -1, 0, 0, 0, 0, 0, 0, 0, 0)

constrained_clf = xgb.XGBClassifier(
    monotone_constraints=monotonic_rules,
    tree_method="hist",
    n_estimators=100
)
constrained_clf.fit(X_train, y_train)
```

#Saving Model in Universal JSON Format

Exporting trained model for portable cross-platform serving:

```python
# Save model in standard JSON format (recommended for XGBoost 2.x)
clf.save_model("xgboost_model.json")

# Load model in production service
loaded_clf = xgb.XGBClassifier()
loaded_clf.load_model("xgboost_model.json")
```

## Common Patterns

### DMatrix Native Training with Early Stopping Callback

**Problem**: Preventing overfitting without training hundreds of redundant trees after validation loss plateaus.

**Solution**:
Use native `xgb.train` with `early_stopping`:

```python
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_test, label=y_test)

params = {
    "objective": "binary:logistic",
    "eval_metric": "logloss",
    "tree_method": "hist"
}

evals = [(dtrain, "train"), (dval, "val")]
bst = xgb.train(
    params,
    dtrain,
    num_boost_round=1000,
    evals=evals,
    callbacks=[xgb.callback.EarlyStopping(rounds=50, save_best=True)],
    verbose_eval=50
)
```

## Best Practices (2026)

- **Do** target XGBoost 2.x with `tree_method="hist"` and `device="cuda"` for extreme training speedups.
- **Do** save models in the native `.json` format (`model.save_model("model.json")`) rather than binary pickle files.
- **Do** set `early_stopping_rounds` in constructor parameters to prevent overfitting on validation data.
- **Do** utilize `monotone_constraints` when business or regulatory logic demands monotonic behavior.
- **Don't** use deprecated `gpu_hist` tree method; in modern XGBoost use `tree_method="hist"` with `device="cuda"`.
- **Don't** perform manual one-hot encoding on high-cardinality categoricals; use `enable_categorical=True`.
- **Don't** tune hyperparameters without early stopping active; it wastes compute on overfitted trees.

## Troubleshooting

| Error                                                              | Cause                                                           | Solution                                                                              |
| :----------------------------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `XGBoostError: Invalid device ordinal`                             | Requesting GPU when no CUDA device is present or wrong GPU ID.  | Set `device="cpu"` or verify GPU with `nvidia-smi`.                                   |
| `DataFrame columns must be the same as when the model was trained` | Inference DataFrame features do not match training order/names. | Align inference DataFrame columns: `df = df[model.feature_names_in_]`.                |
| `Overfitting on training set`                                      | Trees too deep or learning rate too high.                       | Decrease `max_depth` (e.g. 4-6) and tune regularization `reg_alpha` and `reg_lambda`. |

## References

- [XGBoost Documentation](https://xgboost.readthedocs.io/)
