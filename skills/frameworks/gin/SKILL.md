---
name: gin
description: Expert Gin Go web framework assistance covering fast HTTP routing, middleware chains, JSON binding, and group routing. Use when building production-ready REST APIs in Go.
---

# Gin

Gin is a high-performance HTTP web framework written in Go, featuring a fast radix-tree router, composable middleware chains, and structured request validation.

## When to Use

- **High-Throughput Go Microservices**: Building low-latency web services with martini-like API and fast radx tree routing.
- **JSON REST APIs**: Serializing and deserializing payloads with strong validation and minimal allocation overhead.
- **Microservice Middleware Stacks**: Implementing custom logging, auth, rate limiting, and recovery middleware.
- **File Upload & Static Asset Serving**: Fast static asset handling and multipart streaming.

## Quick Start

```go
package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	r.GET("/api/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "pong"})
	})

	r.Run(":8080")
}
```

## Core Concepts

### Radix Tree Routing & Parameter Binding

Fast route matching with typed model binding:

```go
package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

type CreateAccountRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required,min=8"`
}

func main() {
	r := gin.New()
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	v1 := r.Group("/api/v1")
	{
		v1.GET("/health", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{"status": "UP"})
		})

		v1.POST("/accounts", func(c *gin.Context) {
			var req CreateAccountRequest
			if err := c.ShouldBindJSON(&req); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			c.JSON(http.StatusCreated, gin.H{"email": req.Email, "id": 1001})
		})
	}

	_ = r.Run(":8080")
}
```

### Custom Middleware Pipeline

Intercepting requests and calculating execution latency:

```go
package main

import (
	"log"
	"time"
	"github.com/gin-gonic/gin"
)

func LatencyTracker() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		c.Next() // Process subsequent handlers

		latency := time.Since(start)
		status := c.Writer.Status()
		log.Printf("[GIN] %s %s | %d | %v", c.Request.Method, c.Request.URL.Path, status, latency)
	}
}
```

### Structured Validation Error Responses

Converting Go validator errors into actionable API responses:

```go
import (
	"errors"
	"net/http"
	"github.com/go-playground/validator/v10"
	"github.com/gin-gonic/gin"
)

func handleValidationError(c *gin.Context, err error) {
	var ve validator.ValidationErrors
	if errors.As(err, &ve) {
		out := make(map[string]string)
		for _, fe := range ve {
			out[fe.Field()] = "Failed validation rule: " + fe.Tag()
		}
		c.JSON(http.StatusUnprocessableEntity, gin.H{"errors": out})
		return
	}
	c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
}
```

## Common Patterns

### Request Validation with ShouldBindJSON

**Problem**: Manually validating JSON fields leads to verbose boilerplate and runtime type bugs.

**Solution**:
Use Gin's struct tag binding with `binding:"required"`:

```go
type CreateOrderRequest struct {
	ItemId   string  `json:"item_id" binding:"required"`
	Quantity int     `json:"quantity" binding:"required,gt=0"`
	Price    float64 `json:"price" binding:"required,gt=0"`
}

func CreateOrderHandler(c *gin.Context) {
	var req CreateOrderRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, gin.H{"status": "created", "item_id": req.ItemId})
}
```

## Best Practices

**Do**:

- Use `gin.SetMode(gin.ReleaseMode)` in production environments to disable debug logging and increase throughput.
- Use `c.ShouldBindJSON` instead of `c.BindJSON` to retain explicit control over HTTP status error codes.
- Use `c.Copy()` if passing the Gin context to concurrent background goroutines.
- Attach `gin.Recovery()` to avoid server crashes from uncaught panics.

**Don't**:

- Use `gin.Default()` in production if you want customized, structured logging (`gin.New()` + custom logger).
- Read `c.Request.Body` multiple times without buffering; reading drains the request stream.
- Write to `c.Writer` after returning an error.

## Troubleshooting

| Error                                                         | Cause                                                       | Solution                                                                              |
| :------------------------------------------------------------ | :---------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `Headers were already written`                                | Handler returned without exiting after writing response.    | Add `return` statement immediately after calling `c.JSON()` or `c.AbortWithStatus()`. |
| `[GIN-debug] [WARNING] Headers were already written`          | Middleware executed `c.Next()` after writing response body. | Only call `c.Next()` prior to response generation or handle conditionally.            |
| `panic: [recovery] recovered: assignment to entry in nil map` | Inserting key into uninitialized `gin.H` map variable.      | Initialize map with `gin.H{}` or `make(map[string]any)`.                              |

## References

- [Gin Documentation](https://gin-gonic.com/)
