---
name: erlang
description: Erlang concurrent programming with OTP. Use for .erl files.
---

# Erlang

Erlang powered WhatsApp and the telecom backbone. OTP 27 (2024) adds a **JSON module** and triple-quoted strings. It is the foundation of Elixir.

## When to Use

- **99.9999999% Reliability**: Hot code reloading, supervision trees.
- **Massive Concurrency**: Lightweight processes (millions per node).
- **Distributed Systems**: Distributed Erlang nodes connect natively.

## Core Concepts

### OTP

Open Telecom Platform. Behaviors like `gen_server` (Generic Server).

### Let it Crash

Don't catch exceptions. Let the supervisor restart the process.

### Message Passing

`Pid ! Message`. No shared memory.

## Best Practices (2025)

**Do**:

- **Use `rebar3`**: The standard build tool.
- **Use `maybe`**: The new monadic-like flow control (enabled by default in 27).
- **Use `json`**: The new stdlib JSON parser (faster/safer).

**Don't**:

- **Don't optimize pre-maturely**: Profile first. Messages are copied.

## References

- [Erlang.org](https://www.erlang.org/)
