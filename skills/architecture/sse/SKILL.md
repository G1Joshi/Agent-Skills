---
name: sse
description: Expert Server-Sent Events (SSE) assistance covering HTTP streaming, EventSource API, unidirectional live updates, reconnection handling, and text/event-stream semantics. Use when streaming LLM completions, delivering live notifications, or building real-time dashboards without WebSockets.
---

# Server-Sent Events (SSE)

SSE allow a web page to get updates from a server. Unlike WebSockets, SSEs are **unidirectional** (Server -> Client) and use standard HTTP.

## When to Use

- **Unidirectional Real-Time Streaming**: Pushing server updates to web browsers without requiring the overhead of bidirectional WebSockets.
- **LLM Token Streaming**: Delivering incremental token completions from OpenAI/Anthropic/vLLM models to frontend chat interfaces.
- **Live Activity Feeds & Dashboards**: Pushing live sport scores, stock tickers, system metrics, and notification counts.
- **Native HTTP/2 Multiplexing**: Benefiting from standard HTTP infrastructure, firewalls, load balancers, and authentication headers.

## Quick Start

```javascript
// Client
const evtSource = new EventSource("/api/events");

evtSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Update:", data);
};
```

```javascript
// Server (Express)
app.get("/api/events", (req, res) => {
  // Headers to keep connection open
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  setInterval(() => {
    // Format: "data: <payload>\n\n"
    res.write(`data: ${JSON.stringify({ time: new Date() })}\n\n`);
  }, 1000);
});
```

## Core Concepts

### `text/event-stream` Protocol Format

Data is pushed over an open HTTP connection formatted in plain text blocks ending with double newlines:

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

id: 101
event: price_update
data: {"symbol": "NVDA", "price": 128.50}

id: 102
event: price_update
data: {"symbol": "AAPL", "price": 224.10}
```

### Browser `EventSource` Client API

Standard browser API with built-in automatic reconnection handling and event dispatching:

```typescript
// Client-side subscription
const eventSource = new EventSource("/api/live-stream");

eventSource.addEventListener("price_update", (e) => {
  const data = JSON.parse(e.data);
  console.log("Updated price:", data.symbol, data.price);
});

eventSource.onerror = (err) => {
  console.error("SSE stream disconnected. Browser will auto-reconnect.", err);
};
```

### Resumable Streams with `Last-Event-ID`

When reconnections occur, the browser automatically transmits the last received ID so servers can replay missed events:

```typescript
// Server resumes from last known event ID
app.get("/api/live-stream", (req, res) => {
  const lastEventId = req.headers["last-event-id"];
  if (lastEventId) {
    const missedEvents = eventLog.getSince(Number(lastEventId));
    missedEvents.forEach((e) =>
      res.write(`id: ${e.id}\ndata: ${JSON.stringify(e)}\n\n`),
    );
  }
});
```

## Common Patterns

### LLM Token Streaming via SSE

**Problem**: Waiting for complete LLM responses takes seconds; users need instant incremental token streaming.  
**Solution**: Stream chunks formatted as Server-Sent Events.

```typescript
app.get("/api/stream", async (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  const stream = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Write a short poem" }],
    stream: true,
  });

  for await (const chunk of stream) {
    const text = chunk.choices[0]?.delta?.content || "";
    res.write(`data: ${JSON.stringify({ text })}\n\n`);
  }
  res.write("event: done\ndata: {}\n\n");
  res.end();
});
```

## Best Practices

**Do**:

- Always Set `X-Accel-Buffering: no`: Disable reverse proxy buffering in Nginx to ensure tokens and events flush instantly to clients.
- Assign Unique Monotonic Event IDs: Include `id: <num>` with each event to enable automatic resumption upon network dropouts.
- Transmit Periodic Keep-Alive Comments: Send a comment (`:

`) every 15-30 seconds to prevent aggressive firewall timeouts.

- Use HTTP/2 in Production: Avoid the legacy HTTP/1.1 6-connection per-domain browser limit by serving SSE over HTTP/2.

**Don't**:

- Use SSE when bidirectional client messages are needed: If clients must push frequent messages upstream, choose WebSockets.
- Omit CORS headers on cross-origin streams: Set appropriate `Access-Control-Allow-Origin` headers on stream endpoints.
- Leave server streams open indefinitely when clients disconnect: Listen to `req.on('close')` to release backend resources immediately.

## Troubleshooting

| Error               | Cause                             | Solution                                           |
| :------------------ | :-------------------------------- | :------------------------------------------------- |
| `Buffered Response` | Nginx/Proxy buffering the stream. | Disable proxy buffering (`X-Accel-Buffering: no`). |
| `Cors Error`        | Standard CORS rules apply.        | Configure Access-Control headers.                  |

## References

- [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
