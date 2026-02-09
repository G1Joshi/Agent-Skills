---
name: grpc
description: gRPC high-performance RPC with Protocol Buffers. Use for service-to-service communication.
---

# gRPC

High-performance RPC framework with Protocol Buffers.

## When to Use

- Microservices communication
- Low-latency requirements
- Strong typing needs
- Streaming data

## Quick Start

```protobuf
// user.proto
syntax = "proto3";

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (stream User);
}

message GetUserRequest {
  string id = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
}
```

## Core Concepts

### Server Implementation

```typescript
import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";

const packageDefinition = protoLoader.loadSync("user.proto");
const proto = grpc.loadPackageDefinition(packageDefinition);

const server = new grpc.Server();

server.addService(proto.UserService.service, {
  getUser: async (call, callback) => {
    const user = await db.users.findUnique({ where: { id: call.request.id } });
    callback(null, user);
  },

  listUsers: async (call) => {
    const users = await db.users.findMany();
    for (const user of users) {
      call.write(user);
    }
    call.end();
  },
});

server.bindAsync(
  "0.0.0.0:50051",
  grpc.ServerCredentials.createInsecure(),
  () => {
    server.start();
  },
);
```

### Client Usage

```typescript
const client = new proto.UserService(
  "localhost:50051",
  grpc.credentials.createInsecure(),
);

// Unary call
client.getUser({ id: "123" }, (error, user) => {
  if (error) throw error;
  console.log("User:", user);
});

// Stream
const stream = client.listUsers({});
stream.on("data", (user) => console.log("User:", user));
stream.on("end", () => console.log("Done"));
```

## Common Patterns

### Error Handling

```typescript
import { status } from "@grpc/grpc-js";

server.addService(proto.UserService.service, {
  getUser: async (call, callback) => {
    const user = await db.users.findUnique({ where: { id: call.request.id } });

    if (!user) {
      callback({
        code: status.NOT_FOUND,
        message: "User not found",
      });
      return;
    }

    callback(null, user);
  },
});
```

### Interceptors (Middleware)

```typescript
function authInterceptor(options, nextCall) {
  return new grpc.InterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      const token = extractToken(metadata);
      if (!validateToken(token)) {
        listener.onReceiveStatus({
          code: status.UNAUTHENTICATED,
          details: "Invalid token",
        });
        return;
      }
      next(metadata, listener);
    },
  });
}
```

## Best Practices

**Do**:

- Use proto versioning
- Implement proper error codes
- Add deadline/timeout
- Use streaming for large data

**Don't**:

- Send huge messages
- Ignore backpressure
- Skip TLS in production
- Use deprecated fields

## Troubleshooting

| Issue              | Cause              | Solution            |
| ------------------ | ------------------ | ------------------- |
| Connection refused | Server not running | Check server status |
| UNAVAILABLE        | Network issue      | Check connectivity  |
| DEADLINE_EXCEEDED  | Slow response      | Increase timeout    |

## References

- [gRPC Documentation](https://grpc.io/docs/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
