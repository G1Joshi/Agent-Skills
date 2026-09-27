---
name: xunit
description: Expert xUnit.net testing assistance covering .NET Fact/Theory tests, constructor fixtures, and output capture. Use when writing C# unit tests, testing ASP.NET Core applications, or running `dotnet test`.
---

# xUnit.net

xUnit.net is the modern, open-source unit testing tool for .NET (C#, F#, VB). It is chosen by Microsoft/dotnet for their own repositories.

## When to Use

- **Modern .NET Core Unit Testing**: The modern, opinionated, community-preferred testing framework for C# and ASP.NET Core applications.
- **Isolated Clean Test Execution**: Enforcing a new class instance for every single test method to guarantee zero state contamination.
- **Theory-Driven Parameterized Tests**: Running tests across inline data (`[InlineData]`), member data, and class data sources.
- **Constructor-Based Test Setup**: Replacing `[SetUp]` attributes with standard C# object-oriented constructors and `IDisposable`.

## Quick Start

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void PassingTest()
    {
        Assert.Equal(4, Add(2, 2));
    }

    [Theory]
    [InlineData(3)]
    [InlineData(5)]
    [InlineData(6)]
    public void MyTheory(int value)
    {
        Assert.True(IsOdd(value));
    }
}
```

## Core Concepts

#Instance-Per-Test Lifecycle Architecture

Unlike NUnit and MSTest, xUnit instantiates a completely new instance of the test class for every `[Fact]`, preventing shared instance field state:

```
[ Test Class ] ──new()──→ Runs Fact 1 ──Dispose()
[ Test Class ] ──new()──→ Runs Fact 2 ──Dispose()
```

#Facts vs Theories (`[Fact]` vs `[Theory]`)

- `[Fact]`: Test that is always true and tests invariant conditions.
- `[Theory]`: Parameterized test that executes across datasets:

```csharp
using Xunit;

public class OrderValidatorTests
{
    [Fact]
    public void EmptyOrder_IsInvalid()
    {
        var order = new Order();
        Assert.False(order.IsValid());
    }

    [Theory]
    [InlineData(100, "DISCOUNT10", 90)]
    [InlineData(50, "SAVE5", 45)]
    [InlineData(20, "", 20)]
    public void ApplyDiscount_CalculatesCorrectTotal(decimal price, string code, decimal expected)
    {
        var total = OrderService.CalculateTotal(price, code);
        Assert.Equal(expected, total);
    }
}
```

#Shared Context via Class Fixtures (`IClassFixture<T>`)

Shares expensive setup (database, web test servers) across tests without static state:

```csharp
public class DatabaseFixture : IDisposable
{
    public SqlConnection Connection { get; }
    public DatabaseFixture() { Connection = new SqlConnection("Server=localhost;..."); Connection.Open(); }
    public void Dispose() { Connection.Dispose(); }
}

public class CustomerRepositoryTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;
    public CustomerRepositoryTests(DatabaseFixture fixture) => _fixture = fixture;

    [Fact]
    public void QueriesCustomerRecord() { /* Uses _fixture.Connection */ }
}
```

## Common Patterns

### Theory with InlineData and ClassData

**Problem**: Writing duplicate test methods for multiple inputs in C# applications.

**Solution**:
Use `[Theory]` with `[InlineData]`:

```csharp
using Xunit;

public class MathTests
{
    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(-1, 1, 0)]
    [InlineData(0, 0, 0)]
    public void Add_ValidInputs_ReturnsExpectedSum(int a, int b, int expected)
    {
        var calculator = new Calculator();
        var result = calculator.Add(a, b);
        Assert.Equal(expected, result);
    }
}
```

## Best Practices (2026)

**Do**:

- **Use Constructors for Setup and `Dispose()` for Teardown**: Implement `IDisposable` or `IAsyncLifetime` rather than looking for `[SetUp]`.
- **Use `IClassFixture<T>` for Shared State**: Share heavy dependencies (like Testcontainers or WebApplicationFactory) cleanly.
- **Inject `ITestOutputHelper` for Logging**: Write test logs via `ITestOutputHelper` rather than `Console.WriteLine()`.
- **Run Tests in Parallel**: Leverage xUnit's default parallelization across test collections.

**Don't**:

- **Don't use static variables in test classes**: xUnit runs test classes in parallel; static state introduces race conditions.
- **Don't write `Assert.True(x == y)`**: Use `Assert.Equal(expected, actual)` for informative failure diff messages.
- **Don't create asynchronous void tests**: Always return `async Task` from test methods; `async void` exceptions crash the test runner.

## Troubleshooting

| Error                                             | Cause                                                     | Solution                                                                  |
| :------------------------------------------------ | :-------------------------------------------------------- | :------------------------------------------------------------------------ |
| `No test matches the given testcase filter`       | Filter string doesn't match namespace or class name.      | Run `dotnet test --filter FullyQualifiedName~MathTests`.                  |
| `Console.WriteLine produces no output`            | xUnit isolates console output to prevent race conditions. | Inject `ITestOutputHelper` in constructor and call `_output.WriteLine()`. |
| `Assert.Equal() Failure: Expected ... Actual ...` | Output mismatch in assertion.                             | Review diff and check floating-point precision with tolerance arguments.  |

## References

- [xUnit Documentation](https://xunit.net/)
