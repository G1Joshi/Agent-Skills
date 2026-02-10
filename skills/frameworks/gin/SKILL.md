---
name: gin
description: Gin Go web framework with high performance and middleware. Use for Go APIs.
---

# Gin

Gin is the most popular Go web framework, known for its **martini-like API** and performance (httprouter). v1.10 (2025) adds structured logging and better binding.

## When to Use

- **REST APIs**: The industry standard for Go microservices.
- **Performance**: 40x faster than Martini.
- **Middleware Ecosystem**: Massive library of plugins.

## Core Concepts

### Router

Radix tree based routing. `r.GET("/ping", handler)`.

### Context (`c *gin.Context`)

Holds request, response, and metadata.

### Binding

`ShouldBindJSON` automatically validates structs.

## Best Practices (2025)

**Do**:

- **Use `ShouldBind`**: Better error handling than `Bind` (which panics/writes 400).
- **Use `gin.Recovery()`**: Prevent crashes from taking down the server.
- **Use `Slog`**: Integrate with Go's `log/slog` for structured logs.

**Don't**:

- **Don't abuse `c.Set/Get`**: Use type-safe struct passing where possible.

## References

- [Gin Documentation](https://gin-gonic.com/)
