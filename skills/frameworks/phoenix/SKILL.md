---
name: phoenix
description: Expert Phoenix assistance covering Elixir web development, LiveView real-time reactive UIs, Ecto queries, and Channels. Use when building high-concurrency real-time web applications with minimal JavaScript.
---

# Phoenix

Phoenix (Elixir) provides real-time scalability (millions of connections). v1.7 + **LiveView** allows building rich SPAs without writing JavaScript.

## When to Use

- **Real-Time Interactive Web Applications**: Real-time dashboards, multiplayer games, and collaboration tools with LiveView.
- **High-Concurrency Distributed Backends**: Leveraging Erlang/Elixir BEAM VM for fault-tolerant microservices.
- **Scalable WebSocket & Channel Architectures**: Millions of persistent connections with minimal memory per process.
- **Maintainable Functional Web Development**: Clean separation with Ecto schemas, contexts, and Plugs.

## Quick Start

```elixir
defmodule MyAppWeb.PageController do
  use MyAppWeb, :controller

  def home(conn, _params) do
    render(conn, :home, layout: false)
  end
end

# In router.ex:
# scope "/", MyAppWeb do
#   pipe_through :browser
#   get "/", PageController, :home
# end
```

## Core Concepts

### Phoenix LiveView: Server-Driven Interactivity

Real-time UI state management over WebSockets without JavaScript client state:

```elixir
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view

  def mount(_params, _session, socket) do
    {:ok, assign(socket, count: 0)}
  end

  def handle_event("increment", _params, socket) do
    {:noreply, update(socket, :count, &(&1 + 1))}
  end

  def render(assigns) do
    ~H[
    <div class="counter-box">
      <h2 class="text-xl">Count: <%= @count %></h2>
      <button phx-click="increment" class="bg-blue-500 text-white px-4 py-2 rounded">
        Increment
      </button>
    </div>
    ]
  end
end
```

### Ecto Contexts & Composability

Decoupled business logic and transactional database access:

```elixir
defmodule MyApp.Accounts do
  import Ecto.Query, warn: false
  alias MyApp.Repo
  alias MyApp.Accounts.User

  def list_active_users do
    from(u in User, where: u.is_active == true, order_by: [desc: u.inserted_at])
    |> Repo.all()
  end

  def create_user(attrs \\ %{}) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end
end
```

### Phoenix Channels: Low-Latency Pub/Sub

Real-time broadcasting across connected clients:

```elixir
defmodule MyAppWeb.RoomChannel do
  use MyAppWeb, :channel

  def join("room:lobby", _payload, socket) do
    {:ok, socket}
  end

  def handle_in("new_msg", %{"body" => body}, socket) do
    broadcast!(socket, "new_msg", %{body: body, user: socket.assigns.user_id})
    {:reply, :ok, socket}
  end
end
```

## Common Patterns

### Real-Time LiveView Counter with PubSub Broadcasts

**Problem**: Synchronizing live state changes across multiple concurrent browser tabs.

**Solution**:
Use Phoenix LiveView with PubSub broadcasting:

```elixir
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view

  def mount(_params, _session, socket) do
    if connected?(socket), do: Phoenix.PubSub.subscribe(MyApp.PubSub, "counter")
    {:ok, assign(socket, count: 0)}
  end

  def handle_event("inc", _params, socket) do
    new_count = socket.assigns.count + 1
    Phoenix.PubSub.broadcast(MyApp.PubSub, "counter", {:count_updated, new_count})
    {:noreply, assign(socket, count: new_count)}
  end

  def handle_info({:count_updated, count}, socket) do
    {:noreply, assign(socket, count: count)}
  end
end
```

## Best Practices

**Do**:

- Target Phoenix 1.7+ with verified routes (`~p"/users"`) and HEEx functional components.
- Structure domain boundaries using Phoenix Contexts rather than exposing Ecto queries in controllers.
- Use LiveView streams (`stream/3`) for large collections to minimize memory usage on both client and server.
- Use Ecto Multi (`Ecto.Multi`) for atomic multi-table transactional workflows.

**Don't**:

- Store large binary data or huge collections in LiveView socket assigns; use temporary assigns or streams.
- Make blocking third-party HTTP calls directly in LiveView processes without wrapping in `Task`.
- Bypass Ecto changesets for user input validation.

## Troubleshooting

| Error                                                | Cause                                                                      | Solution                                                         |
| :--------------------------------------------------- | :------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `(Ecto.NoResultsError) expected at least one result` | `Repo.get!` or `Repo.one!` returned nil for query.                         | Use non-bang variant `Repo.get` and handle nil safely.           |
| `phx-socket closed / reconnecting in LiveView`       | LiveView process crashed due to unhandled `handle_info` or `handle_event`. | Inspect Elixir crash stack trace in `iex -S mix phx.server`.     |
| `CompileError: undefined function MyAppWeb...`       | Module name typo or Phoenix view helper not included.                      | Run `mix compile` and check module namespace in `my_app_web.ex`. |

## References

- [Phoenix Documentation](https://www.phoenixframework.org/)
