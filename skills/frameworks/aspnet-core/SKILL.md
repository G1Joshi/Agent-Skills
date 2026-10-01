---
name: aspnet-core
description: Expert ASP.NET Core assistance covering Minimal APIs, Controller routing, Entity Framework Core, middleware, and dependency injection. Use when building enterprise .NET backend APIs and cloud services.
---

# ASP.NET Core

Cross-platform, high-performance framework for building modern web apps.

## When to Use

- **High-Performance Enterprise Backends**: Developing mission-critical APIs, microservices, and gRPC services on .NET 8 / 9.
- **Cloud-Native Containerized Applications**: Microservices deployed to Kubernetes, Azure Container Apps, or AWS ECS.
- **Real-Time Bidirectional Communication**: Scalable WebSocket and SSE apps using SignalR.
- **Full-Stack C# Web Development**: Blazor Server, Blazor WebAssembly, and Minimal APIs with C# 13.

## Quick Start

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();
```

## Core Concepts

### Minimal APIs with Typed Results & OpenAPI

Lightweight, high-performance endpoint mapping with zero controller ceremony:

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddSingleton<IOrderRepository, InMemoryOrderRepository>();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.MapGet("/api/orders/{id:guid}", async (Guid id, IOrderRepository repo) =>
{
    var order = await repo.GetByIdAsync(id);
    return order is not null
        ? Results.Ok(order)
        : Results.NotFound(new { message = $"Order {id} not found" });
})
.WithName("GetOrderById")
.Produces<Order>(StatusCodes.Status200OK)
.Produces(StatusCodes.Status404NotFound);

app.Run();
```

### Dependency Injection, Options Pattern & Configuration

Strongly typed configuration with validation:

```csharp
public class DatabaseOptions
{
    public const string SectionName = "Database";
    public required string ConnectionString { get; set; }
    public int MaxPoolSize { get; set; } = 100;
}

// In Program.cs:
builder.Services.AddOptions<DatabaseOptions>()
    .BindConfiguration(DatabaseOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart();

// In Service:
public class OrderService(IOptions<DatabaseOptions> options, ILogger<OrderService> logger)
{
    private readonly DatabaseOptions _options = options.Value;
}
```

### Global Error Handling Middleware & Problem Details

Standardized RFC 7807 error responses:

```csharp
app.UseExceptionHandler(exceptionHandlerApp =>
{
    exceptionHandlerApp.Run(async context =>
    {
        var exceptionHandlerPathFeature = context.Features.Get<IExceptionHandlerPathFeature>();
        var exception = exceptionHandlerPathFeature?.Error;

        var problemDetails = new ProblemDetails
        {
            Status = StatusCodes.Status500InternalServerError,
            Title = "An unexpected error occurred",
            Detail = exception?.Message,
            Instance = context.Request.Path
        };

        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        context.Response.ContentType = "application/problem+json";
        await context.Response.WriteAsJsonAsync(problemDetails);
    });
});
```

## Common Patterns

### Minimal API Endpoint Group with Validation

**Problem**: Controller-heavy boilerplate for simple microservice CRUD endpoints.

**Solution**:
Use ASP.NET Core Minimal APIs with Route Groups:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var users = app.MapGroup("/api/users");

users.MapGet("/", async (AppDbContext db) =>
    await db.Users.AsNoTracking().ToListAsync());

users.MapPost("/", async (CreateUserDto dto, AppDbContext db) => {
    var user = new User { Name = dto.Name, Email = dto.Email };
    db.Users.Add(user);
    await db.SaveChangesAsync();
    return Results.Created($"/api/users/{user.Id}", user);
});

app.Run();
```

## Best Practices

**Do**:

- Use Minimal APIs for microservices to maximize throughput and minimize cold-start latency.
- Return `IResult` / `TypedResults` from endpoints for compile-time response verification.
- Use `IHttpClientFactory` with Polly resilience pipelines for external HTTP calls.
- Enable AOT (Ahead-of-Time) compilation (`PublishAot=true`) for microservices to slash memory footprint.

**Don't**:

- Call `.Result` or `.Wait()` on async Tasks; always use `await` to prevent thread pool starvation.
- Register transient services in singletons without scoping via `IServiceScopeFactory`.
- Log sensitive credentials or PII; configure logging sanitization filters.

## Troubleshooting

| Error                                                                  | Cause                                                                | Solution                                                                     |
| :--------------------------------------------------------------------- | :------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `InvalidOperationException: Unable to resolve service for type ...`    | Service not registered in DI container.                              | Register service in `builder.Services.AddScoped<IService, Service>()`.       |
| `System.Text.Json.JsonException: A possible object cycle was detected` | Circular reference in Entity Framework navigation properties.        | Configure `ReferenceHandler.IgnoreCycles` in JSON options or return DTOs.    |
| `HTTP 500.30 - ANCM In-Process Start Failure`                          | Startup exception during application bootstrapping in IIS / Kestrel. | Inspect `stdoutLogEnabled="true"` in web.config or review event viewer logs. |

## References

- [ASP.NET Core Docs](https://learn.microsoft.com/en-us/aspnet/core/)
