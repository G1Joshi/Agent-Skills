---
name: groovy
description: Groovy scripting for JVM, Gradle builds, and Jenkins pipelines. Use for .groovy files.
---

# Groovy

Groovy v4 adds **Switch Expressions**, Records, and Sealed Types. It remains the key to **Gradle** and Jenkins Pipelines.

## When to Use

- **Build Automation**: Writing `build.gradle` scripts.
- **CI/CD**: Writing Jenkinsfiles.
- **Scripting JVM**: Interacting with Java libraries dynamically.

## Core Concepts

### Closures

`{ item -> item.name }`. The core functional primitive.

### Dynamic Typing

`def x = 1`. (Though `@CompileStatic` can force types).

### Builders

`JsonBuilder`, `MarkupBuilder` for generating hierarchical data.

## Best Practices (2025)

**Do**:

- **Use `@CompileStatic`**: For performance critical code (production logic).
- **Use Spock**: The best testing framework on the JVM (written in Groovy).
- **Use `def` sparingly**: Type your variables if you know them.

**Don't**:

- **Don't mix logic in Gradle**: Keep build scripts declarative. Move logic to `buildSrc`.

## References

- [Apache Groovy](https://groovy-lang.org/)
