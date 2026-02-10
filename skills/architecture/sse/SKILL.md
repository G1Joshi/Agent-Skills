---
name: sse
description: Server-Sent Events one-way real-time. Use for live updates.
---

# Server-Sent Events (SSE)

SSE allow a web page to get updates from a server. Unlike WebSockets, SSEs are **unidirectional** (Server -> Client) and use standard HTTP.

## When to Use

- **Live Feeds**: News tickers, Sport scores, Stock prices.
- **Progress Updates**: "Processing Import: 45%...", Logging streams.
- **Notifications**: In-app alerts where the user doesn't need to reply instantly via the same channel.
- **Replacement for Polling**: More efficient than asking "Are we there yet?" every second.

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

### Event Stream Format

Plain text. Fields: `event`, `data`, `id`, `retry`.

```
event: update
data: {"value": 42}

data: This is a default message
```

### Auto-Reconnection

Browsers automatically try to reconnect if the connection drops. The server can send a `retry: 5000` field to control the delay.

## Common Patterns

### Connection Limit

Browsers (HTTP/1.1) limit concurrent connections (usually 6) per domain. Using HTTP/2 solves this (Multi-plexing).

## Best Practices

**Do**:

- Use **HTTP/2** to avoid connection limits.
- Send **Hearbeats** (comments `: ping`) to prevent proxies from killing idle connections.
- Use the `Last-Event-ID` header to resume streams after incorrect.

**Don't**:

- Don't use for Gaming/Chat (Latency and bidirectionality needs WebSockets).
- Don't send huge binary blobs (It's text-based).

## Troubleshooting

| Error               | Cause                             | Solution                                           |
| :------------------ | :-------------------------------- | :------------------------------------------------- |
| `Buffered Response` | Nginx/Proxy buffering the stream. | Disable proxy buffering (`X-Accel-Buffering: no`). |
| `Cors Error`        | Standard CORS rules apply.        | Configure Access-Control headers.                  |

## References

- [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
