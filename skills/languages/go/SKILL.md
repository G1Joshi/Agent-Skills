---
name: go
description: Expert Go programming assistance covering goroutines, channels, interfaces, generics, context, and error handling. Use when building microservices, high-concurrency network servers, or cloud-native infrastructure.
---

# Go

A simple, fast, and concurrent language developed by Google.

## When to Use

- **Cloud-Native & Container Infrastructure**: Powering Kubernetes, Docker, Terraform, Prometheus, and cloud-native systems.
- **High-Concurrency Microservices & APIs**: Serving tens of thousands of concurrent HTTP/gRPC requests with minimal memory overhead.
- **Networking Tools & Distributed Daemons**: Building low-latency proxy servers, reverse proxies, and CLI developer tools.
- **Fast Standalone Single-Binary Compilation**: Deploying self-contained static binaries across Linux, macOS, and Windows with zero runtime dependencies.

## Quick Start

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")

    ch := make(chan string)
    go func() {
        ch <- "from goroutine"
    }()

    msg := <-ch
    fmt.Println(msg)
}
```

## Core Concepts

### Goroutines & Channels (CSP Concurrency)

Lightweight green threads managed by the Go runtime scheduler, communicating via channels:

```go
package main

import (
    "fmt"
    "time"
)

func fetchMetric(id int, ch chan<- string) {
    time.Sleep(100 * time.Millisecond)
    ch <- fmt.Sprintf("Metric %d: 99.4", id)
}

func main() {
    ch := make(chan string, 3)

    for i := 1; i <= 3; i++ {
        go fetchMetric(i, ch)
    }

    for i := 1; i <= 3; i++ {
        fmt.Println(<-ch)
    }
}
```

### Implicit Interface Implementation

Types satisfy interfaces automatically without declaring `implements`:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

// Any struct with a matching Read() method satisfies Reader implicitly
```

### Explicit Error Handling & Sentinel Errors

Errors are regular values returned explicitly as the last return argument:

```go
import (
    "errors"
    "fmt"
)

var ErrNotFound = errors.New("record not found")

func FindUser(id string) (*User, error) {
    if id == "" {
        return nil, fmt.Errorf("invalid query: %w", ErrNotFound)
    }
    return &User{ID: id}, nil
}
```

## Common Patterns

### Worker Pool with Context Cancellation

**Problem**: Processing thousands of jobs concurrently without overwhelming system resources or memory.

**Solution**:
Use fixed worker goroutines reading from a shared channel with context cancellation:

```go
package main

import (
	"context"
	"fmt"
	"sync"
)

func worker(ctx context.Context, id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case <-ctx.Done():
			return
		case job, ok := <-jobs:
			if !ok {
				return
			}
			results <- job * 2
		}
	}
}
```

## Best Practices

**Do**:

- Always Pass `context.Context`: Propagate context across function calls to support cancellation, timeouts, and distributed tracing.
- Handle Every Error Explicitly: Check `if err != nil` immediately; wrap errors with `fmt.Errorf("context: %w", err)`.
- Use `sync.Pool` for High-Allocation Code: Reuse byte buffers and temporary structs to alleviate garbage collector pressure.
- Run `golangci-lint` in CI: Catch bugs, memory leaks, and style inconsistencies with comprehensive static analysis.

**Don't**:

- Ignore Goroutine Leaks: Ensure every spawned goroutine has an exit condition or context cancellation listener.
- Use `panic` for standard error flows: Reserve `panic` for unrecoverable startup issues; return `error` for business failures.
- Pass large structs by value: Pass structs by pointer (`*User`) to avoid memory copying overhead on function calls.

## Troubleshooting

| Error                                                                     | Cause                                                                   | Solution                                                                     |
| :------------------------------------------------------------------------ | :---------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `fatal error: all goroutines are asleep - deadlock!`                      | Goroutine waiting on channel with no senders or mutex locked twice.     | Ensure channel close or buffer space, and verify mutex release in `defer`.   |
| `panic: runtime error: invalid memory address or nil pointer dereference` | Accessing method or field on nil pointer variable.                      | Check pointer with `if ptr != nil` before dereferencing.                     |
| `race detected during execution of test`                                  | Concurrent reads and writes to shared variable without synchronization. | Run with `go test -race` and protect accesses with `sync.Mutex` or channels. |

## References

- [Go Documentation](https://go.dev/doc/)
- [Effective Go](https://go.dev/doc/effective_go)
