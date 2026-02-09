---
name: claude
description: Anthropic Claude API for chat, analysis, and tool use. Use for advanced AI reasoning.
---

# Claude

Anthropic's Claude API for conversational AI and complex reasoning.

## When to Use

- Long-form content analysis
- Complex reasoning tasks
- Code generation and review
- Document understanding

## Quick Start

```typescript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const message = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude!" }],
});

console.log(message.content[0].text);
```

## Core Concepts

### Messages API

```typescript
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 4096,
  system: "You are a helpful coding assistant.",
  messages: [{ role: "user", content: "Explain async/await in JavaScript" }],
  temperature: 0.7,
});
```

### Tool Use

```typescript
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  tools: [
    {
      name: "get_weather",
      description: "Get current weather for a location",
      input_schema: {
        type: "object",
        properties: {
          location: { type: "string", description: "City name" },
        },
        required: ["location"],
      },
    },
  ],
  messages: [{ role: "user", content: "What is the weather in Paris?" }],
});

// Handle tool use
if (response.stop_reason === "tool_use") {
  const toolUse = response.content.find((c) => c.type === "tool_use");
  const result = await getWeather(toolUse.input.location);

  // Continue with tool result
  const followUp = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What is the weather in Paris?" },
      { role: "assistant", content: response.content },
      {
        role: "user",
        content: [
          { type: "tool_result", tool_use_id: toolUse.id, content: result },
        ],
      },
    ],
  });
}
```

## Common Patterns

### Streaming

```typescript
const stream = await anthropic.messages.stream({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a story" }],
});

for await (const event of stream) {
  if (event.type === "content_block_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

### Vision

```typescript
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: base64Image,
          },
        },
        { type: "text", text: "What is in this image?" },
      ],
    },
  ],
});
```

## Best Practices

**Do**:

- Use system prompts for consistent behavior
- Leverage extended thinking for complex tasks
- Implement proper error handling
- Stream for better UX

**Don't**:

- Ignore content moderation
- Skip input validation
- Use without rate limiting
- Expose API keys

## Troubleshooting

| Issue            | Cause              | Solution            |
| ---------------- | ------------------ | ------------------- |
| Overloaded error | High demand        | Retry with backoff  |
| Max tokens hit   | Response truncated | Increase max_tokens |
| Tool use loop    | Missing result     | Return tool_result  |

## References

- [Anthropic Docs](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference/)
