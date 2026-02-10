---
name: java
description: Java OOP with Spring ecosystem, Maven/Gradle, streams, and JVM optimization. Use for .java files.
---

# Java

Modern Java development with Java 17+ features, streams, and enterprise patterns.

## When to Use

- Working with `.java` files
- Building enterprise applications with Spring Boot
- Android development with Kotlin interop
- Microservices architecture

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

### Records (Java 17+)

```java
// Immutable data carriers
public record User(String id, String name, String email) {
    // Compact constructor for validation
    public User {
        Objects.requireNonNull(id, "id must not be null");
    }

    // Additional methods
    public String displayName() {
        return name.toUpperCase();
    }
}
```

### Sealed Classes

```java
public sealed interface Result<T> permits Success, Failure {
    T getOrThrow();
}

public record Success<T>(T value) implements Result<T> {
    @Override
    public T getOrThrow() { return value; }
}

public record Failure<T>(Exception error) implements Result<T> {
    @Override
    public T getOrThrow() { throw new RuntimeException(error); }
}
```

## Common Patterns

### Streams & Collections

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

- Use `var` for local variables with obvious types
- Prefer records for data transfer objects
- Use Optional instead of null checks
- Use virtual threads for I/O-bound tasks (Java 21+)

**Don't**:

- Use raw types for collections (use generics)
- Use `Optional.get()` without checking
- Catch generic `Exception` (be specific)
- Create mutable DTOs unnecessarily

## Troubleshooting

| Error                             | Cause                      | Solution                         |
| --------------------------------- | -------------------------- | -------------------------------- |
| `NullPointerException`            | Null value access          | Use Optional or null checks      |
| `ClassCastException`              | Invalid type cast          | Use instanceof pattern matching  |
| `ConcurrentModificationException` | Modifying during iteration | Use Iterator.remove() or streams |

## References

- [Java Official Docs](https://docs.oracle.com/en/java/)
- [Baeldung](https://www.baeldung.com/)
