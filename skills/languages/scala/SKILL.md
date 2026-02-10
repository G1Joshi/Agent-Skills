---
name: scala
description: Scala functional and OOP programming on the JVM with Akka. Use for .scala files.
---

# Scala

Scalable Language. It interops seamlessly with Java.

## When to Use

- Big Data processing (Spark)
- High-concurrency systems (Akka)
- Functional programming on the JVM
- Complex domains

## Quick Start

```scala
object Hello extends App {
  println("Hello, World!")

  val list = List(1, 2, 3)
  val doubled = list.map(_ * 2)
  println(doubled)
}
```

## Core Concepts

### Functional & OOP

Classes and traits mixed with higher-order functions and immutability.

### Immutability

Default preference for immutable data structures (`val` vs `var`).

### Pattern Matching

Powerful switch-like construct.

```scala
x match {
  case 1 => "one"
  case "two" => 2
  case _ => "other"
}
```

### Case Classes

Immutable value objects with built-in `equals`, `hashCode`, and pattern matching support.

## Best Practices

**Do**:

- Prefer immutability (`val`)
- Use Option instead of null
- Leverage the type system
- Use scalafmt

**Don't**:

- Write "Java in Scala"
- Overuse implicit conversions (can be confusing)
- Use `return` keyword (expression-oriented)

## References

- [Scala Documentation](https://docs.scala-lang.org/)
