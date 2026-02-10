---
name: echo
description: Echo high-performance Go web framework. Use for Go APIs.
---

# Echo

Echo is a minimalist Go framework known for performance. v4 is stable and widely used for microservices.

## When to Use

- **Microservices**: Lightweight REST APIs.
- **Performance**: Low memory footprint.
- **Simplicity**: No magic, just handlers and middleware.

## Core Concepts

### Context

`c.Param()`, `c.JSON()`. The context object wraps request/response.

### Middleware

Centralized logic. `e.Use(middleware.Logger())`.

### Binding

`c.Bind(u)` binds JSON/Form data to structs.

## Best Practices (2025)

**Do**:

- **Use `Validator`**: Integrate `go-playground/validator` for struct validation.
- **Use `Graceful Shutdown`**: Support safe deployment restarts.
- **Group Routes**: `v1 := e.Group("/v1")`.

**Don't**:

- **Don't ignore errors**: Go requires explicit error handling.

## References

- [Echo Documentation](https://echo.labstack.com/)
