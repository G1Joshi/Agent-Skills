---
name: huggingface
description: Hugging Face transformers library and hub. Use for NLP models.
---

# Hugging Face

Hugging Face is the GitHub of AI. It hosts 1M+ models. 2025 sees massive growth in **Multimodal** models and **Robotics** (LeRobot).

## When to Use

- **Model Discovery**: Finding the SOTA open-source model for any task.
- **Inference**: `transformers` library is the standard way to run models in Python.
- **Datasets**: Accessing standard datasets (`load_dataset('squad')`).

## Core Concepts

### Transformers Library

The API to download and run models. `pipeline('sentiment-analysis')`.

### Hugging Face Hub (Hugging Face CLI)

Versioning, git-based storage for large model weights (`git lfs`).

### Spaces

Hosting simple Gradio/Streamlit apps for model demos.

## Best Practices (2025)

**Do**:

- **Use `bitsandbytes`**: Load 70B models in 4-bit precision easily.
- **Use `accelerate`**: For multi-GPU training/inference distributed across devices.
- **Push to Hub**: Share your fine-tunes.

**Don't**:

- **Don't hardcode paths**: Use `from_pretrained("repo/id")` to auto-cache models.

## References

- [Hugging Face Documentation](https://huggingface.co/docs)
