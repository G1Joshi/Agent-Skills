---
name: clojure
description: Clojure functional programming on the JVM with immutable data. Use for .clj files.
---

# Clojure

A Lisp hosted on the JVM (and JS via ClojureScript) with a focus on immutability.

## When to Use

- Data processing
- Concurrency (Software Transactional Memory)
- Web development
- JVM interop needed

## Quick Start

```clojure
(println "Hello, World!")

(defn square [x]
  (* x x))

(map square [1 2 3]) ; (1 4 9)
```

## Core Concepts

### Persistent Data Structures

Immutable lists, vectors, maps, and sets that structurally share data to be efficient.

### REPL Driven Development

Writing code interactively in a Running Eval-Print Loop.

### Macros

Code that takes code as input and returns code.

## Best Practices

**Do**:

- Use the REPL
- Use threading macros `->` and `->>` to make code readable
- Leverage JVM libraries

**Don't**:

- Use atoms/agents/refs unless you need mutable state
- Write deeply nested parentheses (use structural editing)

## References

- [Clojure.org](https://clojure.org/)
- [ClojureDocs](https://clojuredocs.org/)
