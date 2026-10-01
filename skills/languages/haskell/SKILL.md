---
name: haskell
description: Expert Haskell assistance covering pure functional programming, monads, typeclasses, GHC, and Cabal/Stack. Use when developing provably correct software, compilers, financial models, or theorem provers.
---

# Haskell

An advanced, purely functional programming language.

## When to Use

- **Pure Functional Programming**: Building systems with mathematical guarantees of purity, referential transparency, and immutability.
- **Compiler Construction & Domain-Specific Languages (DSLs)**: Authoring parsers, programming language compilers, and type checkers.
- **Financial Modeling & Cryptographic Protocols**: Implementing smart contract runtimes (Cardano/Plutus) and quantitative financial models.
- **High-Assurance Systems**: Mission-critical software where compile-time type verification must eliminate runtime errors entirely.

## Quick Start

```haskell
main :: IO ()
main = putStrLn "Hello, World!"

factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)
```

## Core Concepts

### Non-Strict Lazy Evaluation

Expressions are not evaluated until their results are explicitly demanded by consumer functions:

```haskell
-- Generates an infinite stream of Fibonacci numbers lazily
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- Safely takes only the first 10 elements without evaluating infinity
main :: IO ()
main = print (take 10 fibs) -- [0,1,1,2,3,5,8,13,21,34]
```

### Monads & Explicit I/O Separation

Isolates pure code from side effects (disk, network, state) using Monads:

```haskell
-- Pure logic (no side-effects possible)
validateEmail :: String -> Either String String
validateEmail email
  | '@' `elem` email = Right email
  | otherwise        = Left "Invalid email format"

-- Explicit IO boundary
main :: IO ()
main = do
  putStrLn "Enter email address:"
  input <- getLine
  case validateEmail input of
    Right email -> putStrLn ("Success: " ++ email)
    Left err    -> putStrLn ("Error: " ++ err)
```

### Advanced Typeclasses & Higher-Kinded Types

Defines generic behaviors across data types (Functor, Applicative, Monad):

```haskell
-- Custom Functor mapping over container structure
data Tree a = Leaf a | Node (Tree a) (Tree a) deriving (Show)

instance Functor Tree where
  fmap f (Leaf x)   = Leaf (f x)
  fmap f (Node l r) = Node (fmap f l) (fmap f r)
```

## Common Patterns

### Monadic Error Handling with Either and Do Notation

**Problem**: Deeply nested error checks make business logic unreadable.

**Solution**:
Compose operations cleanly using the `Either` monad:

```haskell
data User = User { userId :: Int, email :: String } deriving (Show)

validateId :: Int -> Either String Int
validateId uid = if uid > 0 then Right uid else Left "Invalid User ID"

validateEmail :: String -> Either String String
validateEmail e = if '@' `elem` e then Right e else Left "Invalid Email"

createUser :: Int -> String -> Either String User
createUser uid e = do
    validId <- validateId uid
    validE  <- validateEmail e
    return (User validId validE)
```

## Best Practices

**Do**:

- Use GHC Modern Language Extensions: Standardize on `GHC2021` or `GHC2024` with `OverloadedStrings` and `RecordWildCards`.
- Use Strict Data Types in Production: Use `Data.Text` instead of `String` (`[Char]`); use strict fields (`!`) in record data types.
- Structure Applications with Polysemy or MTL: Manage effects cleanly using Monad Transformers (`ReaderT`, `ExceptT`) or effect systems.
- Enforce Warnings with `-Wall`: Compile with `-Wall -Werror` to treat unhandled pattern cases as fatal build errors.

**Don't**:

- Use `head` or `fromJust`: Partial functions crash at runtime on empty lists; use pattern matching or safe alternatives (`headMay`).
- Use `String` for high-throughput text processing: The default `String` is a linked list of characters; use `Text` or `ByteString`.
- Cause space leaks with lazy accumulation: Use strict fold (`foldl'`) instead of lazy fold (`foldl`) to prevent building massive thunk trees.

## Troubleshooting

| Error                                                       | Cause                                                | Solution                                                                          |
| :---------------------------------------------------------- | :--------------------------------------------------- | :-------------------------------------------------------------------------------- |
| `Couldn't match expected type '...' with actual type '...'` | Type mismatch in expression.                         | Check function signature and use GHC typed holes (`_`) to inspect required types. |
| `Non-exhaustive patterns in function`                       | Pattern match missing one or more constructor cases. | Compile with `-Wall` to catch unhandled pattern match cases.                      |
| `Infinite loop / space leak on foldl`                       | Lazy evaluation retaining thunk chains in memory.    | Use strict fold `foldl'` from `Data.List` to force eager evaluation.              |

## References

- [Haskell.org](https://www.haskell.org/)
- [Learn You a Haskell](http://learnyouahaskell.com/)
