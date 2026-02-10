---
name: midjourney
description: Midjourney AI image generation. Use for creative AI.
---

# Midjourney

Midjourney is a closed-source image generator known for its **artistic quality** and distinct "Midjourney Look". v7 (2025) adds 3D modeling and higher photorealism.

## When to Use

- **Marketing/Art**: Unbeatable aesthetic quality out of the box.
- **Ideation**: Rapidly generating mood boards.
- **Web Interface**: Now usable via web (no longer Discord-only).

## Core Concepts

### Parameters

`--ar 16:9` (Aspect Ratio), `--stylize 100`, `--niji` (Anime style).

### Zoom / Pan / Vary

In-painting and out-painting features to edit generated images.

### Character Reference (`--cref`)

Keep the same character face across different images.

## Best Practices (2025)

**Do**:

- **Use the Web Editor**: Much better than Discord for editing/masking.
- **Use Style References (`--sref`)**: Pass an image URL to copy its art style.
- **Use Permutations**: Generate 4 variations of a prompt with `{red, blue}` syntax.

**Don't**:

- **Don't use for text**: While v7 is better, SD3/Flux are often better for strict text rendering.

## References

- [Midjourney Documentation](https://docs.midjourney.com/)
