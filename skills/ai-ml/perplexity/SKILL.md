---
name: perplexity
description: Expert Perplexity AI API assistance covering sonar online models, search grounding, citations, and real-time web retrieval. Use when building search-augmented AI research and current event query pipelines.
---

# Perplexity

Perplexity is an AI search engine. For developers, the **Sonar API** provides grounded, cited answers for building search-enabled apps.

## When to Use

- **Real-Time Web-Augmented Search & Retrieval**: Querying fresh, live web data with grounded, verifiable source citations.
- **Fact-Checking & Research Automation**: Generating comprehensive answers with linked URLs for financial, legal, and tech intelligence.
- **Perplexity Sonar Models via API**: Accessing `sonar-pro`, `sonar`, and reasoning models for production AI assistants.
- **Recency-Filtered Search**: Restricting search scope to the last day, week, or month for breaking developments.

## Quick Start

```python
from openai import OpenAI

# Perplexity uses OpenAI-compatible API format
client = OpenAI(
    api_key="your-perplexity-api-key",
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "user", "content": "What were the major tech announcements this week?"}
    ]
)

print(response.choices[0].message.content)
```

## Core Concepts

#Consuming Perplexity Sonar API with Citations

Querying live web search intelligence using OpenAI-compatible SDK:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "system", "content": "You are a research analyst. Provide factual answers with explicit citations."},
        {"role": "user", "content": "What are the latest developments in quantum computing error correction in 2026?"}
    ],
    temperature=0.2,
)

answer = response.choices[0].message.content
citations = getattr(response, 'citations', [])

print("Answer:\n", answer)
print("\nSources / Citations:")
for i, url in enumerate(citations, 1):
    print(f"[{i}] {url}")
```

#Search Domain & Recency Filtering

Restricting search context to authoritative domains and specific timeframes:

```python
import requests
import json

url = "https://api.perplexity.ai/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ.get('PERPLEXITY_API_KEY')}",
    "Content-Type": "application/json"
}

payload = {
    "model": "sonar",
    "messages": [
        {"role": "user", "content": "What were the key policy changes announced by the central bank this week?"}
    ],
    "search_domain_filter": ["bloomberg.com", "reuters.com", "ft.com"],
    "search_recency_filter": "week" # "day", "week", "month", "year"
}

res = requests.post(url, json=payload, headers=headers)
data = res.json()
print(data['choices'][0]['message']['content'])
```

#Structured Output Formatting with Sonar

Directing the model to output verified markdown data tables:

```python
response = client.chat.completions.create(
    model="sonar",
    messages=[
        {"role": "user", "content": "Compare the top 3 open-source vector databases by license, GitHub stars, and vector indexing algorithm. Output as a Markdown table."}
    ],
    temperature=0.1
)

print(response.choices[0].message.content)
```

## Common Patterns

### Domain-Restricted Search Grounding

**Problem**: Retrieval results include low-quality blogs or outdated forum answers.

**Solution**:
Filter search sources using `search_domain_filter`:

```python
response = client.chat.completions.create(
    model="sonar",
    messages=[{"role": "user", "content": "What is the latest RFC standard for HTTP/3?"}],
    extra_body={
        "search_domain_filter": ["ietf.org", "mozilla.org", "w3.org"],
        "return_citations": True
    }
)

print("Answer:", response.choices[0].message.content)
# Access citation URLs if enabled
citations = getattr(response, "citations", [])
print("Citations:", citations)
```

## Best Practices (2026)

- **Do** target `sonar-pro` for deep analytical research and `sonar` for fast, lightweight web queries.
- **Do** inspect and parse the `citations` array to display clickable references in user-facing interfaces.
- **Do** apply `search_recency_filter` when querying time-sensitive or breaking news topics.
- **Do** use `search_domain_filter` to limit search to trusted corporate, scientific, or government websites.
- **Don't** use high temperature settings (> 0.3) if exact factual precision and strict web grounding are desired.
- **Don't** assume web search is necessary for closed-domain math or pure coding tasks; standard LLMs are faster and cheaper.
- **Don't** hardcode `PERPLEXITY_API_KEY` in scripts; load securely from environment variables.

## Troubleshooting

| Error                        | Cause                                                              | Solution                                                      |
| :--------------------------- | :----------------------------------------------------------------- | :------------------------------------------------------------ |
| `401 Unauthorized`           | Invalid or expired Perplexity API key.                             | Verify API key in Perplexity settings and set `PPLX_API_KEY`. |
| `Model not supported: ...`   | Using deprecated model tag (e.g. `llama-3-sonar-8b`).              | Use active sonar models: `sonar` or `sonar-pro`.              |
| `Base URL missing in client` | Connecting to default api.openai.com instead of api.perplexity.ai. | Specify `base_url="https://api.perplexity.ai"`.               |

## References

- [Perplexity API](https://docs.perplexity.ai/)
