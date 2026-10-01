---
name: fsharp
description: Expert F# functional programming assistance covering pattern matching, immutability, async workflows, and .NET interop. Use when developing type-safe domain models, data processing pipelines, or cloud services.
---

# F#

F# is a functional-first, cross-platform programming language on .NET, combining strong static typing, pattern matching, lightweight syntax, and seamless C# interoperability.

## When to Use

- **Functional-First Software on .NET**: Building robust, concise, type-safe enterprise applications within the .NET ecosystem.
- **Financial Engineering & Domain Modeling**: Modeling financial instruments, actuarial rules, and transactional workflows using algebraic data types.
- **High-Velocity Data Science & ETL**: Manipulating tabular datasets using interactive F# scripts (`.fsx`) and FSharp.Data type providers.
- **Full-Stack Safe Web Apps (SAFE Stack)**: Developing end-to-end type-safe web applications spanning Saturn, Azure, Fable, and Elmish.

## Quick Start

```fsharp
type Person = { Name: string; Age: int }

let describePerson person =
    match person.Age with
    | age when age < 18 -> sprintf "%s is a minor" person.Name
    | _ -> sprintf "%s is an adult" person.Name

let alice = { Name = "Alice"; Age = 25 }
printfn "%s" (describePerson alice)
```

## Core Concepts

### Discriminated Unions & Pattern Matching

Makes illegal business states unrepresentable through closed algebraic data types:

```fsharp
type PaymentMethod =
    | CreditCard of cardNumber: string * cvv: string
    | BankTransfer of iban: string
    | Crypto of walletAddress: string

let processPayment method amount =
    match method with
    | CreditCard(num, _) -> printfn "Charging card %s: $%.2f" num amount
    | BankTransfer iban  -> printfn "Initiating SEPA transfer to %s" iban
    | Crypto wallet      -> printfn "Broadcasting crypto payment to %s" wallet
```

### Type Providers (Compile-Time Schema Generation)

Generates strongly-typed types directly from external JSON, CSV, or SQL sources at compile-time:

```fsharp
open FSharp.Data

type UserApi = JsonProvider<"https://api.example.com/user.json">

let parseUser jsonString =
    let user = UserApi.Parse(jsonString)
    printfn "User Name: %s, Email: %s" user.Name user.Email
```

### Functional Pipelines & Partial Application

Composes functions using forward pipe (`|>`) and composition (`>>`) operators:

```fsharp
let addTax amount = amount * 1.10
let applyDiscount amount = amount - 5.0

let calculateFinalPrice = applyDiscount >> addTax

let finalTotal = 100.0 |> calculateFinalPrice
```

## Common Patterns

### Discriminated Unions for Exhaustive Domain Modeling

**Problem**: Representing complex state transitions with boolean flags leads to invalid object states.

**Solution**:
Use Discriminated Unions with compiler-verified pattern matching:

```fsharp
type PaymentMethod =
    | CreditCard of cardNumber: string * cvv: string
    | PayPal of email: string
    | Crypto of walletAddress: string

let processPayment method amount =
    match method with
    | CreditCard(num, _) -> sprintf "Charging $%.2f to Card ending in %s" amount (num.Substring(num.Length - 4))
    | PayPal email -> sprintf "Charging $%.2f via PayPal (%s)" amount email
    | Crypto wallet -> sprintf "Requesting crypto transfer to %s" wallet
```

## Best Practices

**Do**:

- Make Illegal States Unrepresentable: Model business domains using Discriminated Unions and Records rather than primitive types.
- Use the Result Type for Error Handling: Chain validation steps using `Result.bind` instead of throwing untyped exceptions.
- Leverage F# Interactive (FSI): Rapidly prototype algorithms in `.fsx` script files before adding to production projects.
- Interoperate with C# and .NET Cleanly: Consume NuGet packages and ASP.NET Core libraries natively.

**Don't**:

- Use mutable variables (`mutable`) unnecessarily: Favor immutable values and recursive or folded loops.
- Use `null`: F# values cannot be null by default; use `Option<'T>` to represent optional data.
- Write heavy class hierarchies: Prefer composition of records, functions, and modules over deep inheritance.

## Troubleshooting

| Error                                                              | Cause                                                                | Solution                                                                    |
| :----------------------------------------------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Incomplete pattern matches on this expression`                    | Pattern match missing one or more cases of a Discriminated Union.    | Add missing cases to make pattern match exhaustive.                         |
| `FS0001: Type mismatch`                                            | Expected one type but received another; F# does not implicitly cast. | Cast explicitly using functions like `float`, `int`, or conversion methods. |
| `FS0041: A unique overload for method ... could not be determined` | .NET method overload resolution ambiguous.                           | Provide explicit type annotations on method parameters.                     |

## References

- [F# Guide](https://fsharp.org/)
