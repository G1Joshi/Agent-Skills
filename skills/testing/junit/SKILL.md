---
name: junit
description: JUnit testing framework for Java with annotations and assertions. Use for Java tests.
---

# JUnit

Java testing framework for unit and integration testing.

## When to Use

- Java unit testing
- Spring Boot testing
- Integration testing
- TDD development

## Quick Start

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    @Test
    void shouldAddNumbers() {
        Calculator calc = new Calculator();
        assertEquals(5, calc.add(2, 3));
    }

    @Test
    void shouldThrowOnDivisionByZero() {
        Calculator calc = new Calculator();
        assertThrows(ArithmeticException.class, () -> calc.divide(1, 0));
    }
}
```

## Core Concepts

### Lifecycle

```java
class UserServiceTest {
    private UserService service;
    private UserRepository mockRepo;

    @BeforeAll
    static void setUpClass() {
        // Once before all tests
    }

    @BeforeEach
    void setUp() {
        mockRepo = mock(UserRepository.class);
        service = new UserService(mockRepo);
    }

    @AfterEach
    void tearDown() {
        // Cleanup after each test
    }

    @AfterAll
    static void tearDownClass() {
        // Once after all tests
    }
}
```

### Assertions

```java
// Basic assertions
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);
assertTrue(condition);
assertFalse(condition);
assertNull(value);
assertNotNull(value);

// Collections
assertIterableEquals(expected, actual);
assertArrayEquals(expected, actual);

// Exceptions
assertThrows(Exception.class, () -> riskyOperation());
assertDoesNotThrow(() -> safeOperation());

// Grouped assertions
assertAll(
    () -> assertEquals("John", user.getFirstName()),
    () -> assertEquals("Doe", user.getLastName())
);
```

## Common Patterns

### Parameterized Tests

```java
@ParameterizedTest
@ValueSource(strings = {"hello", "world", "test"})
void shouldNotBeEmpty(String input) {
    assertFalse(input.isEmpty());
}

@ParameterizedTest
@CsvSource({
    "1, 2, 3",
    "5, 5, 10",
    "-1, 1, 0"
})
void shouldAdd(int a, int b, int expected) {
    assertEquals(expected, calculator.add(a, b));
}
```

### Mockito Integration

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository repository;

    @InjectMocks
    private UserService service;

    @Test
    void shouldFindUser() {
        when(repository.findById(1L)).thenReturn(Optional.of(new User("John")));

        User user = service.getUser(1L);

        assertEquals("John", user.getName());
        verify(repository).findById(1L);
    }
}
```

## Best Practices

**Do**:

- Use descriptive test names
- Use @Nested for grouping
- Use parameterized tests
- Follow AAA pattern

**Don't**:

- Test private methods directly
- Share state between tests
- Use Thread.sleep
- Ignore test failures

## Troubleshooting

| Issue            | Cause              | Solution              |
| ---------------- | ------------------ | --------------------- |
| Test not running | Missing annotation | Add @Test             |
| Mock not working | Missing extension  | Add @ExtendWith       |
| Assertion fails  | Wrong order        | Check expected/actual |

## References

- [JUnit 5 Documentation](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/)
