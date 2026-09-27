---
name: grpc
description: Expert gRPC assistance covering Protocol Buffers (proto3), unary and streaming RPCs, HTTP/2 multiplexing, interceptors, and client generation. Use when designing low-latency inter-service communication, polyglot microservice RPCs, or real-time bi-directional streaming.
---

# gRPC

gRPC is a modern open-source high-performance Remote Procedure Call (RPC) framework that can run in any environment. It uses Protocol Buffers (Protobuf) as its Interface Definition Language (IDL).

## When to Use

- **Low-Latency Microservice Communication**: High-throughput inter-service RPCs requiring binary Protobuf serialization and HTTP/2 multiplexing.
- **Polyglot Systems**: Generating strongly-typed, idiomatic client and server stubs across Go, Rust, Java, Python, C++, and Node.js.
- **Bidirectional Streaming**: Real-time communication pipelines requiring continuous duplex message exchanges over a single TCP connection.
- **Internal Cluster Mesh Traffic**: Connecting services behind the API gateway with minimal CPU and bandwidth serialization overhead.

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

#Protocol Buffers (proto3) Contract Definition

Compact binary serialization defined independently of programming languages:

```protobuf
// proto/payment/v1/payment.proto
syntax = "proto3";
package payment.v1;
option go_package = "example.com/payment/v1;paymentv1";

service PaymentService {
  rpc ProcessPayment (ProcessPaymentRequest) returns (ProcessPaymentResponse);
}

message ProcessPaymentRequest {
  string order_id = 1;
  int64 amount_cents = 2;
  string currency = 3;
}

message ProcessPaymentResponse {
  string transaction_id = 1;
  bool is_successful = 2;
}
```

#HTTP/2 Multiplexing & Binary Framing

Multiple concurrent RPC calls share a single TCP connection without head-of-line blocking:

```
TCP Connection
  ├── Stream 1: ProcessPayment(Req #1) ──→ Response #1
  ├── Stream 2: ProcessPayment(Req #2) ──→ Response #2
  └── Stream 3: ServerStream(Telemetry) ──→ Frame A -> Frame B -> Frame C
```

#gRPC Interceptors (Middleware Pipeline)

Intercepts incoming and outgoing calls to inject authentication, tracing, and logging:

```go
// server.go: Unary Server Interceptor
func loggingInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    log.Printf("method=%s duration=%s err=%v", info.FullMethod, time.Since(start), err)
    return resp, err
}
```

## Common Patterns

#Server Streaming RPC for Real-Time Updates
**Problem**: Polling server for updates wastes bandwidth and introduces latency.  
**Solution**: Implement server streaming in Protocol Buffers.

```protobuf
// service.proto
syntax = "proto3";
package telemetry;

service SensorService {
  rpc StreamMetrics (MetricsRequest) returns (stream MetricData);
}

message MetricsRequest { string device_id = 1; }
message MetricData { double cpu = 1; double memory = 2; int64 timestamp = 3; }
```

```go
// server.go
func (s *server) StreamMetrics(req *pb.MetricsRequest, stream pb.SensorService_StreamMetricsServer) error {
    for {
        metric := &pb.MetricData{Cpu: 42.5, Memory: 81.2, Timestamp: time.Now().Unix()}
        if err := stream.Send(metric); err != nil {
            return err
        }
        time.Sleep(1 * time.Second)
    }
}
```

## Best Practices (2026)

**Do**:

- **Reuse gRPC Channels**: Keep gRPC client connections open; initializing new connections on every request destroys HTTP/2 performance.
- **Propagate Context Deadlines / Timeouts**: Always attach timeouts to client contexts (`context.WithTimeout`) to prevent hanging RPCs.
- **Use Protocol Buffer Field Numbers Conservatively**: Never change or delete field tag numbers; mark deprecated tags with `reserved`.
- **Implement gRPC Health Checking Protocol**: Expose standard `grpc.health.v1.Health` for Kubernetes liveness and readiness probes.

**Don't**:

- **Don't expose raw gRPC directly to public web browsers**: Use gRPC-Web or an API Gateway (Envoy/Kong) to translate HTTP/JSON.
- **Don't send massive single messages**: Split multi-megabyte payloads into streaming chunks or use an object store with claim-check keys.
- **Don't ignore status codes**: Use canonical gRPC status codes (`codes.NotFound`, `codes.InvalidArgument`) rather than generic errors.

## Troubleshooting

| Error                | Cause                                | Solution                                  |
| :------------------- | :----------------------------------- | :---------------------------------------- |
| `Unavailable (14)`   | Server down or network issue.        | Implement Exponential Backoff Retry.      |
| `Unimplemented (12)` | Service method not found.            | Re-generate code and check `.proto` sync. |
| `Message too large`  | Payload exceeds limit (4MB default). | Increase limit or use Streaming.          |

## References

- [gRPC.io](https://grpc.io/)
- [Protocol Buffers](https://protobuf.dev/)
