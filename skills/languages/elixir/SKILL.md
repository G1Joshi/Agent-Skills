---
name: elixir
description: Expert Elixir programming assistance covering pattern matching, GenServer, OTP supervisors, and Phoenix channels. Use when building highly concurrent, distributed, fault-tolerant web and backend systems.
---

# Elixir

A dynamic, functional language designed for building scalable and maintainable applications. Running on the Erlang VM (BEAM).

## When to Use

- **High-Concurrency Distributed Systems**: Running millions of simultaneous processes on the battle-tested BEAM (Erlang VM).
- **Real-Time Web Applications (Phoenix LiveView)**: Building dynamic, interactive web interfaces with zero client-side JavaScript.
- **Fault-Tolerant Microservices & Telecommunications**: Applications that self-heal from failures using supervision trees and "let it crash" philosophy.
- **IoT & Embedded Systems (Nerves)**: Building robust embedded firmware for IoT gateways and industrial controllers.

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

### Lightweight Actor Processes & Message Passing

Processes on the BEAM are isolated, consume only ~2KB of memory, and communicate exclusively via asynchronous message passing:

```elixir
# Spawn an isolated actor process
pid = spawn(fn ->
  receive do
    {:ping, sender_pid} ->
      send(sender_pid, :pong)
  end
end)

# Send message and await response
send(pid, {:ping, self()})
receive do
  :pong -> IO.puts("Received pong response!")
after
  1000 -> IO.puts("Timeout waiting for response")
end
```

### Pattern Matching & Pipe Operator (`|>`)

Pipelines data transformations through readable function compositions:

```elixir
def process_order(payload) do
  payload
  |> Jason.decode!()
  |> validate_order()
  |> calculate_tax()
  |> persist_to_database()
end
```

### Supervision Trees & Fault Tolerance

Supervisors monitor worker processes and restart them automatically when unhandled exceptions occur:

```elixir
defmodule CoreApp.Supervisor do
  use Supervisor

  def start_link(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      {CoreApp.DatabaseWorker, []},
      {CoreApp.EventConsumer, []}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end
```

## Common Patterns

### State Management with GenServer

**Problem**: Maintaining state and handling concurrent messages safely without shared memory locks.

**Solution**:
Implement a supervised GenServer actor:

```elixir
defmodule CounterServer do
  use GenServer

  # Client API
  def start_link(default \\ 0) do
    GenServer.start_link(__MODULE__, default, name: __MODULE__)
  end

  def increment do
    GenServer.cast(__MODULE__, :inc)
  end

  def get_count do
    GenServer.call(__MODULE__, :get)
  end

  # Server Callbacks
  @impl true
  def init(count), do: {:ok, count}

  @impl true
  def handle_cast(:inc, state), do: {:noreply, state + 1}

  @impl true
  def handle_call(:get, _from, state), do: {:reply, state, state}
end
```

## Best Practices

**Do**:

- Embrace Phoenix LiveView: Build rich real-time SPAs using server-rendered LiveView; eliminate client API maintenance.
- Let It Crash: Do not defensively catch every exception; let crashed processes be cleanly restarted by supervisors.
- Use Ecto Changesets for Data Validation: Validate incoming parameters and domain constraints using composable changesets.
- Structure Concurrency with GenServer & Task: Use standard OTP behaviors (`GenServer`, `Task`, `Agent`) rather than raw `spawn`.

**Don't**:

- Use GenServers as simple data storage: Storing large volumes of data in GenServer state creates performance bottlenecks; use ETS.
- Perform blocking work inside GenServer `handle_call`: Delegate slow tasks to separate `Task.async` workers.
- Mutate state across processes: State is strictly immutable; communicate via messages and return new state.

## Troubleshooting

| Error                                               | Cause                                                                              | Solution                                                                       |
| :-------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `MatchError: no match of right hand side value`     | Pattern match failed on expected tuple (e.g. `{:ok, val}` got `{:error, reason}`). | Add fallback clause or use `with` statement for multi-step pattern matching.   |
| `GenServer.call timeout after 5000ms`               | Target process deadlocked, busy, or crashed during call.                           | Inspect GenServer callback work and increase timeout parameter if intentional. |
| `UndefinedFunctionError: function ... is undefined` | Module not compiled, typo in function name, or wrong arity.                        | Run `mix compile` and check module exports with `module_info(:exports)`.       |

## References

- [Elixir-Lang](https://elixir-lang.org/)
- [Phoenix Framework](https://www.phoenixframework.org/)
