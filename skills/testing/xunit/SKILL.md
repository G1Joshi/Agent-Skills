---
name: xunit
description: xUnit .NET testing framework. Use for .NET testing.
---

# xUnit.net

xUnit.net is the modern, open-source unit testing tool for .NET (C#, F#, VB). It is chosen by Microsoft/dotnet for their own repositories.

## When to Use

- **.NET Core / .NET 5+**: The default template choice.
- **Modern Practices**: Enforces good habits (Isolation, Constructor Injection for fixtures).

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

### Facts vs Theories

- `[Fact]`: A test that is always true. Invariant.
- `[Theory]`: A test that is true for a particular set of data (Parameterized).

### Fixtures (IClassFixture)

xUnit creates a new instance of the Test Class for _every_ test method (High isolation). To share context (like a DB connection), implement `IClassFixture<T>`.

### Assert

`Assert.Equal`, `Assert.Throws`, `Assert.Collection`.

## Best Practices (2025)

**Do**:

- **Use `xunit.runner.visualstudio`**: To run tests in VS/VS Code.
- **Use FluentAssertions**: xUnit's asserts are okay, but `value.Should().Be(4)` (FluentAssertions) is much more readable.
- **Constructor Injection**: Use the constructor for Setup, and `Dispose()` (IDisposable) for Teardown. xUnit abolished `[SetUp]` and `[TearDown]` attributes to force cleaner design.

**Don't**:

- **Don't use `Console.WriteLine`**: Use `ITestOutputHelper` injected in the constructor to log outputs.

## References

- [xUnit Documentation](https://xunit.net/)
