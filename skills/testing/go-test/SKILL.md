---
name: go-test
description: Expert Go test assistance covering table-driven tests, subtests, mocks, and benchmarking. Use when running `go test`, writing unit/integration tests in Go, or measuring performance.
---

# Go Test

Go has a built-in testing framework in the `testing` package. It follows Go's effective, minimalist philosophy: no magic, just code.

## When to Use

- **Go Standard Library Testing**: Official, zero-dependency testing toolchain built directly into the Go runtime.
- **Table-Driven Unit Tests**: Structuring comprehensive test suites with multiple input/output scenarios cleanly in Go.
- **Race Condition Detection**: Identifying concurrent memory access bugs using `go test -race`.
- **Benchmarking & Memory Profiling**: Measuring operations per second and heap allocations with `go test -bench`.

## Quick Start

```go
// main_test.go
package main

import "testing"

func TestAdd(t *testing.T) {
    got := Add(1, 2)
    want := 3
    if got != want {
        t.Errorf("Add(1, 2) = %d; want %d", got, want)
    }
}
```

Run with `go test ./...`.

## Core Concepts

### Table-Driven Test Structure

The idiomatic Go approach for executing multiple test cases using an anonymous slice of structs:

```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        price    float64
        coupon   string
        expected float64
        wantErr  bool
    }{
        {"standard no coupon", 100.0, "", 100.0, false},
        {"vip coupon 20 percent", 100.0, "VIP20", 80.0, false},
        {"invalid negative price", -10.0, "", 0.0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := CalculateDiscount(tt.price, tt.coupon)
            if (err != nil) != tt.wantErr {
                t.Fatalf("CalculateDiscount() error = %v, wantErr %v", err, tt.wantErr)
            }
            if got != tt.expected {
                t.Errorf("got %v, want %v", got, tt.expected)
            }
        })
    }
}
```

### Race Detection (`-race`)

Instruments memory accesses to detect unsafe concurrent reads/writes:

```bash
# Execute test suite with race detector enabled
go test -race ./...
```

### Benchmark Functions (`testing.B`)

Profiles memory allocations and loop throughput:

```go
func BenchmarkJSONSerialization(b *testing.B) {
    payload := Order{ID: "123", Total: 99.50}
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = json.Marshal(payload)
    }
}
```

## Common Patterns

### Table-Driven Tests with Subtests

**Problem**: Writing separate test functions for multiple input combinations creates repetitive, unmaintainable boilerplate.

**Solution**:
Use anonymous struct slices and `t.Run` subtests:

```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        price    float64
        customer string
        expected float64
    }{
        {"VIP customer", 100.0, "VIP", 80.0},
        {"Regular customer", 100.0, "REG", 100.0},
        {"Zero price", 0.0, "VIP", 0.0},
    }

    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            got := CalculateDiscount(tc.price, tc.customer)
            if got != tc.expected {
                t.Errorf("got %.2f; want %.2f", got, tc.expected)
            }
        })
    }
}
```

## Best Practices

**Do**:

- Always Run `go test -race ./...` in CI: Catch elusive concurrency data races before deploying to production.
- Use Subtests with `t.Run()`: Enable granular reporting, isolated setup, and parallel subtest execution (`t.Parallel()`).
- Use `t.Cleanup()` for Resource Teardown: Register cleanup functions adjacent to resource creation rather than relying on deferred functions.
- Measure Code Coverage: Generate HTML coverage reports using `go test -coverprofile=coverage.out ./... && go tool cover -html=coverage.out`.

**Don't**:

- Use heavy assertion libraries when `if got != want` suffices: Idiomatic Go favors simple `if` checks over opaque assertion magic.
- Leave goroutines leaking in tests: Ensure test goroutines exit cleanly before tests finish.
- Ignore `-short` flag: Support `if testing.Short() { t.Skip() }` to allow developers to run quick test cycles locally.

## Troubleshooting

| Error                                         | Cause                                                                             | Solution                                                                        |
| :-------------------------------------------- | :-------------------------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| `panic: test timed out after 10m`             | Deadlock or hanging goroutine in test suite.                                      | Run `go test -v -timeout 30s` and inspect stack traces.                         |
| `testing: warning: no tests to run`           | Test filenames missing `_test.go` suffix or function names missing `Test` prefix. | Rename file to `*_test.go` and functions to `TestXxx(t *testing.T)`.            |
| `data race detected during execution of test` | Unsynchronized concurrent reads and writes to shared variable.                    | Run `go test -race` and protect shared resources with `sync.Mutex` or channels. |

## References

- [Go Testing Package](https://pkg.go.dev/testing)
