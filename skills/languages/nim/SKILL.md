---
name: nim
description: Expert Nim systems programming assistance covering Python-like syntax, C/C++ compilation, macros, and ARC memory management. Use when writing high-performance CLI tools, games, or systems software.
---

# Nim

Nim is a statically typed systems programming language offering Python-like expressive syntax, compile-time metaprogramming, and deterministic ARC/ORC memory management compiling to C, C++, and JavaScript.

## When to Use

- **High-Performance Compiled Systems**: Producing tiny, dependency-free C/C++ or JavaScript output with Python-like syntax elegance.
- **Memory-Constrained Embedded Systems**: Running on microcontrollers with the deterministic ARC/ORC memory management model.
- **Cross-Compilation Simplicity**: Cross-compiling to Windows, Linux, macOS, and WebAssembly with a single compiler flag.
- **Powerful AST Compile-Time Metaprogramming**: Writing complex macros that generate and inspect code at compile time.

## Quick Start

```nim
type
  Person = object
    name: string
    age: int

proc greet(p: Person) =
  echo "Hello, ", p.name, "! You are ", p.age, " years old."

let alice = Person(name: "Alice", age: 30)
greet(alice)
```

## Core Concepts

### Pythonic Indentation with C-Level Performance

Clean, readable syntax that compiles directly into optimized C/C++ code:

```nim
type
  Customer = object
    id: int
    name: string
    active: bool

proc calculateBonus(customer: Customer, spend: float): float =
  if customer.active:
    result = spend * 0.05
  else:
    result = 0.0

let vip = Customer(id: 415, name: "Alice", active: true)
echo "Bonus earned: $", calculateBonus(vip, 1500.0)
```

### ARC / ORC Deterministic Memory Management

Automatic Reference Counting with cycle detection (ORC) eliminates stop-the-world garbage collection pauses:

```bash
# Compile with modern deterministic ORC memory management
nim c --mm:orc -d:release main.nim
```

### Powerful Compile-Time Macro System

Manipulates the Abstract Syntax Tree (AST) directly during compilation:

```nim
import macros

macro debugLog(expr: untyped): untyped =
  let strExpr = expr.toStrLit
  quote do:
    echo "DEBUG: ", `strExpr`, " = ", `expr`

let x = 42
debugLog(x * 2) # Prints: DEBUG: x * 2 = 84
```

## Common Patterns

### Compile-Time Macro Code Generation

**Problem**: Repetitive boilerplate for serializing or validating domain objects.

**Solution**:
Use Nim's AST macros executed at compile time:

```nim
import macros

macro printVarNameAndValue*(v: untyped): untyped =
  result = newStmtList()
  result.add(newCall("echo", newLit(v.repr & " = "), v))

let score = 98
printVarNameAndValue(score) # Outputs: score = 98
```

## Best Practices

**Do**:

- Use `--mm:orc` by Default: Standardize on ARC/ORC memory management for deterministic, low-latency execution.
- Compile with `-d:release` or `-d:danger`: Enable optimizations and disable runtime assertions for maximum production speed.
- Leverage Method Chaining and UFCS: Use Uniform Function Call Syntax (`data.filter().map()`) for clean readable pipelines.
- Document Code with `nim doc`: Generate HTML API documentation directly from docstrings.

**Don't**:

- Use legacy `--mm:refc`: Deprecate the old mark-and-sweep GC; migrate to modern ORC.
- Write heavy macros when templates suffice: Use simple `template` expansions before reaching for complex AST `macro` code.
- Ignore compiler hints: Nim provides detailed compile-time diagnostics; address warnings before deploying.

## Troubleshooting

| Error                                                | Cause                                                     | Solution                                                                         |
| :--------------------------------------------------- | :-------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `Error: type mismatch: got <...> but expected <...>` | Strict static type mismatch.                              | Check types and use conversion procedures like `int()`, `float()`, or `$`.       |
| `Error: undeclared identifier`                       | Symbol referenced before declaration or missing `import`. | Ensure identifier is declared earlier or exported with `*` from imported module. |
| `SIGSEGV in C backend execution`                     | Unsafe pointer dereference or C interop memory violation. | Compile with `--mm:orc` and enable `--debugger:native` for debug traces.         |

## References

- [Nim Lang](https://nim-lang.org/)
