---
name: rider
description: Expert JetBrains Rider assistance covering .NET/C# cross-platform development, Unity/Unreal game development, dotTrace profiling, and ReSharper code analysis. Use when configuring Rider solutions, debugging ASP.NET Core apps, analyzing memory leaks, or developing Unity games.
---

# Rider

Rider is JetBrains' .NET IDE. It is faster than Visual Studio 2022 in many cases and runs on Mac/Linux. It works great for **Unity** and **Unreal Engine**.

## When to Use

- **Cross-Platform .NET / C# Development**: Building high-performance ASP.NET Core web APIs, Blazor, and microservices on macOS, Linux, and Windows.
- **Game Engine Engineering (Unity & Unreal)**: Profiling, debugging C# scripts, and integrating shaders with deep engine hooks.
- **ReSharper-Powered Refactoring**: Performing enterprise-scale code migrations, nullability analysis, and LINQ optimization.
- **dotTrace & dotMemory Profiling**: Identifying memory leaks, GC pressure, and multi-threaded execution locks.

## Quick Start

### 1. Open Solution & Run

```bash
# Open solution via Rider CLI
rider MyProject.sln
```

### 2. Configure launchSettings.json

```json
{
  "profiles": {
    "Development": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": true,
      "applicationUrl": "https://localhost:7001;http://localhost:5001",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```

- Select profile in top toolbar and press `Ctrl + F5` (Run) or `F5` (Debug).

## Core Concepts

### Modern .NET Solution & EditorConfig

Configuring code formatting, nullability, and C# 12/13 conventions via `.editorconfig`:

```ini
# .editorconfig
root = true

[*.cs]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8

# C# Formatting Rules
csharp_new_line_before_open_brace = all
csharp_indent_braces = false
csharp_prefer_braces = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
dotnet_style_null_propagation = true:suggestion
dotnet_naming_rule.async_methods_must_end_with_async.severity = warning

# Code Quality & Nullable Inspections
dotnet_diagnostic.CS8600.severity = error # Converting null literal to non-nullable
dotnet_diagnostic.CS8602.severity = error # Dereference of a possibly null reference
dotnet_diagnostic.CA1822.severity = warning # Member can be made static
```

### High-Speed ASP.NET Core Fast Endpoints Configuration

Building modern, high-throughput C# microservices in Rider:

```csharp
using FastEndpoints;

public class CreateUserRequest
{
    public required string Email { get; init; }
    public required string Name { get; init; }
}

public class CreateUserResponse
{
    public required Guid Id { get; init; }
    public required string Status { get; init; }
}

public class CreateUserEndpoint : Endpoint<CreateUserRequest, CreateUserResponse>
{
    public override void Configure()
    {
        Post("/api/v1/users");
        AllowAnonymous();
    }

    public override async Task HandleAsync(CreateUserRequest req, CancellationToken ct)
    {
        var userId = Guid.NewGuid();
        // Business logic execution
        await SendCreatedAtAsync<GetUserEndpoint>(
            new { id = userId },
            new CreateUserResponse { Id = userId, Status = "Created" },
            cancellation: ct
        );
    }
}
```

### dotMemory Profiling & Memory Leak Detection

- Attach Rider dotMemory profiler to a running .NET process (`Run -> Profile with dotMemory`).
- Take snapshot before and after workload execution.
- Compare memory generations, pinned handles, and investigate retention paths for undisposed event handlers and singletons.

## Common Patterns

#Launch Settings Profile (.run/launchSettings.json)
**Problem**: Standardize ASP.NET Core environment variables across developers.  
**Solution**: Configure launch profiles in `launchSettings.json`.

```json
{
  "profiles": {
    "LocalDevelopment": {
      "commandName": "Project",
      "launchBrowser": false,
      "applicationUrl": "https://localhost:5001;http://localhost:5000",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development",
        "DOTNET_USE_POLLING_FILE_WATCHER": "1"
      }
    }
  }
}
```

## Best Practices (2026)

- **Do** enable Nullable Reference Types (`<Nullable>enable</Nullable>`) across all project files.
- **Do** utilize Rider's integrated **dotMemory** and **dotTrace** for profiling GC allocations and high-CPU methods.
- **Do** use `Ctrl + Shift + R` (Refactor This) for safe signature modifications, interface extraction, and inline methods.
- **Do** enable Solution-Wide Analysis to catch compilation and architectural rule violations before committing.
- **Don't** check in `.idea/` workspace files or personal launch settings into Git.
- **Don't** ignore ReSharper yellow and red inspection warnings; resolve them continuously.
- **Don't** run synchronous blocking calls (`.Result`, `.Wait()`) on asynchronous Task operations; use `await`.

## Troubleshooting

| Error / Symptom                                    | Cause                                                                              | Solution                                                                                                  |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Rider cannot find target .NET SDK                  | Multiple SDKs or wrong architecture installed (e.g. ARM64 vs x64 on Apple Silicon) | Set custom SDK path in **Settings > Build, Execution, Deployment > Toolset and Build**.                   |
| Unity breakpoints not hitting                      | Rider plugin in Unity outdated or debugger attached to wrong process               | Check Unity Package Manager for `com.unity.ide.rider`; ensure editor is attached to Unity Editor process. |
| High memory consumption on multi-project solutions | Solution-wide analysis inspecting hundreds of projects simultaneously              | Lower inspection severity in **Settings > Editor > Inspection Settings** or pause Solution-Wide Analysis. |

## References

- [Rider Documentation](https://www.jetbrains.com/rider/documentation/)
