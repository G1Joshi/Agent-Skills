---
name: csharp
description: C# programming for .NET, ASP.NET Core, LINQ, async patterns, and Entity Framework. Use for .cs files.
---

# C#

Modern C# development with .NET 8+, async patterns, and Entity Framework.

## When to Use

- Working with `.cs` files
- Building ASP.NET Core web APIs
- Unity game development
- Desktop apps with WPF/MAUI

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

### Records & Nullable

```csharp
// Records for immutable data
public record User(string Id, string Name, string Email)
{
    public string DisplayName => Name.ToUpperInvariant();
}

// With-expressions for copies
var updated = user with { Name = "New Name" };

// Nullable reference types
public User? FindUser(string id)
{
    return users.FirstOrDefault(u => u.Id == id);
}
```

### Async/Await

```csharp
public async Task<List<User>> GetUsersAsync()
{
    // Parallel async operations
    var tasks = ids.Select(id => GetUserAsync(id));
    var users = await Task.WhenAll(tasks);
    return users.ToList();
}

// Async streams
public async IAsyncEnumerable<User> StreamUsersAsync()
{
    await foreach (var user in _repository.GetAllAsync())
    {
        yield return user;
    }
}

// Cancellation
public async Task<User> GetUserAsync(string id, CancellationToken ct)
{
    return await _client.GetFromJsonAsync<User>($"/users/{id}", ct);
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

## Best Practices

**Do**:

- Use `record` for DTOs and value objects
- Enable nullable reference types
- Use async/await for I/O operations
- Use dependency injection

**Don't**:

- Block async code with `.Result` or `.Wait()`
- Ignore cancellation tokens
- Use `dynamic` when type is known
- Create God classes

## Troubleshooting

| Error                     | Cause                   | Solution                    |
| ------------------------- | ----------------------- | --------------------------- |
| `NullReferenceException`  | Accessing null          | Enable nullable, use `?.`   |
| `ObjectDisposedException` | Using disposed resource | Check lifetime, use `using` |
| `TaskCanceledException`   | Operation cancelled     | Handle or propagate         |

## References

- [Microsoft .NET Docs](https://docs.microsoft.com/dotnet/)
- [C# Programming Guide](https://docs.microsoft.com/dotnet/csharp/)
