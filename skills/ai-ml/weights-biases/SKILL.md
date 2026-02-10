---
name: weights-biases
description: Weights & Biases ML experiment tracking. Use for ML monitoring.
---

# Weights & Biases (W&B)

W&B is the "Github for ML models". It tracks every run, hyperparameter, and artifact. 2025 brings **W&B Inference** and **Weave**.

## When to Use

- **Visualization**: Live loss curves during training.
- **Collaboration**: Sharing reports ("The loss spiked here") with teammates.
- **Model Registry**: Managing lifecycle.

## Core Concepts

### W&B Run

A single experiment.

### Sweeps

Hyperparameter optimization engine.

### Weave

A toolkit for logging and debugging interactive GenAI applications (like Tracing).

## Best Practices (2025)

**Do**:

- **Use Weave**: For LLM apps. It replaces simple text logging.
- **Log Model Artifacts**: Save `best_model.pt` to W&B, not local disk.

**Don't**:

- **Don't leak secrets**: W&B logs configs. Ensure API keys aren't in your `config` object.

## References

- [Weights & Biases](https://wandb.ai/)
