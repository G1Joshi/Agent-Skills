---
name: haskell
description: Haskell pure functional programming with monads and type classes. Use for .hs files.
---

# Haskell

An advanced, purely functional programming language.

## When to Use

- Academic Research
- Compilers / DSLs
- Financial Systems (correctness)
- High-assurance software

## Quick Start

```haskell
main :: IO ()
main = putStrLn "Hello, World!"

factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)
```

## Core Concepts

### Pure Functions

Functions have no side effects. Output depends only on input.

### Lazy Evaluation

Expressions are not evaluated until their results are needed.

```haskell
ints = [1..] -- Infinite list
take 5 ints  -- [1, 2, 3, 4, 5]
```

### Type System

Strong, static typing with type inference and Type Classes (similar to Interfaces).

```haskell
class Eq a where
  (==) :: a -> a -> Bool
```

### Monads

A structure that represents computations defined as sequences of steps (e.g., IO, Maybe).

## Best Practices

**Do**:

- Use HLint
- Write type signatures for top-level functions
- Use pattern matching

**Don't**:

- Write partial functions (e.g., `head` on empty list) if possible
- Use complex monad stacks without abstraction

## References

- [Haskell.org](https://www.haskell.org/)
- [Learn You a Haskell](http://learnyouahaskell.com/)
