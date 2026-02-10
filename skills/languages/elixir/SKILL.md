---
name: elixir
description: Elixir functional programming with OTP, GenServer, and Phoenix. Use for .ex files.
---

# Elixir

A dynamic, functional language designed for building scalable and maintainable applications. Running on the Erlang VM (BEAM).

## When to Use

- High-concurrency applications
- Real-time systems (chat, gaming)
- Distributed systems that need fault tolerance
- Web development with Phoenix

## Quick Start

```elixir
IO.puts "Hello, World!"

list = [1, 2, 3]
doubled = Enum.map(list, fn x -> x * 2 end)

defmodule Math do
  def sum(a, b), do: a + b
end
```

## Core Concepts

### Processes

Elixir code runs inside lightweight processes (not OS threads) that are isolated and exchange information via messages.

```elixir
pid = spawn(fn ->
  receive do
    {:hello, msg} -> IO.puts "Got hello: #{msg}"
  end
end)

send(pid, {:hello, "world"})
```

### Pattern Matching

Used assignment and function dispatch.

```elixir
{a, b, c} = {:hello, "world", 42}
# a is :hello, b is "world", c is 42
```

### OTP (Open Telecom Platform)

A set of libraries and design principles for building fault-tolerant systems (Supervisors, GenServers).

## Best Practices

**Do**:

- Use the pipe operator `|>`
- Leverage pattern matching
- Design with "Let it crash" philosophy (Supervisors restart processes)

**Don't**:

- Use `if/else` excessively (use pattern matching or `case`)
- Mutate state (data is immutable)

## References

- [Elixir-Lang](https://elixir-lang.org/)
- [Phoenix Framework](https://www.phoenixframework.org/)
