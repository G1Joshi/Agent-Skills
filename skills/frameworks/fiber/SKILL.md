---
name: fiber
description: Expert Fiber Go web framework assistance covering zero-memory allocation, Express-like routing, middleware, and fasthttp. Use when building ultra-low latency microservices in Go.
---

# Fiber

Fiber is an **Express.js** inspired framework for Go, running on `fasthttp` (the fastest HTTP engine for Go). v3 brings generic support and better middleware.

## When to Use

- **Extreme-Performance Go Web Services**: Developing HTTP APIs on top of `fasthttp` with zero memory allocation goals.
- **Express-like Ergonomics in Go**: Writing web handlers with an intuitive, familiar API similar to Express.js.
- **High-Concurrency Low-Latency Microservices**: Handling tens of thousands of concurrent connections with minimal CPU overhead.
- **Real-Time WebSockets & Streaming**: Building low-latency chat, game servers, and IoT ingestion gateways.

## Quick Start

```go
package main

import (
	"log"
	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "ok", "framework": "fiber"})
	})

	log.Fatal(app.Listen(":3000"))
}
```

## Core Concepts

### High-Speed Routing & Context Handlers

Routing requests with Fasthttp-powered zero-allocation context:

```go
package main

import (
	"log"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/recover"
)

type Customer struct {
	ID    string `json:"id"`
	Email string `json:"email"`
}

func main() {
	app := fiber.New(fiber.Config{
		Prefork:       false,
		ServerHeader:  "Fiber-2026",
		CaseSensitive: true,
	})

	app.Use(logger.New())
	app.Use(recover.New())

	api := app.Group("/api/v1")
	api.Get("/customers/:id", func(c *fiber.Ctx) error {
		id := c.Params("id")
		return c.Status(fiber.StatusOK).JSON(Customer{
			ID:    id,
			Email: "customer_" + id + "@example.com",
		})
	})

	log.Fatal(app.Listen(":3000"))
}
```

### JSON Body Parsing & Struct Validation

Binding request payloads efficiently:

```go
type CreateOrderRequest struct {
	ProductID int     `json:"product_id"`
	Quantity  int     `json:"quantity"`
	Price     float64 `json:"price"`
}

func createOrder(c *fiber.Ctx) error {
	req := new(CreateOrderRequest)
	if err := c.BodyParser(req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Cannot parse JSON payload",
		})
	}

	if req.Quantity <= 0 || req.Price <= 0 {
		return c.Status(fiber.StatusUnprocessableEntity).JSON(fiber.Map{
			"error": "Invalid order values",
		})
	}

	return c.Status(fiber.StatusCreated).JSON(req)
}
```

### Native Fiber Rate Limiter Middleware

Protecting endpoints against brute-force and DDoS traffic:

```go
import (
	"time"
	"github.com/gofiber/fiber/v2/middleware/limiter"
)

func applyRateLimiting(app *fiber.App) {
	app.Use(limiter.New(limiter.Config{
		Max:        100,
		Expiration: 1 * time.Minute,
		KeyGenerator: func(c *fiber.Ctx) string {
			return c.IP()
		},
		LimitReached: func(c *fiber.Ctx) error {
			return c.Status(fiber.StatusTooManyRequests).JSON(fiber.Map{
				"error": "Rate limit exceeded. Try again in 60s.",
			})
		},
	}))
}
```

## Common Patterns

### Request Validation with Validator Package

**Problem**: Inbound JSON payloads require strict field and format validation before processing.

**Solution**:
Bind body and validate with `go-playground/validator`:

```go
type CreateUserPayload struct {
	Name  string `json:"name" validate:"required,min=3"`
	Email string `json:"email" validate:"required,email"`
}

func CreateUser(c *fiber.Ctx) error {
	payload := new(CreateUserPayload)
	if err := c.BodyParser(payload); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}
	// Validate struct
	if err := validate.Struct(payload); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}
	return c.Status(fiber.StatusCreated).JSON(payload)
}
```

## Best Practices

**Do**:

- Use `c.CopyString()` or allocate heap copies if passing `c.Params()` or `c.Body()` to background goroutines.
- Attach `recover.New()` middleware to prevent unhandled panics from terminating the process.
- Evaluate whether Fiber's prefork feature fits the target deployment architecture (e.g. bare metal vs Kubernetes).
- Use `fiber.Map{}` for quick JSON responses and strongly typed structs for domain schemas.

**Don't**:

- Retain `*fiber.Ctx` references across goroutines; Fiber reuses contexts after the handler returns.
- Bypass validation when using `c.BodyParser()`.
- Enable `Prefork: true` inside multi-threaded container environments unless ports are properly balanced.

## Troubleshooting

| Error                                        | Cause                                                             | Solution                                                                              |
| :------------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `Body values modified after handler returns` | Accessing Fiber's recycled buffer memory in background goroutine. | Copy bytes or clone strings before passing to background goroutines (`c.BodyCopy()`). |
| `Method Not Allowed (405)`                   | Route registered with different HTTP method.                      | Verify exact HTTP verb (`app.Post` vs `app.Get`).                                     |
| `Panic: failed to listen to port`            | Target port occupied or non-privileged user trying to bind <1024. | Run on non-privileged port (>1024) or terminate conflicting service.                  |

## References

- [Fiber Documentation](https://gofiber.io/)
