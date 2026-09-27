---
name: scala
description: Expert Scala (Scala 3) assistance covering functional programming, Akka/Pekko, ZIO, Cats Effect, and Spark. Use when developing distributed systems, high-concurrency microservices, or big data pipelines.
---

# Scala

Scalable Language. It interops seamlessly with Java.

## When to Use

- **Big Data Distributed Processing**: Apache Spark, Apache Flink, and large-scale data engineering pipelines.
- **High-Concurrency Reactive Systems**: Building resilient distributed services with Akka/Pekko actors or Cats Effect/ZIO.
- **Type-Level & Purely Functional Programming**: Enforcing compile-time domain guarantees with Scala 3 given/using and opaque types.
- **Enterprise JVM Microservices**: Leveraging the entire Java ecosystem while utilizing concise, expressive FP idioms.

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

#Scala 3 Contextual Abstractions: Given & Using

Type classes and dependency injection unified cleanly without implicit conversions:

```scala
// Define type class
trait JsonEncoder[A]:
  def encode(a: A): String

// Given instances (type class implementations)
given JsonEncoder[String] with
  def encode(a: String): String = s"\"${a.replace(""", "\\"")}\""

given JsonEncoder[Int] with
  def encode(a: Int): String = a.toString

// Contextual function with 'using' clause
def toJson[T](value: T)(using encoder: JsonEncoder[T]): String =
  encoder.encode(value)

// Extension methods for clean syntax
extension [T](value: T)(using encoder: JsonEncoder[T])
  def asJson: String = encoder.encode(value)
```

#Algebraic Data Types & Exhaustive Pattern Matching

Modeling domain states with Scala 3 sealed traits and enums:

```scala
enum PaymentStatus:
  case Pending
  case Authorized(transactionId: String, amountCents: Long)
  case Failed(reason: String, retryable: Boolean)

def evaluatePayment(status: PaymentStatus): String = status match
  case PaymentStatus.Pending =>
    "Waiting for gateway response..."
  case PaymentStatus.Authorized(txId, amt) =>
    s"Payment $txId confirmed for \$${amt / 100.0}"
  case PaymentStatus.Failed(reason, true) =>
    s"Transient error: $reason. Retrying..."
  case PaymentStatus.Failed(reason, false) =>
    s"Permanent failure: $reason. Contacting customer."
```

#Asynchronous Effect Management with Cats Effect

Pure functional concurrency with resource safety and fiber cancellation:

```scala
import cats.effect.{IO, IOApp, Resource}
import scala.concurrent.duration.*

object ServerApp extends IOApp.Simple:
  def acquireDbConnection: IO[String] = IO.println("DB Connected") *> IO.pure("conn-123")
  def releaseDbConnection(conn: String): IO[Unit] = IO.println(s"DB Disconnected: $conn")

  val dbResource: Resource[IO, String] =
    Resource.make(acquireDbConnection)(releaseDbConnection)

  def run: IO[Unit] =
    dbResource.use { conn =>
      for
        fiber <- IO.sleep(100.millis).as("Query result").start
        res   <- fiber.joinWithNever
        _     <- IO.println(s"Executed on $conn: $res")
      yield ()
    }
```

## Common Patterns

### Enum and Pattern Matching in Scala 3

**Problem**: Verbose sealed trait hierarchies for algebraic data types in legacy Scala 2.

**Solution**:
Use Scala 3 concise `enum` definitions:

```scala
enum TransactionStatus:
  case Pending
  case Approved(txId: String, amount: BigDecimal)
  case Rejected(reason: String)

def describe(status: TransactionStatus): String = status match
  case TransactionStatus.Pending => "Transaction is being processed"
  case TransactionStatus.Approved(id, amount) => s"Approved $id: $$$amount"
  case TransactionStatus.Rejected(reason) => s"Declined: $reason"
```

## Best Practices (2026)

- **Do** embrace Scala 3 syntax: use `enum`, `given`/`using`, and top-level definitions instead of Scala 2 package objects.
- **Do** use `opaque type` aliases for type-safe domain identifiers (e.g. `UserId`, `OrderId`) without heap allocation overhead.
- **Do** structure async applications around functional effect systems (`Cats Effect 3` or `ZIO 2`) rather than raw `scala.concurrent.Future`.
- **Do** enable compiler strictness (`-Xfatal-warnings`, `-Wunused:all`) to maintain clean codebases.
- **Don't** use `var` or mutable collections in domain logic; use immutable collections and `case class .copy()`.
- **Don't** catch raw `Throwable` without re-throwing non-fatal exceptions; use `scala.util.control.NonFatal`.
- **Don't** use `Option.get` or `Try.get`; use `getOrElse`, pattern matching, or for-comprehensions.

## Troubleshooting

| Error                                     | Cause                                                                  | Solution                                                                                       |
| :---------------------------------------- | :--------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| `type mismatch: found ... required ...`   | Incompatible types in expression or missing implicit conversion.       | Verify types and import appropriate typeclass instances.                                       |
| `No implicit arguments found of type ...` | Missing `using` / implicit parameter in scope (e.g. ExecutionContext). | Import default execution context: `import scala.concurrent.ExecutionContext.Implicits.global`. |
| `OutOfMemoryError during sbt compile`     | JVM heap limit too low for Scala compiler.                             | Increase heap in `.sbtopts`: `-J-Xmx4G`.                                                       |

## References

- [Scala Documentation](https://docs.scala-lang.org/)
