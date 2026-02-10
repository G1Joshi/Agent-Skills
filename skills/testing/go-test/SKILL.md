---
name: go-test
description: Go testing package. Use for Go testing.
---

# Go Test

Go has a built-in testing framework in the `testing` package. It follows Go's effective, minimalist philosophy: no magic, just code.

## When to Use

- **Go Projects**: It is the standard. No 3rd party runner needed.
- **Benchmarks**: Built-in support (`func BenchmarkXxx(b *testing.B)`).

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

### Table Driven Tests

The idiomatic way to write Go tests. Define a slice of structs with input/output, then loop range over them.

```go
tests := []struct {
    input int
    want  int
}{
    {1, 2},
    {2, 4},
}
for _, tc := range tests {
    t.Run("subtest", func(t *testing.T) { ... })
}
```

### Subtests (`t.Run`)

Allows hierarchical test execution and reporting.

### Helper Functions

Use `t.Helper()` in utility functions so that failure logs point to the test caller, not the helper line.

## Best Practices (2025)

**Do**:

- **Use `testify/assert`**: If you hate `if got != want`, use the `testify` library for `assert.Equal(t, want, got)`. It's the most accepted "lib" extension.
- **Run with `-race`**: `go test -race ./...` to detect race conditions.
- **Parallelism**: Use `t.Parallel()` inside tests to speed up execution.

**Don't**:

- **Don't use assertions for everything**: Go prefers explicit error checking.
- **Don't ignore errors**: If a setup step fails, use `t.Fatal` to stop the test immediately.

## References

- [Go Testing Package](https://pkg.go.dev/testing)
