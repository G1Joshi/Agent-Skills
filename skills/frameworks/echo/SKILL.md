---
name: echo
description: Expert Echo Go web framework assistance covering routing, middleware, data binding, and JSON validation. Use when developing high-performance, lightweight microservices in Go.
---

# Echo

Echo is a minimalist Go framework known for performance. v4 is stable and widely used for microservices.

## When to Use

- **High-Performance Go RESTful APIs**: Developing low-latency web services and microservices with minimal allocation overhead.
- **Microservices Requiring Middleware Pipelines**: Utilizing built-in JWT authentication, CORS, rate limiting, and recover middleware.
- **Robust Route Parameter Extraction & Binding**: Automatically binding and validating JSON, XML, and form-data payloads.
- **WebSocket & SSE Streaming Backends**: Real-time push notification endpoints in Go.

## Quick Start

```go
package main

import (
	"net/http"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type User struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

func main() {
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/api/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	e.Logger.Fatal(e.Start(":8080"))
}
```

## Core Concepts

### Handler Registration & Parameter Extraction

Clean route grouping with context parameter extraction:

```go
package main

import (
	"net/http"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type UserResponse struct {
	ID       string `json:"id"`
	Username string `json:"username"`
}

func getUserHandler(c echo.Context) error {
	id := c.Param("id")
	queryFilter := c.QueryParam("include_details")

	return c.JSON(http.StatusOK, UserResponse{
		ID:       id,
		Username: "user_" + id + "_filter_" + queryFilter,
	})
}

func main() {
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	api := e.Group("/api/v1")
	api.GET("/users/:id", getUserHandler)

	e.Logger.Fatal(e.Start(":8080"))
}
```

### Request Payload Binding & Validation

Validating incoming JSON payloads with go-playground validator:

```go
package main

import (
	"net/http"
	"github.com/go-playground/validator/v10"
	"github.com/labstack/echo/v4"
)

type CustomValidator struct {
	validator *validator.Validate
}

func (cv *CustomValidator) Validate(i interface{}) error {
	return cv.validator.Struct(i)
}

type CreateUserRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Age      int    `json:"age" validate:"gte=18,lte=120"`
}

func createUser(c echo.Context) error {
	req := new(CreateUserRequest)
	if err := c.Bind(req); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	if err := c.Validate(req); err != nil {
		return echo.NewHTTPError(http.StatusUnprocessableEntity, err.Error())
	}
	return c.JSON(http.StatusCreated, req)
}
```

### Centralized Custom HTTP Error Handler

Uniform error responses conforming to RFC 7807:

```go
func customHTTPErrorHandler(err error, c echo.Context) {
	code := http.StatusInternalServerError
	msg := "Internal Server Error"

	if he, ok := err.(*echo.HTTPError); ok {
		code = he.Code
		msg = he.Message.(string)
	}

	if !c.Response().Committed {
		_ = c.JSON(code, map[string]interface{}{
			"error":  true,
			"code":   code,
			"detail": msg,
		})
	}
}
```

## Common Patterns

### Custom Context and JWT Authentication Middleware

**Problem**: Extracting authenticated user identity into request context safely across handlers.

**Solution**:
Create custom middleware and access via `c.Get`:

```go
func AuthMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		token := c.Request().Header.Get("Authorization")
		if token != "Bearer valid-token" {
			return echo.NewHTTPError(http.StatusUnauthorized, "Invalid token")
		}
		c.Set("userId", 42)
		return next(c)
	}
}

// In handler: userId := c.Get("userId").(int)
```

## Best Practices

**Do**:

- Attach `middleware.Recover()` at the root router to prevent unhandled panics from crashing the HTTP server.
- Use `echo.Context.Request().Context()` to propagate cancellation and deadlines to database operations.
- Configure timeouts (`ReadTimeout`, `WriteTimeout`, `IdleTimeout`) on the underlying `http.Server`.
- Implement a custom validator and assign it to `e.Validator`.

**Don't**:

- Store request-scoped data in global variables; store them in `c.Set(key, value)`.
- Use standard `log.Print` in handlers; use `c.Logger()` or structured `slog`.
- Write to `c.Response().Writer` after returning an error from a handler.

## Troubleshooting

| Error                                                          | Cause                                                          | Solution                                                                   |
| :------------------------------------------------------------- | :------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `code=400, message=Syntax error: unexpected end of JSON input` | Empty request body passed to `c.Bind(&struct)`.                | Verify request body contains valid JSON before binding.                    |
| `http: superfluous response.WriteHeader call`                  | Calling `c.JSON()` or `c.String()` twice in same handler flow. | Return immediately upon rendering response: `return c.JSON(...)`.          |
| `routing conflict: ... has conflicting route with ...`         | Overlapping route definitions with wildcard/param matchers.    | Adjust route paths or separate route groups to remove parameter ambiguity. |

## References

- [Echo Documentation](https://echo.labstack.com/)
