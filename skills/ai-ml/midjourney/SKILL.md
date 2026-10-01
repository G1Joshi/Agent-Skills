---
name: midjourney
description: Expert Midjourney generative AI assistance covering prompt engineering, parameters (--v, --ar, --stylize, --chaos), and style referencing. Use when designing photorealistic concept art and production visuals.
---

# Midjourney

Midjourney is an advanced generative image platform recognized for artistic composition, fine detail, photorealism, and parameter-driven prompt manipulation.

## When to Use

- **High-End Concept Art & Creative Exploration**: Synthesizing cinematic illustrations, character design, and game environments.
- **Photorealistic Architectural & Product Visuals**: Generating high-fidelity mockups with precise lighting and texture prompts.
- **Style Consistency with Style References**: Replicating specific artistic styles and palettes across multiple prompts using `--sref`.
- **Multi-Prompt Weighting & Composition**: Blending concepts with explicit semantic weights using `::` syntax.

## Quick Start

```text
/imagine prompt: cinematic wide shot of a futuristic data center with neon liquid cooling, architectural digest style, volumetric lighting, unreal engine 5 render --ar 16:9 --v 6.1 --style raw
```

## Core Concepts

### Core Command Parameters (v6 & v6.1)

Directing aspect ratio, stylization, and rendering engines:

```text
/imagine prompt: cinematic photography of a sleek glass server rack in a minimalist data center, volumetric teal lighting, shallow depth of field, architectural digest style --ar 16:9 --v 6.1 --style raw --stylize 250 --quality 1
```

Parameter breakdown:

- `--ar 16:9`: Sets wide landscape aspect ratio (9:16 for mobile, 1:1 for square).
- `--v 6.1`: Specifies the Midjourney v6.1 rendering algorithm.
- `--style raw`: Reduces Midjourney's default aesthetic bias for more photographic realism.
- `--stylize 250` (`--s`): Controls strength of artistic flair (range 0 to 1000).
- `--chaos 15` (`--c`): Adds variation to initial grid generations (range 0 to 100).

### Style References (--sref) & Character Consistency (--cref)

Transferring aesthetic signatures across scenes:

```text
# Style Reference: match aesthetic of an existing reference image
/imagine prompt: an autonomous delivery drone flying over a futuristic metropolis at sunset --sref https://example.com/style_sample.jpg --sw 800

# Character Reference: maintain subject identity
/imagine prompt: the detective sitting at a rainy cafe table reviewing case files --cref https://example.com/detective_face.jpg --cw 90
```

### Multi-Prompting with Explicit Weights (::)

Preventing concept bleed and tuning semantic emphasis:

```text
# Concept separation: 'hot' and 'dog' instead of a frankfurter
/imagine prompt: hot::2 dog::1 running on beach --ar 3:2

# Negative weighting: suppress specific elements without prompt negative words
/imagine prompt: vibrant Tokyo street market at night, cinematic neon reflections --no blur, text, watermark, vehicles
```

## Common Patterns

### Character Consistency with Style and Character Reference (--sref, --cref)

**Problem**: Generating the same character or style across multiple scenes produces completely different visuals.

**Solution**:
Use `--cref` (character reference) and `--sref` (style reference) parameters:

```text
/imagine prompt: cybernetic detective walking down a rainy alley, night time, cinematic lighting --cref https://url-to-character-face.png --cw 80 --v 6.1

/imagine prompt: cozy cafe interior with warm morning light --sref https://url-to-style-reference.png --sw 100 --v 6.1
```

## Best Practices

**Do**:

- Use `--style raw` when aiming for accurate photorealism and literal prompt adherence.
- Specify lighting, camera lenses, and film stock (e.g. `35mm lens, f/1.8, golden hour illumination`) for realism.
- Leverage `--sref` (Style Reference) with `--sw` (weight) to maintain brand aesthetic across a series of images.
- Use `--no` for negative conditions rather than writing phrases like "without people" in the main prompt.

**Don't**:

- Use buzzwords like "photorealistic", "hyperrealistic", or "4K"; describe physical lighting and textures instead.
- Use long, rambling paragraphs; concise, comma-separated descriptive descriptors yield better results.
- Exceed `--stylize 750` unless abstract, highly stylized, or artistic interpretation is desired.

## Troubleshooting

| Error                                    | Cause                                                                           | Solution                                                             |
| :--------------------------------------- | :------------------------------------------------------------------------------ | :------------------------------------------------------------------- |
| `Invalid parameter: unrecognized flag`   | Typo in parameter name or space between double dashes.                          | Ensure format is exactly `--ar 16:9`, `--v 6.1`, or `--stylize 250`. |
| `Image reference URL cannot be accessed` | Direct link to image URL is private, expired, or not ending in image extension. | Ensure image URL is public and ends in `.png`, `.jpg`, or `.webp`.   |
| `Banned prompt / Content filter trigger` | Prompt contains words flagged by Midjourney community guidelines.               | Rephrase prompt using descriptive, non-violent, non-explicit terms.  |

## References

- [Midjourney Documentation](https://docs.midjourney.com/)
