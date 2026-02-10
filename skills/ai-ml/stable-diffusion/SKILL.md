---
name: stable-diffusion
description: Stable Diffusion image generation models. Use for image AI.
---

# Stable Diffusion

Stable Diffusion (by Stability AI) is the open standard for image generation. SD 3.5 (2025) improves prompt adherence and typography.

## When to Use

- **Control**: You need exact composition control (ControlNet).
- **Local Generation**: Run on your own GPU. No censorship/cost.
- **Fine-Tuning**: training LoRAs on your own face/product.

## Core Concepts

### Diffusers Library

The Hugging Face library to run SD pipelines in Python.

### LoRA (Low-Rank Adaptation)

Small adapter files (100MB) that add a style or character to the base model.

### ComfyUI

The node-based GUI for building complex SD workflows (see separate skill).

## Best Practices (2025)

**Do**:

- **Use SD 3.5 Large**: For best text rendering.
- **Use Flux**: The community has largely moved to **Flux.1** (Black Forest Labs) alongside SD.
- **Use ControlNet**: To force the image to follow a specific pose or edge map.

**Don't**:

- **Don't use SD 1.5**: Unless you need specific legacy LoRAs. SDXL/SD3/Flux are superior.

## References

- [Stability AI Models](https://stability.ai/models)
