---
name: nunit
description: Expert NUnit testing assistance covering .NET assertions, test fixtures, and parameterized testing. Use when writing C# / F# unit tests, testing .NET solutions, or running `dotnet test`.
---

# NUnit

Ported from JUnit, NUnit is one of the oldest and most feature-rich frameworks for .NET. Ideally suited for complex test setups and legacy migrations.

## When to Use

- **C# and .NET Testing**: A mature, feature-rich testing framework widely used across enterprise .NET applications.
- **Parameterized & Combinatorial Testing**: Generating test matrices effortlessly with `[TestCase]` and `[Combinatorial]`.
- **Constraint-Based Assertions**: Writing expressive assertions using the `Assert.That()` syntax.
- **ASP.NET Core & Unity Game Testing**: Testing web APIs, microservices, and Unity game scripts.

## Quick Start

```csharp
using NUnit.Framework;

[TestFixture]
public class Tests
{
    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void Test1()
    {
        Assert.Pass();
    }

    [TestCase(1, 2, 3)]
    [TestCase(2, 2, 4)]
    public void TestAdd(int a, int b, int expected)
    {
       Assert.AreEqual(expected, a + b);
    }
}
```

## Core Concepts

### Constraint-Based Assertion Model

NUnit emphasizes fluent constraint assertions over legacy multiple-assert methods:

```csharp
using NUnit.Framework;

[TestFixture]
public class AccountTests
{
    [Test]
    public void TestDepositIncreasesBalance()
    {
        var account = new Account(100);
        account.Deposit(50);

        Assert.That(account.Balance, Is.EqualTo(150));
        Assert.That(account.Transactions, Has.Count.EqualTo(1));
        Assert.That(account.Owner, Does.StartWith("Jane"));
    }
}
```

### Parameterized Test Cases (`[TestCase]`)

Passes inline parameters to test multiple input/output permutations:

```csharp
[TestCase(10, 20, 30)]
[TestCase(-5, 5, 0)]
[TestCase(0, 0, 0)]
public void Add_ReturnsCorrectSum(int a, int b, int expected)
{
    var calculator = new Calculator();
    Assert.That(calculator.Add(a, b), Is.EqualTo(expected));
}
```

### Multiple Assertions Block (`Assert.Multiple`)

Executes all assertions in a block, reporting all failures rather than terminating on the first:

```csharp
[Test]
public void ValidateUserRecord()
{
    var user = GetUser();
    Assert.Multiple(() =>
    {
        Assert.That(user.FirstName, Is.EqualTo("Jane"));
        Assert.That(user.LastName, Is.EqualTo("Doe"));
        Assert.That(user.IsActive, Is.True);
    });
}
```

## Common Patterns

### Parameterized Test Fixture with Setup

**Problem**: Redundant boilerplate when testing multiple implementations of the same interface.

**Solution**:
Use `[TestCase]` with typed expectations:

```csharp
using NUnit.Framework;

[TestFixture]
public class CalculatorTests
{
    private Calculator _calculator;

    [SetUp]
    public void SetUp()
    {
        _calculator = new Calculator();
    }

    [TestCase(5, 3, 8)]
    [TestCase(-1, 1, 0)]
    [TestCase(0, 0, 0)]
    public void Add_ReturnsExpectedSum(int a, int b, int expected)
    {
        int result = _calculator.Add(a, b);
        Assert.That(result, Is.EqualTo(expected));
    }
}
```

## Best Practices

**Do**:

- Adopt `Assert.Multiple`: Run all field assertions on complex objects to view full failure contexts simultaneously.
- Use `Assert.That` Exclusively: Modern NUnit deprecates legacy `Assert.AreEqual()` in favor of the constraint model.
- Enable Parallel Execution: Add `[assembly: Parallelizable(ParallelScope.Fixtures)]` to accelerate test execution.
- Pair with FluentAssertions: Combine with `FluentAssertions` library for enhanced assertion readability.

**Don't**:

- Use `[SetUp]` for slow integration setup: Use `[OneTimeSetUp]` for database connections shared across the fixture.
- Leave static shared state unreset: Ensure parallelizable test fixtures do not mutate static state.
- Write huge monolithic test methods: Keep test methods focused on single business behaviors.

## Troubleshooting

| Error                                                              | Cause                                                      | Solution                                                                                     |
| :----------------------------------------------------------------- | :--------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| `No test is available in ... Make sure test project has reference` | Missing `NUnit3TestAdapter` NuGet package in test project. | Install `NUnit3TestAdapter` and `Microsoft.NET.Test.Sdk`.                                    |
| `AssertionException: Expected: ... But was: ...`                   | Calculation result does not match expectation.             | Check logic and verify constraints using fluent `Assert.That(actual, Is.EqualTo(expected))`. |
| `System.NullReferenceException in SetUp`                           | Accessing uninitialized fixture field in test execution.   | Ensure initialization code is in a `[SetUp]` method, not in standard constructor.            |

## References

- [NUnit Documentation](https://nunit.org/)
