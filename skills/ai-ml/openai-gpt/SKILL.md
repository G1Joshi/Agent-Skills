---
name: openai-gpt
description: OpenAI GPT API for chat completions, embeddings, and function calling. Use for AI-powered features.
---

# OpenAI GPT

Large language model API for text generation and AI features.

## When to Use

- Chat and conversational AI
- Text generation and completion
- Code generation
- Embeddings and semantic search

## Quick Start

```typescript
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const completion = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Hello!" },
  ],
});

console.log(completion.choices[0].message.content);
```

## Core Concepts

### Chat Completions

```typescript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a coding assistant." },
    { role: "user", content: "Write a Python function to sort a list" },
  ],
  temperature: 0.7,
  max_tokens: 1000,
});
```

### Function Calling

```typescript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "What is the weather in Tokyo?" }],
  tools: [
    {
      type: "function",
      function: {
        name: "get_weather",
        description: "Get weather for a location",
        parameters: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" },
          },
          required: ["location"],
        },
      },
    },
  ],
});

// Handle tool call
const toolCall = response.choices[0].message.tool_calls?.[0];
if (toolCall) {
  const args = JSON.parse(toolCall.function.arguments);
  const weather = await getWeather(args.location);
  // Continue conversation with tool result
}
```

## Common Patterns

### Streaming

```typescript
const stream = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Tell me a story" }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || "");
}
```

### Embeddings

```typescript
const embedding = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: "Search query text",
});

const vector = embedding.data[0].embedding;
// Store in vector database for semantic search
```

## Best Practices

**Do**:

- Use structured outputs for reliable parsing
- Implement retry logic with exponential backoff
- Monitor token usage and costs
- Use streaming for long responses

**Don't**:

- Expose API keys in client code
- Skip input validation
- Ignore rate limits
- Use high temperatures for factual tasks

## Troubleshooting

| Issue          | Cause             | Solution              |
| -------------- | ----------------- | --------------------- |
| Rate limit     | Too many requests | Implement backoff     |
| Context length | Too many tokens   | Truncate or summarize |
| Hallucinations | Model limitation  | Add grounding/RAG     |

## References

- [OpenAI API Docs](https://platform.openai.com/docs)
- [OpenAI Cookbook](https://cookbook.openai.com/)
