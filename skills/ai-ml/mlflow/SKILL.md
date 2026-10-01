---
name: mlflow
description: Expert MLflow assistance covering experiment tracking, autologging, model registry, and MLflow recipes. Use when tracking ML metrics, versioning model artifacts, or serving production models.
---

# MLflow

MLflow is an open-source platform for managing the end-to-end machine learning lifecycle, including experiment tracking, model registry, artifact storage, and LLM tracing evaluation.

## When to Use

- **Machine Learning Experiment Tracking**: Logging parameters, metrics, code versions, and artifacts across runs.
- **Model Registry & Governance**: Managing model lifecycle stages (Staging, Production, Archived) with lineage.
- **LLM Evaluation & Prompt Engineering**: Evaluating LLMs, RAG applications, and prompts using MLflow Evaluate.
- **Unified Model Deployment**: Packaging models into self-contained flavors (Python function, PyTorch, ONNX) for one-click deployment.

## Quick Start

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

mlflow.set_experiment("housing_price_prediction")

with mlflow.start_run():
    n_estimators = 50
    model = RandomForestRegressor(n_estimators=n_estimators)
    model.fit(X_train, y_train)

    preds = model.predict(X_val)
    mse = mean_squared_error(y_val, preds)

    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_metric("mse", mse)
    mlflow.sklearn.log_model(model, "random_forest_model")
```

## Core Concepts

### Experiment Tracking & Autologging

Logging parameters, evaluation metrics, and model weights automatically:

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Configure remote or local tracking URI
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("iris_classification_prod")

# Enable automatic framework logging
mlflow.sklearn.autolog(log_model_signatures=True)

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run(run_name="rf_n100_d5") as run:
    params = {"n_estimators": 100, "max_depth": 5, "random_state": 42}
    mlflow.log_params(params)

    clf = RandomForestClassifier(**params)
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    mlflow.log_metric("accuracy", score)
    print(f"Logged run: {run.info.run_id} with Accuracy: {score:.4f}")
```

### Model Registry & Production Staging

Registering and promoting versioned models:

```python
from mlflow import MlflowClient

client = MlflowClient()

# Register model from a completed run artifact
model_uri = f"runs:/{run.info.run_id}/model"
registered_model = mlflow.register_model(model_uri, "CustomerChurnPredictor")

# Assign an alias (MLflow 2.x recommended pattern)
client.set_registered_model_alias(
    name="CustomerChurnPredictor",
    alias="champion",
    version=registered_model.version
)

# Load champion model in production serving microservice
champion_model = mlflow.pyfunc.load_model("models:/CustomerChurnPredictor@champion")
predictions = champion_model.predict(X_test)
```

### LLM Evaluation with mlflow.evaluate

Benchmarking RAG outputs against ground truth datasets:

```python
import mlflow
import pandas as pd

eval_df = pd.DataFrame({
    "inputs": ["What is MLflow?", "How does autologging work?"],
    "ground_truth": [
        "MLflow is an open-source platform for managing the end-to-end ML lifecycle.",
        "Autologging automatically captures metrics, parameters, and models without explicit log statements."
    ],
    "predictions": [
        "MLflow manages machine learning experiments, models, and deployments.",
        "It automatically tracks parameters and metrics during training."
    ]
})

with mlflow.start_run():
    results = mlflow.evaluate(
        data=eval_df,
        targets="ground_truth",
        predictions="predictions",
        model_type="text-summarization",
        evaluators="default"
    )
    print("Evaluation Metrics:", results.metrics)
```

## Common Patterns

### Autologging Framework Integrations

**Problem**: Writing manual `mlflow.log_metric` lines for every epoch and hyperparameter.

**Solution**:
Enable automatic framework-level logging:

```python
import mlflow

# Autolog PyTorch, TensorFlow, Scikit-Learn, LightGBM, or XGBoost
mlflow.autolog()

# Subsequent model.fit() calls automatically log all parameters, metrics, and models
model.fit(X_train, y_train)
```

## Best Practices

**Do**:

- Target MLflow 2.15+ utilizing model aliases (`@champion`, `@challenger`) rather than legacy stage transitions.
- Log model signatures (`mlflow.models.infer_signature`) to ensure input/output schema validation at deployment time.
- Use `mlflow.start_run()` inside Python context managers to ensure runs are reliably closed on errors.
- Back up the remote backend store (PostgreSQL) and artifact repository (S3/GCS) regularly.

**Don't**:

- Store large training datasets directly as artifacts; log dataset hashes and S3 URIs via `mlflow.data`.
- Use local filesystem tracking URIs in production or collaborative team environments.
- Hardcode tracking URIs; configure via environment variable `MLFLOW_TRACKING_URI`.

## Troubleshooting

| Error                                                | Cause                                                                | Solution                                                                       |
| :--------------------------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `MlflowException: Could not find experiment with ID` | Experiment deleted or connecting to mismatched tracking URI.         | Set explicit tracking URI: `mlflow.set_tracking_uri("http://localhost:5000")`. |
| `Artifact transfer failed`                           | S3 / GCS bucket permissions missing on client runner.                | Ensure AWS/GCP credentials with write permissions are active in environment.   |
| `Schema enforcement error on model load`             | Input DataFrame columns mismatch model signature logged at training. | Align DataFrame columns and types with logged `ModelSignature`.                |

## References

- [MLflow Documentation](https://mlflow.org/)
