---
name: gemini
description: Google Gemini API for multimodal AI with text, images, and video. Use for multimodal AI.
---

# Gemini

Google's multimodal AI API for text, images, and video understanding.

## When to Use

- Multimodal content analysis
- Long context processing
- Code generation
- Image and video understanding

## Quick Start

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

const result = await model.generateContent("Hello, Gemini!");
console.log(result.response.text());
```

## Core Concepts

### Chat Sessions

```typescript
const chat = model.startChat({
  history: [
    { role: "user", parts: [{ text: "Hello" }] },
    { role: "model", parts: [{ text: "Hi! How can I help?" }] },
  ],
});

const result = await chat.sendMessage("Tell me about TypeScript");
console.log(result.response.text());
```

### Multimodal Input

```typescript
import fs from "fs";

const imageData = fs.readFileSync("image.png");

const result = await model.generateContent([
  { text: "Describe this image" },
  {
    inlineData: {
      mimeType: "image/png",
      data: imageData.toString("base64"),
    },
  },
]);
```

## Common Patterns

### Streaming

```typescript
const result = await model.generateContentStream("Write a poem");

for await (const chunk of result.stream) {
  process.stdout.write(chunk.text());
}
```

### Function Calling

```typescript
const model = genAI.getGenerativeModel({
  model: "gemini-2.0-flash",
  tools: [
    {
      functionDeclarations: [
        {
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
      ],
    },
  ],
});

const result = await model.generateContent("What is the weather in Tokyo?");
const call = result.response.functionCalls?.[0];
if (call) {
  const weatherData = await fetchWeather(call.args.location);
  // Continue conversation with result
}
```

## Best Practices

**Do**:

- Leverage long context for documents
- Use multimodal for rich inputs
- Stream for better responsiveness
- Set safety settings appropriately

**Don't**:

- Ignore rate limits
- Skip content filtering
- Use without error handling
- Expose API keys in client

## Troubleshooting

| Issue         | Cause            | Solution               |
| ------------- | ---------------- | ---------------------- |
| Safety block  | Content filtered | Adjust safety settings |
| Token limit   | Input too long   | Summarize or chunk     |
| Slow response | Large model      | Use Flash variant      |

## References

- [Gemini API Docs](https://ai.google.dev/docs)
- [Gemini Cookbook](https://github.com/google-gemini/cookbook)
