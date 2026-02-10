---
name: nunit
description: NUnit .NET testing framework. Use for .NET testing.
---

# NUnit

Ported from JUnit, NUnit is one of the oldest and most feature-rich frameworks for .NET. Ideally suited for complex test setups and legacy migrations.

## When to Use

- **Legacy/Enterprise**: Large existing codebases often use NUnit.
- **Complex Lifecycle**: If you really need `[OneTimeSetUp]`, `[SetUp]`, `[TearDown]` hooks which xUnit discourages.
- **Parallelism**: Strong parallel execution support (`[Parallelizable]`).

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

### Constraints Model (Assert.That)

NUnit offers a powerful fluent assertion style.
`Assert.That(result, Is.EqualTo(4));`
`Assert.That(list, Has.Exactly(1).EqualTo("foo"));`

### Attributes

- `[Test]`: Marks a method as a test.
- `[TestCase]`: Parameterized test input.
- `[Category]`: Grouping for filtering (`dotnet test --filter Category=Integration`).

## Best Practices (2025)

**Do**:

- **Use the Constraint Model (`Assert.That`)**: It enables better error messages than `Assert.AreEqual`.
- **Parallel execution**: Enable it in `AssemblyInfo.cs` to speed up lengthy suites. `[assembly: Parallelizable(ParallelScope.Fixtures)]`.

**Don't**:

- **Don't share state in static fields**: NUnit reuses the same test class instance for all tests (unlike xUnit), so dirty static state can leak between tests.

## References

- [NUnit Documentation](https://nunit.org/)
