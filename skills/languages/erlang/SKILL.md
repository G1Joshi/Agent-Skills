---
name: erlang
description: Expert Erlang programming assistance covering BEAM virtual machine, actor concurrency, supervision trees, and OTP. Use when developing telecom systems, distributed databases, or messaging backbones.
---

# Erlang

Erlang powered WhatsApp and the telecom backbone. OTP 27 (2024) adds a **JSON module** and triple-quoted strings. It is the foundation of Elixir.

## When to Use

- **Nine-Nines High Availability Infrastructure**: Telecommunications, payment switching networks, and messaging systems requiring 99.9999999% uptime.
- **Massively Scalable Chat Systems (WhatsApp/ejabberd)**: Connecting millions of concurrent WebSocket and XMPP connections simultaneously.
- **Hot Code Swapping**: Upgrading running production systems and deploying bugfixes without stopping the server.
- **Low-Latency Distributed Clusters (OTP)**: Building distributed node clusters with built-in node discovery and heartbeats.

## Quick Start

```erlang
-module(hello).
-export([start/0]).

start() ->
    io:format("Hello from Erlang/OTP!~n").
```

## Core Concepts

#Open Telecom Platform (OTP) GenServer Behavior

Standardized generic client-server framework managing state, calls, and asynchronous casts:

```erlang
-module(counter_server).
-behaviour(gen_server).

-export([start_link/0, increment/0, get_count/0]).
-export([init/1, handle_call/3, handle_cast/2, terminate/2]).

start_link() -> gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).
increment()  -> gen_server:cast(?MODULE, inc).
get_count()  -> gen_server:call(?MODULE, get).

init([]) -> {ok, 0}.

handle_call(get, _From, Count) -> {reply, Count, Count}.
handle_cast(inc, Count)        -> {noreply, Count + 1}.
terminate(_Reason, _State)    -> ok.
```

#Pattern Matching Function Clauses

Functions declare multiple clauses matching input parameters structurally:

```erlang
-module(finance).
-export([tax/2]).

tax(Amount, {state, "CA"}) -> Amount * 0.0825;
tax(Amount, {state, "NY"}) -> Amount * 0.08875;
tax(Amount, {state, _Other}) -> Amount * 0.05.
```

#Hot Code Upgrades

Reloads module code live in memory while preserving active process state:

```erlang
% Compile and reload module in running Erlang VM
c(my_worker).
```

## Common Patterns

### Simple Actor Message Passing Loop

**Problem**: Managing asynchronous message queues and state without threads and mutexes.

**Solution**:
Use tail-recursive receive loops:

```erlang
-module(actor_counter).
-export([loop/1, start/0]).

start() ->
    spawn(fun() -> loop(0) end).

loop(Count) ->
    receive
        {increment, N} ->
            loop(Count + N);
        {get, Sender} ->
            Sender ! {current_count, Count},
            loop(Count);
        stop ->
            ok
    end.
```

## Best Practices (2026)

**Do**:

- **Adhere Strictly to OTP Principles**: Build applications around standard OTP behaviors (`gen_server`, `gen_statem`, `supervisor`).
- **Use Erlang Term Storage (ETS) for Shared Cache**: Leverage ETS tables for high-concurrency in-memory read lookups across processes.
- **Run Dialyzer for Static Type Analysis**: Add `-spec` type specifications to all public functions and run Dialyzer in CI.
- **Monitor BEAM Metrics via Telemetry**: Track process count, reductions, and scheduler utilization.

**Don't**:

- **Don't register thousands of named processes**: Atom tables are global and un-garbage-collected; dynamic atoms risk crashing the VM.
- **Don't use defensive try/catch everywhere**: Let processes crash on unexpected errors; let supervisors reset them to known good state.
- **Don't block schedulers with non-yielding C-NIFs**: Keep C Native Implemented Functions (NIFs) under 1ms or use dirty schedulers.

## Troubleshooting

| Error                                          | Cause                                                               | Solution                                                                          |
| :--------------------------------------------- | :------------------------------------------------------------------ | :-------------------------------------------------------------------------------- |
| `{badmatch, Value}`                            | Pattern matching failed on `=` or function argument.                | Verify return structure and provide clauses for all expected outcomes.            |
| `noproc: process not alive`                    | Sending a message or RPC call to a process PID that already exited. | Verify supervisor restart strategies and link/monitor processes with `monitor/2`. |
| `function_clause: no function clause matching` | Invoking function with arguments that don't match any head clause.  | Check argument types, arity, and guard conditions.                                |

## References

- [Erlang.org](https://www.erlang.org/)
