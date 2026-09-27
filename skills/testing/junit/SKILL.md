---
name: junit
description: Expert JUnit 5 testing assistance covering Jupiter assertions, parameterized tests, and test lifecycles. Use when writing Java unit tests, Spring Boot integration tests, or testing Maven/Gradle builds.
---

# JUnit 5

JUnit is the programmer-friendly testing framework for Java and the JVM. JUnit 5 is the current major version, composed of the JUnit Platform, JUnit Jupiter, and JUnit Vintage.

## When to Use

- **Java & JVM Ecosystem Testing**: The gold standard testing framework (JUnit 5 / Jupiter) for Java, Kotlin, and Spring Boot applications.
- **Parameterized & Dynamic Testing**: Executing tests across CSV sources, method sources, and enum arguments.
- **Lifecycle Extensions**: Customizing test execution with JUnit 5 Extension model (`@ExtendWith`).
- **Spring Boot Integration Testing**: Pairing with `@SpringBootTest` and MockMvc to test enterprise web applications.

## Quick Start

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class CalculatorTest {

    @Test
    void addition() {
        assertEquals(2, 1 + 1, "Optional failure message");
    }
}
```

## Core Concepts

#JUnit 5 Architecture (Platform + Jupiter + Vintage)

JUnit 5 separates the test execution engine from the developer API:

```
[ JUnit Platform (Launcher, IDE & Maven/Gradle Execution) ]
        ├── [ JUnit Jupiter (Modern API, Annotations, Extensions) ]
        └── [ JUnit Vintage (Backward compatibility with JUnit 3/4) ]
```

#Parameterized Tests (`@ParameterizedTest`)

Executes a test method repeatedly with differing input sets:

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;

class StringUtilityTest {
    @ParameterizedTest(name = "reverse({0}) should be {1}")
    @CsvSource({
        "radar, radar",
        "hello, olleh",
        "'', ''"
    })
    void testReversal(String input, String expected) {
        assertEquals(expected, StringUtility.reverse(input));
    }
}
```

#Lifecycle Callbacks & Nested Test Contexts

Organizes tests hierarchically with `@Nested` and handles setup/teardown cleanly:

```java
import org.junit.jupiter.api.*;

class OrderServiceTest {
    @BeforeEach
    void setUp() { /* Common setup */ }

    @Nested
    @DisplayName("When order has no discount")
    class NoDiscount {
        @Test
        void calculatesFullPrice() { /* ... */ }
    }
}
```

## Common Patterns

### Parameterized Tests with CSV or Method Source

**Problem**: Writing multiple `@Test` methods for different inputs leads to verbose and brittle test classes.

**Solution**:
Use `@ParameterizedTest` with `@CsvSource`:

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.assertEquals;

class MathUtilsTest {
    @ParameterizedTest(name = "{0} + {1} should equal {2}")
    @CsvSource({
        "1, 2, 3",
        "10, 20, 30",
        "-5, 5, 0"
    })
    void testAddition(int a, int b, int expected) {
        assertEquals(expected, MathUtils.add(a, b));
    }
}
```

## Best Practices (2026)

**Do**:

- **Standardize on JUnit Jupiter (JUnit 5)**: Remove the legacy `junit-vintage-engine` dependency from modern projects.
- **Use AssertJ for Fluent Assertions**: Pair JUnit with `assertThat(result).isNotNull().hasSize(3)` for clear assertion failures.
- **Leverage `@TempDir` for File Tests**: Inject temporary directories automatically cleaned up after test completion.
- **Use Display Names**: Provide descriptive `@DisplayName("Should reject expired payment tokens")` annotations.

**Don't**:

- **Don't import JUnit 4 annotations**: Avoid importing `org.junit.Test`; always use `org.junit.jupiter.api.Test`.
- **Don't make test classes or methods `public` in JUnit 5**: Jupiter classes and methods can and should be package-private.
- **Don't ignore test execution order**: Tests should be completely independent; avoid relying on execution sequences.

## Troubleshooting

| Error                                                      | Cause                                                                | Solution                                                                                |
| :--------------------------------------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| `No tests found matching selector`                         | Missing JUnit 5 Jupiter engine dependency in pom.xml / build.gradle. | Add `org.junit.jupiter:junit-jupiter-engine` and enable `useJUnitPlatform()` in Gradle. |
| `org.opentest4j.AssertionFailedError`                      | Expected value does not match actual output.                         | Inspect assertion message: parameter ordering is `assertEquals(expected, actual)`.      |
| `IllegalStateException: Failed to load ApplicationContext` | Spring Boot configuration error during test setup.                   | Check `@ContextConfiguration` or mock missing beans using `@MockBean`.                  |

## References

- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
