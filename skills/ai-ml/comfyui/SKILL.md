---
name: comfyui
description: Expert ComfyUI node-based generative AI assistance covering Stable Diffusion, Flux, controlnets, LoRAs, and API automation. Use when building modular visual generation workflows or automating image/video pipelines.
---

# ComfyUI

ComfyUI is a node-based GUI for Stable Diffusion. It gives you infinite control over the generation pipeline. 2025 update (UI Overhaul) makes it more accessible.

## When to Use

- **Advanced Generative Image & Video Pipelines**: Designing node-based workflows for SDXL, Flux.1, and SD3.
- **Modular LoRA & ControlNet Composition**: Layering multi-ControlNet conditions, IP-Adapter, and inpainting nodes.
- **Automated Headless Generation**: Exporting workflow JSONs and executing generation via the ComfyUI REST API / WebSockets.
- **Custom Node Development**: Extending PyTorch pipelines with proprietary filters, conditioning, and model loaders.

## Quick Start

```bash
# Clone and install ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# Run server with GPU acceleration
python main.py --listen 127.0.0.1 --port 8188
```

## Core Concepts

#ComfyUI API Execution via Python

Triggering generation workflows programmatically via the REST API:

```python
import json
import urllib.request
import urllib.parse

def queue_prompt(prompt_workflow: dict, server_address="127.0.0.1:8188") -> str:
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    req.add_header('Content-Type', 'application/json')

    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return res['prompt_id']

# Minimal workflow dictionary structure
workflow_example = {
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "seed": 42,
            "steps": 25,
            "cfg": 7.0,
            "sampler_name": "euler_ancestral",
            "scheduler": "normal",
            "denoise": 1.0,
            "model": ["4", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0]
        }
    }
}
```

#Developing Custom ComfyUI Extension Nodes

Creating a Python custom node module:

```python
import torch

class ImageBrightnessAdjustNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.05}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "adjust_brightness"
    CATEGORY = "ImageProcessing/Color"

    def adjust_brightness(self, image: torch.Tensor, factor: float):
        # image is a Tensor [batch, height, width, channels] in [0, 1]
        adjusted = torch.clamp(image * factor, 0.0, 1.0)
        return (adjusted,)

NODE_CLASS_MAPPINGS = {
    "ImageBrightnessAdjust": ImageBrightnessAdjustNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBrightnessAdjust": "Adjust Image Brightness"
}
```

#Model Checkpoint & LoRA Weight Stacking

Combining base models with style and character LoRAs:

```text
[Load Checkpoint: flux1-dev.sft]
       │ (MODEL, CLIP, VAE)
       ▼
[LoraLoader: style_hyperrealism.safetensors (0.75)]
       │ (MODEL, CLIP)
       ▼
[CLIPTextEncode (Positive Prompt: "cinematic product shot, studio lighting")]
       │ (CONDITIONING)
       ▼
[KSampler] ──► [VAEDecode] ──► [SaveImage]
```

## Common Patterns

### Headless API Workflow Execution via WebSocket

**Problem**: Executing ComfyUI graph generation workflows programmatically from a backend service.

**Solution**:
POST workflow JSON to the `/prompt` endpoint and monitor generation:

```python
import json
import urllib.request

def queue_prompt(prompt_workflow: dict):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

# prompt_workflow is exported from ComfyUI as 'Save (API Format)'
```

## Best Practices (2026)

- **Do** save workflows as API-format JSON (`Save (API Format)`) when building automated backend pipelines.
- **Do** use `torch.cuda.empty_cache()` inside custom nodes processing large latent batches.
- **Do** store model weights (`.safetensors`) on high-speed NVMe drives to minimize checkpoint switching latency.
- **Do** utilize fp8 / nf4 quantized weights for Flux.1 and SD3 when running on consumer GPUs (16GB VRAM or less).
- **Don't** use untrusted third-party custom nodes without reviewing their Python scripts for arbitrary remote execution.
- **Don't** bake text watermarks into prompts; use negative embeddings and ControlNet masks.
- **Don't** execute long render batches synchronously in UI processes; decouple generation with Redis queues.

## Troubleshooting

| Error                                             | Cause                                                   | Solution                                                      |
| :------------------------------------------------ | :------------------------------------------------------ | :------------------------------------------------------------ |
| `Torch CUDA out of memory`                        | Model checkpoint or latent dimension exceeds GPU VRAM.  | Run ComfyUI with `--lowvram` or `--medvram` flag.             |
| `Node not found in graph`                         | Custom node extension not installed in `custom_nodes/`. | Install missing custom node pack via ComfyUI Manager.         |
| `Checkpoint file missing from models/checkpoints` | Model weights file not placed in models directory.      | Move `.safetensors` model weights into `models/checkpoints/`. |

## References

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
