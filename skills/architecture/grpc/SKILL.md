---
name: grpc
description: gRPC high-performance RPC framework with protobuf. Use for service communication.
---

# gRPC

gRPC is a modern open-source high-performance Remote Procedure Call (RPC) framework that can run in any environment. It uses Protocol Buffers (Protobuf) as its Interface Definition Language (IDL).

## When to Use

- **Microservices Communication**: Low latency, high throughput internal traffic.
- **Polyglot Environments**: Service A (Go) talking to Service B (Java).
- **Streaming**: Bidirectional streaming of data (e.g., Real-time voice/video metadata).
- **Strict Contracts**: When you need strict type safety across services.

## Quick Start

```protobuf
// service.proto
syntax = "proto3";

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

```go
// Server (Go)
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
    return &pb.HelloReply{Message: "Hello " + in.GetName()}, nil
}
```

## Core Concepts

### Protocol Buffers

Binary serialization format. Smaller and faster than JSON.

### HTTP/2

gRPC runs on HTTP/2 by default, enabling Multiplexing (multiple requests over one connection) and Server Push.

### Code Generation

You don't write client libraries manually. You generate them from the `.proto` file for any language (Go, Python, Java, Node, C#).

## Common Patterns

### gRPC-Web

Allows browser clients to talk to gRPC services via a proxy (Envoy).

### Interceptors

Middleware for gRPC. Used for Logging, Auth, and Tracing.

## Best Practices

**Do**:

- Use **Linting** (buf.build) for `.proto` files.
- Manage **Backwards Compatibility** carefully (never change field numbers).
- Use **Deadlines/Timeouts** on every call to prevent resource exhaustion.

**Don't**:

- Don't use gRPC for public browser APIs if simple REST/JSON suffices (proxying adds complexity).
- Don't ignore the `Oneof` feature for union types.

## Troubleshooting

| Error                | Cause                                | Solution                                  |
| :------------------- | :----------------------------------- | :---------------------------------------- |
| `Unavailable (14)`   | Server down or network issue.        | Implement Exponential Backoff Retry.      |
| `Unimplemented (12)` | Service method not found.            | Re-generate code and check `.proto` sync. |
| `Message too large`  | Payload exceeds limit (4MB default). | Increase limit or use Streaming.          |

## References

- [gRPC.io](https://grpc.io/)
- [Protocol Buffers](https://protobuf.dev/)
