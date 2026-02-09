---
name: websockets
description: WebSocket real-time communication with Socket.IO and ws. Use for real-time features.
---

# WebSockets

Real-time bidirectional communication.

## When to Use

- Real-time updates
- Chat applications
- Live notifications
- Collaborative features

## Quick Start

```typescript
// Server (Socket.IO)
import { Server } from "socket.io";

const io = new Server(httpServer, {
  cors: { origin: "*" },
});

io.on("connection", (socket) => {
  console.log("Client connected:", socket.id);

  socket.on("message", (data) => {
    io.emit("message", data);
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected:", socket.id);
  });
});
```

## Core Concepts

### Rooms and Namespaces

```typescript
// Namespaces
const chatNamespace = io.of("/chat");
const notificationsNamespace = io.of("/notifications");

chatNamespace.on("connection", (socket) => {
  // Join room
  socket.join(`room:${roomId}`);

  // Send to room
  socket.to(`room:${roomId}`).emit("user-joined", { userId: socket.id });

  // Leave room
  socket.leave(`room:${roomId}`);
});
```

### Broadcasting

```typescript
// To all clients
io.emit("announcement", { message: "Server restart" });

// To all except sender
socket.broadcast.emit("user-typing", { userId });

// To specific room
io.to("room:123").emit("message", data);

// To multiple rooms
io.to("room:1").to("room:2").emit("event", data);
```

## Common Patterns

### Authentication

```typescript
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  try {
    const user = verifyToken(token);
    socket.data.user = user;
    next();
  } catch (error) {
    next(new Error("Authentication failed"));
  }
});

io.on("connection", (socket) => {
  console.log("User connected:", socket.data.user.name);
});
```

### Error Handling

```typescript
socket.on("action", async (data, callback) => {
  try {
    const result = await processAction(data);
    callback({ success: true, data: result });
  } catch (error) {
    callback({ success: false, error: error.message });
  }
});

// Client
socket.emit("action", data, (response) => {
  if (response.success) {
    console.log("Result:", response.data);
  } else {
    console.error("Error:", response.error);
  }
});
```

## Best Practices

**Do**:

- Implement reconnection logic
- Use rooms for grouping
- Add authentication middleware
- Handle disconnections gracefully

**Don't**:

- Send large payloads
- Ignore connection errors
- Skip heartbeat/ping
- Trust client data

## Troubleshooting

| Issue                | Cause               | Solution               |
| -------------------- | ------------------- | ---------------------- |
| Connection fails     | CORS/firewall       | Check CORS settings    |
| Message not received | Wrong room          | Verify room membership |
| Memory leak          | Uncleaned listeners | Remove on disconnect   |

## References

- [Socket.IO Documentation](https://socket.io/docs/)
- [WebSocket MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
