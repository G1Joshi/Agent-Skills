---
name: blazor
description: Blazor .NET WebAssembly and Server framework. Use for C# frontend.
---

# Blazor

Blazor allows writing web UIs in **C#** instead of JavaScript. .NET 9 (2024/2025) brings unified rendering modes (Server, WebAssembly, Auto).

## When to Use

- **.NET Shops**: Sharing code (Models/DTOs) between Backend and Frontend.
- **Internal Apps**: Rapid development for enterprise tools.
- **WebAssembly**: Running compiled C# in the browser.

## Core Concepts

### Blazor Server

UI logic runs on server, updates sent via SignalR. Low latency, requires connection.

### Blazor WebAssembly

Runs client-side (DLLs downloaded). Offline support.

### Interactive Components

Razor syntax (`@code { ... }`) combining HTML and C#.

## Best Practices (2025)

**Do**:

- **Use `Auto` mode**: Load fast (Server), then switch to WASM (Client) in background.
- **Use `QuickGrid`**: High performance data grid component.
- **Use Component Libraries**: MudBlazor/Radzen for material UI.

**Don't**:

- **Don't block the UI thread**: Use `await` for long implementations.

## References

- [Blazor Documentation](https://dotnet.microsoft.com/apps/aspnet/web-apps/blazor)
