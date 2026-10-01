---
name: scikit-learn
description: Expert Scikit-Learn assistance covering classification, regression, clustering, pipelines, cross-validation, and preprocessing. Use when building classical machine learning models and feature engineering pipelines.
---

# Scikit-learn

Scikit-learn is the foundational Python library for classical machine learning, providing robust implementations of regression, classification, clustering, dimensionality reduction, and pipelines.

## When to Use

- **Classical Machine Learning Algorithms**: Linear models, decision trees, random forests, clustering, and dimensionality reduction.
- **End-to-End ML Pipelines**: Constructing robust pipelines combining imputers, encoders, scalers, and estimators.
- **Cross-Validation & Hyperparameter Tuning**: Stratified K-fold validation, GridSearchCV, and RandomizedSearchCV.
- **Model Evaluation & Diagnostic Metrics**: Confusion matrices, ROC-AUC curves, precision-recall tradeoffs, and classification reports.

## Quick Start

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Type-safe, leakage-free ML pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

pipe.fit(X_train, y_train)
score = pipe.score(X_test, y_test)
print(f"Test Accuracy: {score:.4f}")
```

## Core Concepts

### Robust Pipeline with ColumnTransformer

Handling heterogeneous numeric and categorical columns without data leakage:

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split

# Sample dataset
df = pd.DataFrame({
    'age': [25, 45, np.nan, 35, 52, 23],
    'income': [50000, 120000, 85000, 75000, np.nan, 42000],
    'department': ['sales', 'tech', 'marketing', 'tech', 'sales', 'tech'],
    'promoted': [0, 1, 1, 0, 1, 0]
})

X = df.drop(columns=['promoted'])
y = df['promoted']

numeric_features = ['age', 'income']
categorical_features = ['department']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Full model pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', HistGradientBoostingClassifier(random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
model_pipeline.fit(X_train, y_train)
print("Test Score:", model_pipeline.score(X_test, y_test))
```

### Cross-Validation & Metric Evaluation

Evaluating classification performance comprehensively:

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model_pipeline, X, y, cv=cv, scoring='accuracy')

print(f"5-Fold CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

### Hyperparameter Search with HalvingGridSearchCV

Fast successive halving parameter search:

```python
from sklearn.model_selection import HalvingGridSearchCV

param_grid = {
    'classifier__learning_rate': [0.01, 0.05, 0.1],
    'classifier__max_iter': [50, 100, 200]
}

search = HalvingGridSearchCV(model_pipeline, param_grid, cv=3, factor=2, random_state=42)
search.fit(X, y)
print("Best Parameters:", search.best_params_)
```

## Common Patterns

### ColumnTransformer for Heterogeneous Feature Types

**Problem**: Applying separate preprocessing (scaling to numericals, one-hot encoding to categoricals) without data leakage.

**Solution**:
Use `ColumnTransformer`:

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['age', 'income', 'balance']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['occupation', 'city'])
    ]
)

pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', LogisticRegression())
])
```

## Best Practices

**Do**:

- Always use `Pipeline` and `ColumnTransformer` to prevent data leakage between training and validation sets.
- Use `HistGradientBoostingClassifier` / `Regressor` for tabular data; it is much faster than `GradientBoostingClassifier`.
- Set `sparse_output=False` in `OneHotEncoder` when piping into estimators that expect dense NumPy arrays.
- Evaluate models using appropriate metrics (e.g. `roc_auc`, `f1_weighted`, `brier_score_loss`) for imbalanced datasets.

**Don't**:

- Fit transformers on the entire dataset before splitting into train/test; always fit only on `X_train`.
- Use standard `GridSearchCV` on massive parameter grids; use `HalvingGridSearchCV` or Optuna.
- Use `StandardScaler` on sparse data without `with_mean=False`.

## Troubleshooting

| Error                                                           | Cause                                                         | Solution                                                       |
| :-------------------------------------------------------------- | :------------------------------------------------------------ | :------------------------------------------------------------- |
| `ValueError: Input contains NaN, infinity or a value too large` | Missing values in features array before model training.       | Add `SimpleImputer()` step to pipeline before modeling.        |
| `DataConversionWarning: A column-vector y was passed`           | Target label passed with shape `(n, 1)` instead of 1D `(n,)`. | Call `.ravel()` on target array: `y.ravel()`.                  |
| `Data leakage during cross-validation`                          | Scaler fit on entire dataset before train/test splitting.     | Always fit transformers inside an `sklearn.pipeline.Pipeline`. |

## References

- [Scikit-learn Documentation](https://scikit-learn.org/)
