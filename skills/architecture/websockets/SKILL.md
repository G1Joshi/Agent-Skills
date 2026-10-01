---
name: websockets
description: Expert WebSockets assistance covering bidirectional full-duplex TCP connections, handshake upgrading, heartbeats/ping-pong, connection state management, and horizontal scaling with Redis Pub/Sub. Use when developing chat applications, live collaboration tools, or multiplayer games.
---

# WebSockets

WebSockets provide a persistent connection between a client and server that both parties can use to start sending data at any time.

## When to Use

- **Full-Duplex Real-Time Communication**: Applications requiring continuous, low-latency, two-way message exchanges between client and server.
- **Live Collaborative Canvases & Documents**: Synchronizing multi-user edits, cursor coordinates, and presence indicators (Figma/Google Docs style).
- **Multiplayer Online Gaming & Chat**: Low-overhead messaging protocols where HTTP request-response overhead would introduce unacceptable lag.
- **Financial Trading Desks**: Streaming high-frequency bid/ask order book tickers with sub-millisecond updates.

## Quick Start

```javascript
// Server (Node.js with 'ws')
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", function connection(ws) {
  ws.on("message", function message(data) {
    console.log("received: %s", data);
    // Echo back
    ws.send(`Echo: ${data}`);
  });

  ws.send("Welcome!");
});
```

```javascript
// Client (Browser)
const socket = new WebSocket("ws://localhost:8080");

socket.addEventListener("message", (event) => {
  console.log("Server says:", event.data);
});
```

## Core Concepts

### HTTP Upgrade Handshake Protocol

WebSocket connections begin as standard HTTP GET requests and upgrade to raw TCP full-duplex sockets:

```http
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### Server-Side Socket Management & Rooms

Managing client socket pools and broadcasting to scoped rooms:

```typescript
import { WebSocketServer, WebSocket } from "ws";

const wss = new WebSocketServer({ port: 8080 });
const rooms = new Map<string, Set<WebSocket>>();

wss.on("connection", (ws, req) => {
  const roomId =
    new URL(req.url!, "http://localhost").searchParams.get("room") || "global";

  if (!rooms.has(roomId)) rooms.set(roomId, new Set());
  rooms.get(roomId)!.add(ws);

  ws.on("message", (message) => {
    // Broadcast message to all clients in the room except sender
    for (const client of rooms.get(roomId)!) {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    }
  });

  ws.on("close", () => rooms.get(roomId)?.delete(ws));
});
```

### Heartbeat (Ping/Pong) Keepalive

Detects dead connections caused by client drops or silent network disconnects:

```typescript
// Server heartbeat monitor
const interval = setInterval(() => {
  wss.clients.forEach((ws: any) => {
    if (ws.isAlive === false) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

wss.on("connection", (ws: any) => {
  ws.isAlive = true;
  ws.on("pong", () => {
    ws.isAlive = true;
  });
});
```

## Common Patterns

### Horizontal Scaling with Redis Pub/Sub

**Problem**: Clients connected to different WebSocket server instances cannot exchange messages.  
**Solution**: Distribute broadcast events across server nodes via Redis Pub/Sub.

```typescript
import { WebSocketServer } from "ws";
import { createClient } from "redis";

const wss = new WebSocketServer({ port: 8080 });
const pub = createClient({ url: process.env.REDIS_URL });
const sub = pub.duplicate();
await Promise.all([pub.connect(), sub.connect()]);

// Subscribe to global channel
sub.subscribe("chat_broadcast", (message) => {
  for (const client of wss.clients) {
    if (client.readyState === 1) client.send(message);
  }
});

// Broadcast client message through Redis
wss.on("connection", (ws) => {
  ws.on("message", (data) => pub.publish("chat_broadcast", data.toString()));
});
```

## Best Practices

**Do**:

- Scale Across Nodes with Redis Pub/Sub: Use Redis, NATS, or Kafka to distribute broadcasts across multi-server WebSocket clusters.
- Implement Heartbeats (Ping/Pong): Detect half-open TCP connections by sending periodic pings every 30 seconds.
- Authenticate During the HTTP Handshake: Validate JWT tokens or session cookies in the initial upgrade request before accepting the connection.
- Apply Backpressure & Message Throttling: Limit maximum payload sizes (`maxPayload: 1024 * 1024`) and rate limit rapid client messages.

**Don't**:

- Use WebSockets for simple unidirectional pushes: Use Server-Sent Events (SSE) if clients only receive data and never send upstream.
- Store state on individual server memory alone: Distribute room memberships and sessions using Redis to allow horizontal scaling.
- Transmit uncompressed binary data carelessly: Use compact binary formats like Protobuf or MessagePack for high-frequency coordinate data.

## Troubleshooting

| Error                    | Cause                                             | Solution                                                                        |
| :----------------------- | :------------------------------------------------ | :------------------------------------------------------------------------------ |
| `Connection Closed 1006` | Abnormal closure (often network or server crash). | Implement auto-reconnect logic with backoff.                                    |
| `Load Balancer drops`    | LB timeout.                                       | Configure Application Load Balancer (ALB) sticky sessions and timeout increase. |

## References

- [MDN WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [Socket.IO](https://socket.io/)
