---
name: stable-diffusion
description: Expert Stable Diffusion assistance covering SDXL, SD 1.5, Diffusers library, ControlNet, LoRAs, and prompt weighting. Use when building open-source text-to-image and image-to-image AI pipelines.
---

# Stable Diffusion

Stable Diffusion is an open latent text-to-image diffusion architecture offering versatile fine-tuning (LoRA, ControlNet), local inference, and precise prompt typography adherence.

## When to Use

- **Open-Source Generative Image Synthesis**: Generating photorealistic or stylized artwork using SDXL and Flux with Hugging Face `diffusers`.
- **Precise Spatial Conditioning with ControlNet**: Guiding image composition with depth maps, canny edges, and human poses.
- **Inpainting, Outpainting & Image-to-Image**: Modifying specific masked regions while preserving surrounding image context.
- **Custom Style Adaptation with LoRA**: Applying fine-tuned community style and character adapters.

## Quick Start

```python
import torch
from diffusers import StableDiffusionXLPipeline

# Load SDXL pipeline with FP16 precision
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

prompt = "A high-tech digital laboratory, neon blue accents, volumetric lighting, photorealistic"
image = pipe(prompt=prompt, num_inference_steps=30).images[0]
image.save("output.png")
```

## Core Concepts

### Generating Images with SDXL & Hugging Face Diffusers

High-resolution generative image pipeline with Euler Ancestral scheduler:

```python
import torch
from diffusers import AutoPipelineForText2Image, EulerAncestralDiscreteScheduler

pipeline = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

# Configure fast Euler Ancestral scheduler
pipeline.scheduler = EulerAncestralDiscreteScheduler.from_config(pipeline.scheduler.config)

# Enable memory optimizations
pipeline.enable_vae_tiling()
pipeline.enable_xformers_memory_efficient_attention()

prompt = "cinematic macro photography of a crystal microchip illuminated by blue laser beams, 8k resolution, studio lighting"
negative_prompt = "low resolution, blurry, distorted, watermark, signature, artifacts"

image = pipeline(
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=1024,
    height=1024,
    num_inference_steps=30,
    guidance_scale=7.0
).images[0]

image.save("crystal_chip.png")
```

### ControlNet Conditioning for Spatial Control

Guiding image geometry with Canny edge maps:

```python
import cv2
import numpy as np
from PIL import Image
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel

# Load ControlNet canny model
controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-canny-sdxl-1.0",
    torch_dtype=torch.float16
).to("cuda")

pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# Generate canny edge guide from reference image
input_img = np.array(Image.open("building_sketch.jpg"))
canny_edges = cv2.Canny(input_img, 100, 200)
canny_pil = Image.fromarray(canny_edges)

result = pipe(
    prompt="A modern brutalist concrete villa with lush tropical hanging gardens, photorealistic, 8k",
    image=canny_pil,
    controlnet_conditioning_scale=0.8,
    num_inference_steps=30
).images[0]

result.save("brutalist_villa.png")
```

### Loading & Stacking LoRA Style Weights

Applying domain-specific fine-tuned LoRA weights:

```python
# Load community LoRA style adapter
pipeline.load_lora_weights("nerdyrodent/IsometricSnoo-SDXL", weight_name="isometric_snoo.safetensors", adapter_name="isometric")

# Trigger generation with LoRA active
image = pipeline("isometric 3D model of a cloud server rack, clean clay style", num_inference_steps=25).images[0]
image.save("isometric_rack.png")
```

## Common Patterns

### Memory-Efficient Generation with xFormers and Offloading

**Problem**: SDXL pipelines requiring 12GB+ VRAM crash on consumer GPUs (8GB VRAM).

**Solution**:
Enable sequential CPU offloading and attention slicing:

```python
pipe.enable_model_cpu_offload()
pipe.enable_vae_slicing()
# Reduces peak VRAM footprint down to under 6GB
```

## Best Practices

**Do**:

- Always use `torch.float16` or `torch.bfloat16` with `variant="fp16"` to slash VRAM requirements in half.
- Enable `pipeline.enable_xformers_memory_efficient_attention()` or PyTorch 2.0 SDPA to reduce memory usage during inference.
- Load model weights exclusively in `.safetensors` format rather than legacy PyTorch `.bin` / `.ckpt` files.
- Use `enable_vae_tiling()` when generating or upscaling images beyond 1024x1024 to prevent out-of-memory errors.

**Don't**:

- Use standard 512x512 resolution with SDXL; SDXL is trained natively for 1024x1024 aspect ratios.
- Exceed `guidance_scale=8.5` with SDXL/Flux; excessive CFG values create color saturation artifacts.
- Run inference without setting deterministic seeds (`torch.Generator(device).manual_seed(42)`) when reproducibility is required.

## Troubleshooting

| Error                               | Cause                                                                | Solution                                                            |
| :---------------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------ |
| `Torch CUDA Out of Memory`          | Image dimensions (e.g. >1024x1024) or batch size too large.          | Lower resolution, enable `enable_model_cpu_offload()`, or use FP16. |
| `Black or green blank image output` | VAE NaN error during FP16 precision decode.                          | Run with `--no-half-vae` or use `madebyollin/sdxl-vae-fp16-fix`.    |
| `Cannot find xFormers module`       | xFormers package not compiled or installed for current CUDA version. | Run `pip install xformers` matching installed PyTorch version.      |

## References

- [Stability AI Models](https://stability.ai/models)
