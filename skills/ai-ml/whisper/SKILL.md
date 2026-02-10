---
name: whisper
description: Whisper OpenAI speech recognition. Use for speech-to-text.
---

# Whisper

Whisper (OpenAI) is the industry standard for **Speech-to-Text**. It supports 99 languages and translation. V3 (large-v3) is the current state of the art.

## When to Use

- **Transcription**: Creating subtitles for videos.
- **Translation**: Translating audio to English text.
- **Local Privacy**: Runs 100% locally (sensitive meetings).

## Core Concepts

### Models

`tiny`, `base`, `small`, `medium`, `large`, `legacy`, `large-v3`, `large-v3-turbo`.

### Distil-Whisper

Smaller, faster versions of Whisper (6x speedup, 1% accuracy loss).

## Best Practices (2025)

**Do**:

- **Use `insanely-fast-whisper`**: A wrapper that uses Flash Attention to transcribing 2 hours of audio in 2 minutes.
- **Use API for streaming**: OpenAI API supports streaming audio transcription.

**Don't**:

- **Don't use `large` for realtime**: It's too slow. Use `turbo` or `distil` models.

## References

- [Whisper GitHub](https://github.com/openai/whisper)
