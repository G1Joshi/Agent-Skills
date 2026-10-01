---
name: gemini
description: Expert Google Gemini API assistance covering Gemini 1.5 Pro / Flash, multimodal reasoning (audio, video, PDF), and structured outputs. Use when building multi-modal AI applications with Google's foundation models.
---

# Gemini

Gemini is Google's native multimodal foundation model family, featuring native audio, image, and video comprehension alongside million-token context windows and fast tool-calling.

## When to Use

- **Massive Multimodal Understanding**: Gemini 1.5 Pro / Flash processing up to 2 million tokens of text, hours of video, audio, and large codebases.
- **Structured JSON Extraction**: Enforcing rigid response schemas with Pydantic and native `response_schema`.
- **High-Speed Real-Time Inference**: Gemini 1.5 Flash for sub-second, cost-effective conversational assistants and summarization.
- **Code & Repository Analysis**: Analyzing entire GitHub repositories in a single context window.

## Quick Start

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain quantum computing in one short paragraph.",
)

print(response.text)
```

## Core Concepts

### Structured Output with Pydantic & Google GenAI SDK

Enforcing type-safe JSON schema responses:

```python
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class InvoiceExtraction(BaseModel):
    invoice_number: str
    vendor: str
    total_amount: float = Field(description="Total invoice amount in USD")
    items: list[str]
    is_paid: bool

response = client.models.generate_content(
    model='gemini-1.5-flash',
    contents='Invoice #INV-2026-908 from CloudCorp for $1,450.00. Included 2 Cloud Servers and 1 Storage bucket. Paid via Wire.',
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=InvoiceExtraction,
        temperature=0.1
    ),
)

extracted: InvoiceExtraction = InvoiceExtraction.model_validate_json(response.text)
print(f"Extracted Invoice: {extracted.invoice_number}, Total: ${extracted.total_amount}")
```

### Native Video & Audio Multimodal Analysis

Processing video files directly using the File API:

```python
from google import genai

client = genai.Client()

# Upload video file to File API
video_file = client.files.upload(file="presentation.mp4")

# Query video content directly
response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents=[
        video_file,
        "Summarize the key decisions made between timestamp 04:15 and 08:30 in this meeting."
    ]
)

print(response.text)
```

### Context Caching for Massive Contexts

Reducing cost on recurring queries against massive datasets:

```python
from google import genai
from google.genai import types
import datetime

client = genai.Client()

# Create cached content for a massive documentation corpus
cache = client.caches.create(
    model='gemini-1.5-pro',
    config=types.CreateCachedContentConfig(
        contents=[large_documentation_file],
        ttl=datetime.timedelta(hours=2),
        display_name='api_documentation_v2'
    )
)

# Query against cache at significantly reduced per-token cost
response = client.models.generate_content(
    model='gemini-1.5-pro',
    contents='What are the rate limits for the batch endpoint?',
    config=types.GenerateContentConfig(cached_content=cache.name)
)
```

## Common Patterns

### Multimodal Document Analysis (PDF / Audio / Video)

**Problem**: Processing multi-page PDF documents or audio files without complex local extraction libraries.

**Solution**:
Upload file using the Google GenAI File API:

```python
# Upload document directly to Gemini File API
doc_file = client.files.upload(file="contract.pdf")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        doc_file,
        "Extract the governing law, termination notice period, and liability cap."
    ]
)

print(response.text)
```

## Best Practices

**Do**:

- Target the modern Google GenAI SDK (`google-genai`) instead of legacy deprecated libraries.
- Use `gemini-1.5-flash` for high-volume, low-latency tasks and `gemini-1.5-pro` for deep reasoning.
- Enforce structured outputs with `response_schema` and Pydantic models for reliable API integrations.
- Leverage Context Caching for prompts exceeding 32k tokens that are reused across multiple calls.

**Don't**:

- Upload raw video/audio base64 payloads inline; use the `client.files.upload()` API.
- Leave sensitive credentials exposed in client-side code; proxy requests through a secure backend.
- Use high temperature settings (> 0.4) when strict schema compliance or factual retrieval is required.

## Troubleshooting

| Error                                                | Cause                                            | Solution                                                               |
| :--------------------------------------------------- | :----------------------------------------------- | :--------------------------------------------------------------------- |
| `google.genai.errors.APIError: 400 Invalid argument` | Unsupported file format or invalid model name.   | Verify model identifier (e.g. `gemini-2.0-flash` or `gemini-1.5-pro`). |
| `ResourceExhausted: 429 Quota exceeded`              | Rate limit hit on free tier requests per minute. | Implement client-side rate limiting or upgrade to paid tier API key.   |
| `Missing GEMINI_API_KEY environment variable`        | Environment variable not exported in shell.      | Export `export GEMINI_API_KEY="AIzaSy..."`.                            |

## References

- [Gemini API Documentation](https://ai.google.dev/)
