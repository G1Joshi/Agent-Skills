---
name: ocaml
description: Expert OCaml functional programming assistance covering algebraic data types, pattern matching, modules, and Dune. Use when developing static analysis tools, compilers, theorem provers, or high-assurance software.
---

# OCaml

OCaml v5 brings **Multicore** support to the language, removing the Global Interpreter Lock (GIL). It combines functional safety with imperative speed.

## When to Use

- **High-Performance Static Functional Programming**: Writing safe, algebraic, strongly-typed systems running at near-C execution speeds.
- **Financial Trading Platforms (Jane Street)**: Building mission-critical quantitative trading infrastructure and order books.
- **Static Analysis & Formal Verification Tools**: Authoring compilers, linters, and verification suites (Coq, Flow, Infer).
- **Multicore Parallelism (OCaml 5)**: Leveraging OCaml 5's native multicore concurrency, domains, and effect handlers.

## Quick Start

```ocaml
(* Define a recursive binary tree and compute depth *)
type 'a tree =
  | Leaf
  | Node of 'a * 'a tree * 'a tree

let rec depth = function
  | Leaf -> 0
  | Node (_, left, right) -> 1 + max (depth left) (depth right)

let my_tree = Node ("root", Node ("left", Leaf, Leaf), Leaf)
let () = Printf.printf "Tree depth: %d\n" (depth my_tree)
```

## Core Concepts

### Hindley-Milner Type Inference & Pattern Matching

Infers static types globally without requiring verbose type annotations:

```ocaml
(* Algebraic Data Type with Exhaustive Pattern Matching *)
type payment_status =
  | Pending of float
  | Completed of { id: string; amount: float }
  | Failed of string

let summarize_payment = function
  | Pending amount -> Printf.sprintf "Pending charge of $%.2f" amount
  | Completed { id; amount } -> Printf.sprintf "Completed #%s: $%.2f" id amount
  | Failed reason -> Printf.sprintf "Failed: %s" reason
```

### Module System (Signatures & Functors)

Powerful structural module system supporting parameterized modules (Functors):

```ocaml
module type COMPARABLE = sig
  type t
  val compare : t -> t -> int
end

(* Functor generates a Set for any comparable type *)
module MakeSet (Item : COMPARABLE) = struct
  type element = Item.t
  (* Internal balanced tree implementation *)
end
```

### OCaml 5 Effect Handlers & Multicore Domains

Native CPU domain parallelism and structured non-blocking effects:

```ocaml
open Domain

let task1 = spawn (fun () -> Array.fold_left (+) 0 (Array.make 1_000_000 1))
let task2 = spawn (fun () -> Array.fold_left (+) 0 (Array.make 1_000_000 2))

let total = join task1 + join task2
```

## Common Patterns

### Modular Architecture with Functors

**Problem**: Writing generic container algorithms independent of concrete key comparison logic.

**Solution**:
Use OCaml Functors (modules parameterized by modules):

```ocaml
module type Comparable = sig
  type t
  val compare : t -> t -> int
end

module MakeSet (Item : Comparable) = struct
  type element = Item.t
  type t = element list
  let empty = []
  let rec insert x = function
    | [] -> [x]
    | h :: t as l ->
        let c = Item.compare x h in
        if c = 0 then l
        else if c < 0 then x :: l
        else h :: (insert x t)
end
```

## Best Practices

**Do**:

- Use Dune as Standard Build System: Build, test, and manage projects exclusively using `dune build` and `dune runtest`.
- Adopt OCaml 5+: Utilize modern Multicore OCaml with concurrent Domain execution.
- Leverage Jane Street Base & Core: Enhance the standard library using battle-tested `Base` and `Core`.
- Enforce Exhaustive Pattern Matching: Address all compiler warnings (`-w +A`) regarding unhandled pattern cases.

**Don't**:

- Use polymorphic equality (`=`) carelessly: Polymorphic equality can crash at runtime on functional closures; use typed comparators.
- Rely on unhandled exceptions for control flow: Represent failure explicitly using `Result.t` or `Option.t`.
- Mutate state across Domains without synchronization: Use atomic variables (`Atomic.t`) when sharing memory between threads.

## Troubleshooting

| Error                                                                            | Cause                                                       | Solution                                                              |
| :------------------------------------------------------------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------------------- |
| `Error: This expression has type ... but an expression was expected of type ...` | Type mismatch in expression.                                | Check function argument order; OCaml does not perform implicit casts. |
| `Warning 8 [partial-match]: this pattern-matching is not exhaustive`             | Pattern matching missing one or more cases.                 | Add missing match cases to ensure all possibilities are handled.      |
| `Error: Unbound module ...`                                                      | Module not installed or missing in Dune `libraries` stanza. | Add library dependency to `dune` file and run `dune build`.           |

## References

- [OCaml.org](https://ocaml.org/)
