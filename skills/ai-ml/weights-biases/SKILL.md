---
name: weights-biases
description: Expert Weights & Biases (W&B) assistance covering experiment tracking, artifact versioning, hyperparameter sweeps, and model monitoring. Use when tracking deep learning experiments and collaborating on ML workflows.
---

# Weights & Biases (W&B)

W&B is the "Github for ML models". It tracks every run, hyperparameter, and artifact. 2025 brings **W&B Inference** and **Weave**.

## When to Use

- **Enterprise ML Experiment Tracking**: Tracking hyperparameters, training loss curves, GPU utilization, and system metrics.
- **Hyperparameter Tuning with W&B Sweeps**: Automated Bayesian, grid, and random sweeps across distributed compute nodes.
- **Model & Dataset Versioning (Artifacts)**: Storing, versioning, and tracking data lineage for datasets and model checkpoints.
- **Production Model Evaluation & LLM Tracing**: Evaluating LLM prompts and agentic tool calls with Weave / W&B Prompts.

## Quick Start

```python
import wandb

# Initialize experiment run
wandb.init(project="transformer-pretraining", config={"lr": 0.001, "batch_size": 32})

for epoch in range(10):
    # Simulated training step
    train_loss = 0.5 / (epoch + 1)
    val_acc = 0.75 + (epoch * 0.02)

    wandb.log({"epoch": epoch, "loss": train_loss, "val_accuracy": val_acc})

wandb.finish()
```

## Core Concepts

#Experiment Tracking with wandb.init & wandb.log

Logging metrics, hyperparameters, and console output:

```python
import wandb
import numpy as np

# Initialize W&B run
run = wandb.init(
    project="transformer-pretraining",
    name="llama-3.2-finetune-v1",
    config={
        "learning_rate": 2e-5,
        "batch_size": 32,
        "epochs": 5,
        "optimizer": "AdamW",
        "weight_decay": 0.01,
        "architecture": "Llama-3.2-3B"
    }
)

# Access hyperparameter config
config = wandb.config

# Training loop simulation
for epoch in range(config.epochs):
    train_loss = 2.5 / (epoch + 1) + np.random.normal(0, 0.05)
    val_loss = 2.7 / (epoch + 1) + np.random.normal(0, 0.05)
    val_accuracy = 0.6 + 0.07 * epoch

    # Log metrics to dashboard in real-time
    wandb.log({
        "epoch": epoch,
        "train/loss": train_loss,
        "val/loss": val_loss,
        "val/accuracy": val_accuracy,
    })

wandb.finish()
```

#Dataset & Model Checkpoint Versioning with Artifacts

Tracking data lineage and model weights:

```python
import wandb

run = wandb.init(project="model-registry-pipeline", job_type="train")

# Log model artifact with versioning
model_artifact = wandb.Artifact(
    name="fraud_detection_model",
    type="model",
    description="Fine-tuned XGBoost model with calibrated probabilities",
    metadata={"roc_auc": 0.942, "framework": "xgboost"}
)
model_artifact.add_file("model_weights.json")
run.log_artifact(model_artifact)

# In deployment pipeline: consume specific artifact version
deployed_artifact = run.use_artifact("fraud_detection_model:latest")
artifact_dir = deployed_artifact.download()
print(f"Downloaded model to {artifact_dir}")
run.finish()
```

#Automated Hyperparameter Sweeps with wandb.sweep

Running Bayesian optimization across parameters:

```python
import wandb

sweep_config = {
    "method": "bayes",
    "metric": {"name": "val/loss", "goal": "minimize"},
    "parameters": {
        "learning_rate": {"min": 1e-5, "max": 1e-2},
        "batch_size": {"values": [16, 32, 64]},
        "dropout": {"uniform": [0.1, 0.5]}
    }
}

sweep_id = wandb.sweep(sweep_config, project="hyperparameter-sweeps")

def train():
    with wandb.init() as run:
        config = wandb.config
        loss = (config.learning_rate - 1e-3)**2 + config.dropout * 0.1
        wandb.log({"val/loss": loss})

# Run agent across 5 trials
# wandb.agent(sweep_id, function=train, count=5)
```

## Common Patterns

### Dataset and Model Checkpoint Versioning via Artifacts

**Problem**: Untracked dataset updates causing silent regressions across model training runs.

**Solution**:
Log and consume versioned W&B Artifacts:

```python
run = wandb.init(project="nlp-classifier")

# Log versioned training dataset
artifact = wandb.Artifact("customer_reviews", type="dataset")
artifact.add_file("data/reviews_v2.parquet")
run.log_artifact(artifact)

# In training run: link model artifact directly to input dataset lineage
```

## Best Practices (2026)

- **Do** always set `config=...` in `wandb.init()` to record all training hyperparameters for full experiment reproducibility.
- **Do** call `wandb.finish()` at the end of runs to ensure logs, checkpoints, and system metrics finish syncing.
- **Do** use W&B Artifacts to track datasets and models, establishing end-to-end data lineage and auditability.
- **Do** group related runs using `group="experiment_group_name"` for cleaner team dashboards.
- **Don't** call `wandb.log()` in tight microsecond inner loops; log aggregated metrics periodically per step or epoch.
- **Don't** hardcode your API key; configure via environment variable `WANDB_API_KEY`.
- **Don't** log sensitive credentials or unmasked PII data to W&B dashboards.

## Troubleshooting

| Error                                                        | Cause                                                                    | Solution                                                                       |
| :----------------------------------------------------------- | :----------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `wandb.errors.CommError: It appears your API key is invalid` | Missing or invalid `WANDB_API_KEY`.                                      | Run `wandb login` or export `WANDB_API_KEY`.                                   |
| `Network timeout during artifact upload`                     | Uploading massive multi-gigabyte checkpoint without multipart upload.    | Verify stable internet connection or save model checkpoint reference pointers. |
| `Multiple runs logging to the same dashboard line`           | Forgetting to call `wandb.finish()` between consecutive loop iterations. | Ensure `wandb.finish()` is called inside a `try..finally` block.               |

## References

- [Weights & Biases](https://wandb.ai/)
