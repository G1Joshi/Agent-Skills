---
name: java
description: Expert modern Java (Java 17/21 LTS) assistance covering records, pattern matching, virtual threads (Project Loom), Stream API, and JVM memory tuning. Use when writing idiomatic enterprise Java, optimizing garbage collection, or building concurrent backend applications.
---

# Java

Modern Java development with Java 17+ features, streams, and enterprise patterns.

## When to Use

- **Enterprise Backend Services & Microservices**: Powering high-throughput Spring Boot, Quarkus, and Micronaut backend APIs.
- **Large-Scale Distributed Systems**: Building infrastructure platforms like Apache Kafka, Hadoop, Spark, and Elasticsearch.
- **High-Concurrency Virtual Threads (Project Loom)**: Handling millions of concurrent network connections without reactive code complexity.
- **Mission-Critical Banking & Payment Gateways**: Processing financial transactions with strict type safety, modularity, and garbage collection tuning.

## Quick Start

```java
// Modern record with validation
public record User(String id, String name, String email) {
    public User {
        Objects.requireNonNull(id, "id must not be null");
        Objects.requireNonNull(name, "name must not be null");
    }
}
```

## Core Concepts

### Virtual Threads (Project Loom - Java 21+ LTS)

Lightweight user-mode threads managed by the JVM rather than the OS, allowing synchronous blocking code to scale to millions of concurrent tasks:

```java
import java.net.URI;
import java.net.http.*;
import java.util.concurrent.Executors;

public class VirtualThreadDemo {
    public static void main(String[] args) {
        // Runs each concurrent task on an ephemeral virtual thread
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 10_000; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    // Blocking I/O unmounts virtual thread automatically
                    Thread.sleep(100);
                    return "Task " + taskId + " complete";
                });
            }
        } // Executor awaits completion of all virtual threads
    }
}
```

### Records & Pattern Matching (Java 17/21)

Concise immutable data carriers with expressive pattern matching:

```java
public sealed interface Transaction permits Payment, Refund {}
public record Payment(String transactionId, double amount) implements Transaction {}
public record Refund(String transactionId, double amount, String reason) implements Transaction {}

public class TransactionHandler {
    public static String audit(Transaction tx) {
        return switch (tx) {
            case Payment p when p.amount() > 10_000 -> "Large Payment Audit: " + p.transactionId();
            case Payment p                          -> "Standard Payment: " + p.transactionId();
            case Refund r                           -> "Refund: " + r.reason();
        };
    }
}
```

### Modern Foreign Function & Memory API (Project Panama)

Interacts directly with native C libraries and off-heap memory safely without JNI:

```java
import java.lang.foreign.*;

public class NativeInterop {
    public static void main(String[] args) {
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment nativeString = arena.allocateFrom("Hello Native Memory!");
            System.out.println("Allocated byte size: " + nativeString.byteSize());
        } // Off-heap memory is automatically deallocated here
    }
}
```

## Common Patterns

### Immutable Collection Transformations with Streams

**Problem**: Verbose collection filtering and grouping introducing mutable intermediate states.

**Solution**:

```java
// Immutable collections
var list = List.of("a", "b", "c");
var map = Map.of("key1", "value1", "key2", "value2");

// Stream operations
List<String> names = users.stream()
    .filter(User::active)
    .map(User::name)
    .sorted()
    .toList();

// Collectors grouping
Map<String, List<User>> byRole = users.stream()
    .collect(Collectors.groupingBy(User::role));
```

### Optional

**Problem**: Null reference returns causing unpredictable NullPointerExceptions without compile-time safeguards.

**Solution**:

```java
Optional<User> user = Optional.ofNullable(findUser(id));

String name = user
    .map(User::name)
    .orElse("Unknown");

user.ifPresentOrElse(
    u -> process(u),
    () -> handleMissing()
);
```

## Best Practices

**Do**:

- Adopt Java 21 or 25 LTS: Leverage Virtual Threads, Pattern Matching, Records, and Sequenced Collections.
- Prefer Virtual Threads Over Reactive Complexity: Replace complex WebFlux/RxJava reactive chains with clean synchronous blocking code on virtual threads.
- Use Records for DTOs and Value Objects: Eliminate Lombok boilerplate by using native Java `record`.
- Tune Modern Garbage Collectors: Use ZGC (`-XX:+UseZGC -XX:+ZGenerational`) for sub-millisecond GC pause times on multi-gigabyte heaps.

**Don't**:

- Pool Virtual Threads: Virtual threads are cheap and disposable; create them per task rather than using thread pools.
- Use `synchronized` blocks inside Virtual Threads: Use `ReentrantLock` to avoid pinning virtual threads to OS carrier threads during I/O.
- Return raw `null`: Use `Optional<T>` for return types to force callers to handle absence explicitly.

## Troubleshooting

| Error                             | Cause                      | Solution                         |
| --------------------------------- | -------------------------- | -------------------------------- |
| `NullPointerException`            | Null value access          | Use Optional or null checks      |
| `ClassCastException`              | Invalid type cast          | Use instanceof pattern matching  |
| `ConcurrentModificationException` | Modifying during iteration | Use Iterator.remove() or streams |

## References

- [Java Official Docs](https://docs.oracle.com/en/java/)
- [Baeldung](https://www.baeldung.com/)
