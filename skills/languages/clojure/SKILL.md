---
name: clojure
description: Expert Clojure programming assistance covering immutable data structures, macros, software transactional memory (STM), and REPL workflows. Use when building concurrent functional systems or data transformation pipelines.
---

# Clojure

A Lisp hosted on the JVM (and JS via ClojureScript) with a focus on immutability.

## When to Use

- **Functional Programming on the JVM**: Leveraging immutable data structures, pure functions, and the vast Java library ecosystem.
- **Data-Driven & Event-Sourced Systems**: Processing complex financial, logistics, and transactional data structures effortlessly.
- **Full-Stack Clojure / ClojureScript**: Sharing code, validation schemas (Malli/Spec), and business models between backend and browser.
- **Interactive REPL-Driven Development**: Iterating and hot-reloading code live in running production-like JVM processes.

## Quick Start

```clojure
(println "Hello, World!")

(defn square [x]
  (* x x))

(map square [1 2 3]) ; (1 4 9)
```

## Core Concepts

### Persistent Immutable Data Structures

Clojure vectors, maps, and sets use structural sharing to provide immutable snapshots with O(log32 N) performance:

```clojure
;; Creating and updating immutable maps via structural sharing
(def original-user {:id 415 :name "Jane" :roles #{:member}})
(def updated-user (update original-user :roles conj :admin))

;; original-user remains completely unchanged:
;; {:id 415 :name "Jane" :roles #{:member}}
```

### Concurrency Primitives (Atoms & Software Transactional Memory)

Manages shared state transitions safely without manual lock synchronization:

```clojure
;; Atoms provide atomic, lock-free state updates via compare-and-swap
(def request-count (atom 0))

;; Thread-safe atomic increment
(swap! request-count inc)
(println "Current requests:" @request-count)
```

### Threading Macros (`->` and `->>`)

Pipelines data transformations cleanly without deeply nested function calls:

```clojure
(defn calculate-revenue [orders]
  (->> orders
       (filter :completed?)
       (map :total-cents)
       (reduce +)
       (* 0.01)))
```

## Common Patterns

### Threading Macros for Data Transformation

**Problem**: Deeply nested function calls are hard to read and mentally trace backwards.

**Solution**:
Use `->>` (thread-last) macro for sequential transformations:

```clojure
(defn process-orders [orders]
  (->> orders
       (filter #(= (:status %) "completed"))
       (map :amount)
       (reduce + 0)))

(println (process-orders [{:status "completed" :amount 50}
                          {:status "pending" :amount 20}
                          {:status "completed" :amount 30}]))
;; => 80
```

## Best Practices

**Do**:

- Embrace REPL-Driven Development: Connect your editor (Calva, CIDER) to a running nREPL and test functions interactively.
- Validate Data with Malli or Clojure Spec: Define explicit schemas for function inputs and API boundaries.
- Use Destructuring Comprehensively: Unpack nested maps and vectors cleanly in function argument vectors.
- Leverage Java Interop Directly: Invoke Java classes (`(java.time.Instant/now)`) directly without wrapper overhead.

**Don't**:

- Fight immutability: Do not introduce mutable Java arrays or global variables where immutable maps suffice.
- Hold references to lazy sequences: Realizing unbounded lazy sequences while retaining their head exhausts JVM heap memory.
- Create deep monolithic namespaces: Break namespaces into cohesive, focused modules.

## Troubleshooting

| Error                                                   | Cause                                                        | Solution                                                                  |
| :------------------------------------------------------ | :----------------------------------------------------------- | :------------------------------------------------------------------------ |
| `CompilerException java.lang.ClassCastException`        | Passing wrong data structure (e.g. sequence instead of map). | Verify types using `(type x)` in the REPL.                                |
| `ArityException: Wrong number of args`                  | Function called with more or fewer arguments than defined.   | Check function parameter vector and multi-arity definitions.              |
| `OutOfMemoryError: Java heap space with lazy sequences` | Retaining the head of an unbounded lazy sequence.            | Use `dorun` or `doseq` to consume lazy seqs without retaining references. |

## References

- [Clojure.org](https://clojure.org/)
- [ClojureDocs](https://clojuredocs.org/)
