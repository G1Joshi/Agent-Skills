---
name: csharp
description: Expert C# and .NET assistance covering LINQ, async/await patterns, pattern matching, records, Entity Framework Core, and ASP.NET Core web services. Use when writing idiomatic C#, designing .NET enterprise backends, building cross-platform services, or optimizing memory with span/memory types.
---

# C#

Modern C# development with .NET 8+, async patterns, and Entity Framework.

## When to Use

- **Enterprise Web Backends & Microservices**: Building high-throughput ASP.NET Core web APIs and gRPC microservices on modern .NET 8/9.
- **Cross-Platform Mobile & Desktop (MAUI)**: Compiling native iOS, Android, macOS, and Windows applications from a single C# codebase.
- **Cloud-Native AWS & Azure Infrastructure**: Deploying scalable serverless functions, containerized workers, and event-driven apps.
- **Game Development with Unity / Godot**: Developing gameplay logic, physics, and state machines in leading game engines.

## Quick Start

```csharp
public record User(string Id, string Name, string Email);

public class UserService
{
    public async Task<User?> GetUserAsync(string id)
    {
        return await _repository.FindByIdAsync(id);
    }
}
```

## Core Concepts

#Records & Pattern Matching (C# 12/13)

Immutable data structures with value equality and expressive switch expressions:

```csharp
// Positional Record with built-in value equality
public record Order(string Id, decimal Amount, string Status);

public static class OrderClassifier
{
    public static string Evaluate(Order order) => order switch
    {
        { Status: "PAID", Amount: > 1000 } => "High-Value Order",
        { Status: "PAID" }                 => "Standard Order",
        { Status: "CANCELLED" }            => "Void Order",
        _                                  => "Pending Review"
    };
}
```

#Memory Optimization with `Span<T>` and `ReadOnlySpan<T>`

Allocates and slices continuous memory buffers on the stack without heap GC allocations:

```csharp
public static bool TryParseYear(ReadOnlySpan<char> dateSpan, out int year)
{
    // Slice without allocating new sub-strings
    ReadOnlySpan<char> yearSpan = dateSpan.Slice(0, 4);
    return int.TryParse(yearSpan, out year);
}
```

#Async / Await with `ValueTask`

Efficient asynchronous programming minimizing task object allocations on hot paths:

```csharp
public async ValueTask<UserProfile> GetUserProfileAsync(string userId)
{
    if (_cache.TryGetValue(userId, out var cached))
        return cached; // Synchronous return allocates zero task objects

    return await _repository.FetchFromDatabaseAsync(userId);
}
```

## Common Patterns

### LINQ

```csharp
// Query syntax
var adults = from user in users
             where user.Age >= 18
             orderby user.Name
             select user;

// Method syntax (preferred)
var result = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => new UserDto(u.Id, u.Name))
    .ToList();

// Grouping
var byCountry = users
    .GroupBy(u => u.Country)
    .ToDictionary(g => g.Key, g => g.ToList());
```

### Pattern Matching

```csharp
string GetStatus(object obj) => obj switch
{
    User { IsActive: true } => "Active user",
    User { IsActive: false } => "Inactive user",
    null => "No data",
    _ => "Unknown"
};

// List patterns
if (numbers is [var first, _, var last])
{
    Console.WriteLine($"First: {first}, Last: {last}");
}
```

## Best Practices (2026)

**Do**:

- **Enable Nullable Reference Types (`<Nullable>enable</Nullable>`)**: Catch null reference exceptions at compile time across the codebase.
- **Use Dependency Injection & Options Pattern**: Inject strongly-typed configurations via `IOptions<T>` and constructor injection.
- **Use `ValueTask<T>` on Frequently Cached Code Paths**: Reduce GC allocations by returning `ValueTask` when operations often complete synchronously.
- **Leverage Native AOT Compilation**: Compile .NET applications to native machine code (`PublishAot=true`) for sub-10ms startup and tiny memory footprints.

**Don't**:

- **Don't block async code with `.Result` or `.Wait()`**: Synchronous blocking on asynchronous tasks causes immediate thread pool deadlocks.
- **Don't use mutable shared singletons without thread safety**: Use `ConcurrentDictionary` or proper synchronization primitives.
- **Don't instantiate `HttpClient` per request**: Use `IHttpClientFactory` to prevent socket exhaustion.

## Troubleshooting

| Error                     | Cause                   | Solution                    |
| ------------------------- | ----------------------- | --------------------------- |
| `NullReferenceException`  | Accessing null          | Enable nullable, use `?.`   |
| `ObjectDisposedException` | Using disposed resource | Check lifetime, use `using` |
| `TaskCanceledException`   | Operation cancelled     | Handle or propagate         |

## References

- [Microsoft .NET Docs](https://docs.microsoft.com/dotnet/)
- [C# Programming Guide](https://docs.microsoft.com/dotnet/csharp/)
