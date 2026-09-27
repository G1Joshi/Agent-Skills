---
name: v
description: Expert V language (vlang) assistance covering fast compilation, memory safety, C interop, and concurrency. Use when writing fast lightweight binaries, web servers, or cross-platform utilities.
---

# V (Vlang)

V (2024 updates) focuses on **compilation speed** (1 million LOC/s) and safety (Autofree). It aims to be a modern C replacement with Go-like simplicity.

## When to Use

- **Lightweight, High-Speed Systems Programming**: Compiling native executables with C-equivalent performance and zero dependencies.
- **Rapid Cross-Platform Tooling & CLI Development**: Building standalone command-line utilities with instant compile times (< 1 second).
- **Clean Embedded & WebAssembly Applications**: Low-memory footprint services and game engines without garbage collection spikes.
- **Direct Seamless C Interop**: Calling existing C libraries directly without header generation or binding wrappers.

## Quick Start

```v
struct User {
    id   int
    name string
}

fn main() {
    users := [User{id: 1, name: 'Alice'}, User{id: 2, name: 'Bob'}]
    for u in users {
        println('User $u.id: $u.name')
    }
}
```

## Core Concepts

#Memory Management & Immutability by Default

V uses compile-time autofree memory management without garbage collection pauses:

```v
module main

import os

// Struct definition with explicit access controls
pub struct UserSession {
pub:
	username string
	user_id  int
pub mut:
	token    string
}

fn main() {
	// Variables are immutable by default
	user := UserSession{
		username: 'alice'
		user_id: 101
		token: 'tok-abc'
	}
	println('User: ${user.username}, ID: ${user.user_id}')
}
```

#Result & Option Types for Error Propagation

Handling missing values and errors explicitly without exceptions:

```v
module main

import os

struct Config {
	port int
	host string
}

fn parse_port(env_var string) !int {
	val := os.getenv(env_var)
	if val == '' {
		return error('Environment variable ${env_var} not found')
	}
	port := val.int()
	if port <= 0 || port > 65535 {
		return error('Port ${port} out of valid range (1-65535)')
	}
	return port
}

fn main() {
	port := parse_port('SERVER_PORT') or {
		eprintln('Failed to load port: ${err}')
		8080 // fallback default
	}
	println('Starting server on port ${port}')
}
```

#Concurrency with Coroutines & Channels

Lightweight thread spawning with built-in CSP channels:

```v
module main

import sync

fn worker(id int, ch chan int) {
	for i in 0 .. 3 {
		ch <- id * 10 + i
	}
}

fn main() {
	ch := chan int{cap: 10}

	// Spawn concurrent green threads with 'spawn' keyword
	spawn worker(1, ch)
	spawn worker(2, ch)

	for _ in 0 .. 6 {
		val := <-ch
		println('Received: ${val}')
	}
	ch.close()
}
```

## Common Patterns

### Result and Option Types for Robust Error Handling

**Problem**: Nil-pointer crashes and unhandled error states.

**Solution**:
Use V's built-in `?` Option and `!` Result return types:

```v
fn divide(a f64, b f64) !f64 {
    if b == 0.0 {
        return error('division by zero')
    }
    return a / b
}

fn main() {
    res := divide(10.0, 2.0) or {
        eprintln('Calculation failed: $err')
        return
    }
    println('Result: $res')
}
```

## Best Practices (2026)

- **Do** run `v fmt -w .` to enforce standard formatting across the entire codebase.
- **Do** use `v -prod` when building release binaries to enable aggressive compiler optimizations and stripping.
- **Do** handle all errors using `or { ... }` blocks rather than panicking on unhandled results.
- **Do** write unit tests directly alongside code with `fn test_*()` functions and execute them with `v test .`.
- **Don't** use global mutable variables; pass context structs and state objects explicitly.
- **Don't** disable autofree in production unless explicitly using an arena allocator for game loop allocations.
- **Don't** ignore compiler warnings; treat warnings as errors during CI builds.

## Troubleshooting

| Error                                 | Cause                                                            | Solution                                                       |
| :------------------------------------ | :--------------------------------------------------------------- | :------------------------------------------------------------- |
| `unhandled option / result`           | Function returning Option or Result called without `or { ... }`. | Handle error with `or { ... }` or propagate with `?`.          |
| `variable '...' is immutable`         | Attempting to reassign an immutable variable.                    | Declare variable with `mut`: `mut count := 0`.                 |
| `builder error: C compilation failed` | Missing C compiler (gcc or clang) in system PATH.                | Install gcc/clang and ensure it is available in terminal PATH. |

## References

- [V Lang](https://vlang.io/)
