---
name: blazor
description: Expert Blazor assistance covering WebAssembly, Server-Side Blazor, Razor components, and C# browser interactivity. Use when building interactive web UIs using C# instead of JavaScript.
---

# Blazor

Blazor allows writing web UIs in **C#** instead of JavaScript. .NET 9 (2024/2025) brings unified rendering modes (Server, WebAssembly, Auto).

## When to Use

- **Interactive Full-Stack Web Apps in C#**: Building rich browser UIs without writing separate JavaScript codebases.
- **Blazor Web App Unified Model (.NET 8/9)**: Mixing Server, WebAssembly, and Static Server-Side Rendering per component.
- **Enterprise Internal Dashboards**: Utilizing high-productivity component libraries (MudBlazor, Fluent UI Blazor).
- **Offline Progressive Web Apps**: Compiling C# directly into WebAssembly for client-side offline execution.

## Quick Start

```razor
@page "/counter"
@rendermode InteractiveServer

<PageTitle>Counter</PageTitle>

<h1>Counter</h1>

<p role="status">Current count: @currentCount</p>

<button class="btn btn-primary" @onclick="IncrementCount">Click me</button>

@code {
    private int currentCount = 0;

    private void IncrementCount()
    {
        currentCount++;
    }
}
```

## Core Concepts

#Render Modes & Reactive Parameters

Declaring component interactivity per page or component:

```razor
@page "/counter"
@rendermode InteractiveServer

<PageTitle>Counter</PageTitle>

<div class="card p-4">
    <h3>Current count: @currentCount</h3>
    <button class="btn btn-primary" @onclick="IncrementCount">Click me</button>
</div>

@code {
    private int currentCount = 0;

    [Parameter]
    public int IncrementStep { get; set; } = 1;

    private void IncrementCount()
    {
        currentCount += IncrementStep;
    }
}
```

#Two-Way Binding & EventCallback

Passing events and state between parent and child components:

```razor
<!-- ChildComponent.razor -->
<div class="search-box">
    <input value="@SearchTerm" @oninput="OnInputChanged" placeholder="Search..." />
</div>

@code {
    [Parameter]
    public string SearchTerm { get; set; } = string.Empty;

    [Parameter]
    public EventCallback<string> SearchTermChanged { get; set; }

    private async Task OnInputChanged(ChangeEventArgs e)
    {
        var newValue = e.Value?.ToString() ?? string.Empty;
        await SearchTermChanged.InvokeAsync(newValue);
    }
}
```

#Dependency Injection & Cascading Authentication State

Accessing user security context in Blazor components:

```razor
@inject NavigationManager Navigation
@inject IOrderService OrderService

<AuthorizeView>
    <Authorized>
        <p>Welcome, @context.User.Identity?.Name!</p>
        <button class="btn btn-success" @onclick="LoadOrders">Fetch Orders</button>
    </Authorized>
    <NotAuthorized>
        <p>Please log in to view your orders.</p>
        <a href="/login">Login</a>
    </NotAuthorized>
</AuthorizeView>

@code {
    private async Task LoadOrders()
    {
        var orders = await OrderService.GetUserOrdersAsync();
    }
}
```

## Common Patterns

### Two-Way Component Parameter Binding

**Problem**: Passing state down to child components while bubbling state modifications back up cleanly.

**Solution**:
Use `@bind-Value` and EventCallback conventions:

```razor
<!-- ChildComponent.razor -->
<input value="@Value" @oninput="OnInputChanged" />

@code {
    [Parameter] public string Value { get; set; } = "";
    [Parameter] public EventCallback<string> ValueChanged { get; set; }

    private async Task OnInputChanged(ChangeEventArgs e)
    {
        await ValueChanged.InvokeAsync(e.Value?.ToString());
    }
}

<!-- ParentComponent.razor: <ChildComponent @bind-Value="searchTerm" /> -->
```

## Best Practices (2026)

- **Do** target the .NET 8/9 Blazor Web App unified project template with auto render modes (`InteractiveAuto`).
- **Do** implement `IDisposable` or `IAsyncDisposable` on components subscribing to C# events to avoid memory leaks.
- **Do** use `Virtualize<TItem>` for rendering large lists to render only elements within the viewport.
- **Do** keep state centralized in injected scoped services rather than sprawling across UI components.
- **Don't** use synchronous blocking I/O calls (`.Result`) in component methods; use `async/await`.
- **Don't** pass large binary data over Blazor Server SignalR circuits; use dedicated streaming API endpoints.
- **Don't** trigger unnecessary `StateHasChanged()` calls if standard event callbacks already trigger re-rendering.

## Troubleshooting

| Error                                                                | Cause                                                                | Solution                                                                       |
| :------------------------------------------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `InvalidOperationException: Cannot provide a value for property ...` | Missing `@inject` directive or service not registered in Program.cs. | Register service in `builder.Services.AddScoped<MyService>()`.                 |
| `Blazor circuit disconnected / reconnecting loop`                    | Unhandled exception crashed the SignalR circuit on the server.       | Wrap event handlers in try/catch and inspect server console logs.              |
| `WASM: Out of memory during large data fetch`                        | Large response payload deserialization exceeding WASM memory limits. | Paginate API responses or use streaming deserialization with System.Text.Json. |

## References

- [Blazor Documentation](https://dotnet.microsoft.com/apps/aspnet/web-apps/blazor)
