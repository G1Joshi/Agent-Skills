---
name: phoenix
description: Phoenix Elixir framework with LiveView for real-time. Use for Elixir apps.
---

# Phoenix

Phoenix (Elixir) provides real-time scalability (millions of connections). v1.7 + **LiveView** allows building rich SPAs without writing JavaScript.

## When to Use

- **Real-time**: Chat apps, live dashboards (Channels).
- **High Concurrency**: Leveraging the BEAM VM (Erlang).
- **Low JS**: LiveView handles the UI state on the server.

## Core Concepts

### LiveView

Server-rendered HTML that updates over WebSockets. "The server is the state source".

### Ecto

The database wrapper. Using `Changeset` for validation.

### PubSub

Built-in, distributed publish-subscribe system.

## Best Practices (2025)

**Do**:

- **Use Verified Routes**: `~p"/users/#{@user}"` ensures compile-time link safety.
- **Use Tailwind**: Default in 1.7.
- **Use Function Components**: HEEx templates with declarative assigns.

**Don't**:

- **Don't use SPA unless needed**: LiveView covers 95% of use cases.

## References

- [Phoenix Documentation](https://www.phoenixframework.org/)
