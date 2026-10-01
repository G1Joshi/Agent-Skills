---
name: whisper
description: Expert OpenAI Whisper audio transcription assistance covering ASR (Automatic Speech Recognition), timestamps, translation, and faster-whisper. Use when transcribing audio, generating subtitles, or building voice assistants.
---

# Whisper

Whisper (OpenAI) is the industry standard for **Speech-to-Text**. It supports 99 languages and translation. V3 (large-v3) is the current state of the art.

## When to Use

- **Speech-to-Text Audio Transcription**: Transcribing multi-lingual audio recordings into punctuated, accurate text.
- **Audio Translation to English**: Automatically translating non-English speech directly into English transcripts.
- **Word-Level Subtitles & Timestamps**: Generating SRT and VTT subtitles with word-level alignment for video editors.
- **High-Throughput Inference with Faster-Whisper**: Running CTranslate2-accelerated inference with 4x speedup and lower VRAM.

## Quick Start

```python
import whisper

# Load pre-trained model and transcribe audio file
model = whisper.load_model("base")
result = model.transcribe("interview.mp3")

print("Detected language:", result["language"])
print("Full Transcription:\n", result["text"])
```

## Core Concepts

### High-Speed Audio Transcription with Faster-Whisper

Using CTranslate2 acceleration for production-grade transcription:

```python
from faster_whisper import WhisperModel
import time

# Load model in INT8/FP16 precision on GPU
model = WhisperModel(
    model_size_or_path="large-v3",
    device="cuda",
    compute_type="float16"
)

# Transcribe audio file with voice activity detection (VAD)
start_time = time.time()
segments, info = model.transcribe(
    "interview_audio.mp3",
    beam_size=5,
    language="en",
    vad_filter=True, # Skip silent audio gaps
    vad_parameters=dict(min_silence_duration_ms=500)
)

print(f"Detected language: {info.language} with probability {info.language_probability:.2f}")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

print(f"Transcription completed in {time.time() - start_time:.2f} seconds.")
```

### Generating Word-Level Timestamps for Subtitles

Extracting exact timestamps for every individual spoken word:

```python
segments, info = model.transcribe(
    "keynote_speech.mp4",
    word_timestamps=True
)

for segment in segments:
    for word in segment.words:
        print(f"Word: {word.word:12s} ({word.start:.2f}s - {word.end:.2f}s, prob: {word.probability:.2f})")
```

### Direct Audio Translation to English

Transcribing foreign audio directly into English text:

```python
# Task = 'translate' translates non-English speech to English
segments, info = model.transcribe(
    "spanish_lecture.mp3",
    task="translate",
    beam_size=5
)

full_english_transcript = " ".join([segment.text for segment in segments])
print("Translated Transcript:\n", full_english_transcript)
```

## Common Patterns

### Word-Level Timestamps with faster-whisper

**Problem**: Standard Whisper model runs slowly on CPU and only returns coarse segment timestamps.

**Solution**:
Use CTranslate2-accelerated `faster-whisper` with word-level timestamps:

```python
from faster_whisper import WhisperModel

# 4x faster execution with 8-bit quantization on GPU or CPU
model = WhisperModel("small", device="auto", compute_type="int8")

segments, info = model.transcribe("speech.wav", word_timestamps=True)

for segment in segments:
    for word in segment.words:
        print(f"[{word.start:.2f}s -> {word.end:.2f}s] {word.word}")
```

## Best Practices

**Do**:

- Target `faster-whisper` with `compute_type="float16"` or `"int8_float16"` for up to 4x throughput and lower VRAM.
- Enable `vad_filter=True` to filter out background silence and prevent hallucinated repetitive loops.
- Specify `language` explicitly when known in advance to bypass language identification overhead.
- Use `whisper-large-v3` or `whisper-large-v3-turbo` for optimal transcription accuracy.

**Don't**:

- Process long multi-hour audio files as a single unbuffered stream without VAD chunking.
- Use standard OpenAI whisper Python package in production without checking if faster-whisper provides better throughput.
- Feed extremely noisy audio without applying pre-processing bandpass filters or noise suppression.

## Troubleshooting

| Error                                                              | Cause                                                 | Solution                                                                 |
| :----------------------------------------------------------------- | :---------------------------------------------------- | :----------------------------------------------------------------------- |
| `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'` | System dependency `ffmpeg` not installed in PATH.     | Install ffmpeg: `brew install ffmpeg` or `apt-get install ffmpeg`.       |
| `CUDA Out of Memory loading 'large-v3'`                            | Large model weights exceed available GPU VRAM.        | Use `compute_type="float16"` or switch to `medium` / `small` model size. |
| `Transcription hallucinates repetition loops`                      | Audio contains prolonged silence or background music. | Set `no_speech_threshold=0.6` and `condition_on_previous_text=False`.    |

## References

- [Whisper GitHub](https://github.com/openai/whisper)
