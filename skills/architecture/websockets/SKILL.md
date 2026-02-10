---
name: websockets
description: WebSockets real-time bidirectional communication. Use for real-time features.
---

# WebSockets

WebSockets provide a persistent connection between a client and server that both parties can use to start sending data at any time.

## When to Use

- **Chat Apps**: Real-time messaging.
- **Gaming**: Multiplayer state synchronization (low latency).
- **Collaborative Editing**: Google Docs style co-authoring.
- **Financial Dashboards**: High-frequency trading updates.

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

### Handshake

Starts as an HTTP Request (`Upgrade: websocket`). If server accepts (`101 Switching Protocols`), the specific TCP connection becomes a WebSocket connection.

### Heartbeat (Ping/Pong)

Essential to keep connections alive through proxies/firewalls that drop idle TCP connections.

## Common Patterns

### Socket.IO

A library that adds features on top of raw WebSockets: Auto-reconnection, Rooms, Fallback to HTTP Long-Polling.

### Pub/Sub

Users subscribe to channels (e.g., `chat_room_1`). The server routes messages only to sockets in that channel (using Redis for scaling across multiple servers).

## Best Practices

**Do**:

- Handle **Scaling** early. Sticky Sessions (if using Socket.IO) or a Redis Adapter are needed for multi-server setups.
- Secure with **WSS** (WebSocket Secure) always.
- Authenticate via a Token in the Query Parameter or initial handshake message (Headers are limited in JS WebSocket API).

**Don't**:

- Don't use WebSockets for simple notifications (Use SSE/Push API).
- Don't assume the connection is infinite. Handle disconnects gracefully.

## Troubleshooting

| Error                    | Cause                                             | Solution                                                                        |
| :----------------------- | :------------------------------------------------ | :------------------------------------------------------------------------------ |
| `Connection Closed 1006` | Abnormal closure (often network or server crash). | Implement auto-reconnect logic with backoff.                                    |
| `Load Balancer drops`    | LB timeout.                                       | Configure Application Load Balancer (ALB) sticky sessions and timeout increase. |

## References

- [MDN WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [Socket.IO](https://socket.io/)
