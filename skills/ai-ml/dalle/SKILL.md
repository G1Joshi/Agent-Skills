---
name: dalle
description: Expert OpenAI DALL-E 3 image generation assistance covering prompting, image sizing, quality presets, and API integration. Use when generating marketing visuals, UI assets, or automated graphic pipelines.
---

# DALL-E 3 / 4

DALL-E is OpenAI's image model. It excels at **Prompt Adherence**—it draws exactly what you ask for, including complex text.

## When to Use

- **Generative Image Synthesis**: Generating high-resolution images from natural language prompts using OpenAI DALL-E 3.
- **Dynamic Asset Generation for Apps**: Automating marketing visuals, blog cover illustrations, and game textures.
- **Inpainting & Image Editing**: Modifying existing images using masks and replacement descriptions.
- **Multi-Variations & Creative Explorations**: Producing stylistic variants of source concept art.

## Quick Start

```python
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A modern isometric illustration of a serverless cloud architecture, vibrant neon colors, dark background",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
print(f"Generated Image: {image_url}")
```

## Core Concepts

### Generating Images with OpenAI Python SDK

Calling the DALL-E 3 API with quality and size parameters:

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.images.generate(
    model="dall-e-3",
    prompt="A minimalist, futuristic server room illuminated by cyan neon fiber-optic cables, sleek architectural photography, 8k resolution",
    size="1024x1024",
    quality="hd",
    style="vivid", # "vivid" or "natural"
    n=1,
)

image_url = response.data[0].url
revised_prompt = response.data[0].revised_prompt

print(f"Generated Image URL: {image_url}")
print(f"DALL-E 3 Revised Prompt: {revised_prompt}")
```

### In-Memory Image Handling with Base64 Format

Receiving image bytes directly without expiring temporary URLs:

```python
import base64
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A flat vector logo of an owl wearing modern glasses, brand icon style, white background",
    size="1024x1024",
    response_format="b64_json"
)

# Decode base64 image data and persist locally
image_b64 = response.data[0].b64_json
image_bytes = base64.b64decode(image_b64)

with open("owl_logo.png", "wb") as f:
    f.write(image_bytes)

print("Saved logo to owl_logo.png")
```

### Image Editing & Inpainting with DALL-E 2

Replacing masked regions in existing PNG images:

```python
from openai import OpenAI

client = OpenAI()

# Edit image using an RGBA PNG with transparency mask
with open("original.png", "rb") as image_file, open("mask.png", "rb") as mask_file:
    response = client.images.edit(
        image=image_file,
        mask=mask_file,
        prompt="Add a golden retriever puppy sitting peacefully on the wooden porch",
        n=1,
        size="1024x1024"
    )

print("Edited Image URL:", response.data[0].url)
```

## Common Patterns

### Style Consistency via Seed Prompts and Revised Prompts

**Problem**: DALL-E 3 automatically rewrites user prompts, making cross-image style consistency difficult.

**Solution**:
Capture and inspect `revised_prompt` to guide subsequent image generations:

```python
response = client.images.generate(
    model="dall-e-3",
    prompt="Minimalist corporate logo of a geometric falcon, flat vector style, white background",
    size="1024x1024"
)

# Use revised_prompt as the stylistic baseline for character variations
revised = response.data[0].revised_prompt
print(f"Model rewritten prompt: {revised}")
```

## Best Practices

**Do**:

- Inspect and log `revised_prompt` returned by DALL-E 3 to understand how OpenAI expanded the user query.
- Use `response_format="b64_json"` and immediately upload generated images to S3/Cloudflare R2; temporary URLs expire in 1 hour.
- Select `style="natural"` for realistic photography and `style="vivid"` for striking digital art or marketing banners.
- Sanitize and moderate user input prompts with OpenAI Moderation API before submitting to DALL-E.

**Don't**:

- Assume standard seed reproducibility; DALL-E 3 does not support fixed deterministic seeds.
- Request more than `n=1` with DALL-E 3 (DALL-E 3 API only accepts `n=1` per call).
- Include prohibited content (celebrities, copyrighted logos) causing immediate safety policy rejections.

## Troubleshooting

| Error                                             | Cause                                                               | Solution                                                                       |
| :------------------------------------------------ | :------------------------------------------------------------------ | :----------------------------------------------------------------------------- |
| `openai.BadRequestError: Safety system triggered` | Prompt contains banned keywords, public figures, or unsafe content. | Refine prompt to describe abstract or artistic concepts without trigger terms. |
| `Invalid size: DALL-E 3 only supports ...`        | Requesting unsupported resolution (e.g. 512x512).                   | Use supported dimensions: `1024x1024`, `1024x1792`, or `1792x1024`.            |
| `DALL-E 3 does not support n > 1`                 | Requesting multiple images per call (`n=2`).                        | Generate images sequentially or make parallel requests with `n=1`.             |

## References

- [OpenAI DALL-E](https://openai.com/dall-e-3)
