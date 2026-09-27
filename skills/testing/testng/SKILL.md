---
name: testng
description: Expert TestNG testing assistance covering annotations, groups, parallel execution, and data providers. Use when writing enterprise Java tests, configuring `testng.xml`, or automating regression suites.
---

# TestNG

TestNG is a testing framework setup inspired by JUnit and NUnit but introducing some new functionalities that make it more powerful and easier to use, such as parallel testing and data-driven testing.

## When to Use

- **Enterprise Java Testing**: Powerful testing framework for Java offering advanced dependency management, grouping, and parallel execution.
- **Complex Test Dependency Graphs**: Defining tests that depend on the successful execution of previous test methods (`dependsOnMethods`).
- **Data-Driven Testing via DataProviders**: Passing multi-dimensional test datasets using `@DataProvider`.
- **Large-Scale Selenium / Appium Suites**: Orchestrating multi-browser enterprise test matrices with `testng.xml` suite descriptors.

## Quick Start

```java
import org.testng.Assert;
import org.testng.annotations.Test;

public class TestNGExample {
    @Test(groups = { "fast" })
    public void testAdd() {
        Assert.assertEquals(1 + 1, 2);
    }
}
```

```xml
<!-- testng.xml -->
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd" >
<suite name="Suite1" parallel="methods" thread-count="5">
  <test name="test1">
    <classes>
       <class name="com.example.TestNGExample"/>
    </classes>
  </test>
</suite>
```

## Core Concepts

#Declarative testng.xml Suite Management

Orchestrates multi-suite, multi-thread test runs across packages:

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Enterprise Regression Suite" parallel="tests" thread-count="4">
    <test name="Chrome Tests">
        <parameter name="browser" value="chrome"/>
        <classes>
            <class name="com.example.tests.CheckoutTest"/>
        </classes>
    </test>
</suite>
```

#Method Dependencies (`dependsOnMethods`)

Ensures downstream tests execute only if prerequisite tests pass:

```java
import org.testng.annotations.Test;
import org.testng.Assert;

public class UserWorkflowTest {
    @Test
    public void createUser() {
        Assert.assertTrue(api.register("user@test.com"));
    }

    @Test(dependsOnMethods = {"createUser"})
    public void loginUser() {
        Assert.assertTrue(api.login("user@test.com"));
    }
}
```

#Native DataProviders

Feeds parameterized data to test methods:

```java
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class CalculationTest {
    @DataProvider(name = "taxData")
    public Object[][] provideTaxData() {
        return new Object[][] {
            { 100.0, "NY", 108.875 },
            { 100.0, "CA", 107.25 }
        };
    }

    @Test(dataProvider = "taxData")
    public void testTaxCalculation(double amount, String state, double expected) {
        Assert.assertEquals(TaxCalculator.calculate(amount, state), expected, 0.01);
    }
}
```

## Common Patterns

### Parallel Test Execution with Groups

**Problem**: Large regression test suites take hours to run sequentially in CI pipelines.

**Solution**:
Organize tests into groups and configure parallel execution in `testng.xml`:

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd" >
<suite name="RegressionSuite" parallel="methods" thread-count="4">
  <test name="SmokeTests">
    <groups>
      <run>
        <include name="smoke"/>
      </run>
    </groups>
    <classes>
      <class name="com.example.OrderTest"/>
      <class name="com.example.UserTest"/>
    </classes>
  </test>
</suite>
```

## Best Practices (2026)

**Do**:

- **Leverage `parallel="methods"` for Fast Execution**: Run independent tests concurrently by configuring thread counts in `testng.xml`.
- **Use Groups for Test Categorization**: Tag tests with `@Test(groups = {"smoke", "nightly"})` for selective execution.
- **Implement `ITestListener` for Reporting**: Create custom listeners to log failures, capture screenshots, and publish metrics.
- **Soft Assertions for Multi-Field Validations**: Use `SoftAssert` to collect all field discrepancies before failing the test.

**Don't**:

- **Don't overuse `dependsOnMethods`**: Keep tests independent whenever possible; method dependencies hinder parallel execution.
- **Don't hardcode browser parameters in code**: Pass configuration parameters dynamically via `testng.xml` parameters.
- **Don't ignore thread safety in parallel suites**: Ensure shared drivers and utilities use `ThreadLocal<WebDriver>`.

## Troubleshooting

| Error                                              | Cause                                                                     | Solution                                                                         |
| :------------------------------------------------- | :------------------------------------------------------------------------ | :------------------------------------------------------------------------------- |
| `Cannot find class in classpath`                   | Class path in `testng.xml` has typo or build didn't compile test classes. | Verify package name and run `mvn test-compile` first.                            |
| `TestNGException: Method requires a @DataProvider` | DataProvider name does not match declared name or signature is invalid.   | Ensure `@DataProvider(name = "x")` returns `Object[][]` or `Iterator<Object[]>`. |
| `ConcurrentModificationException in parallel run`  | Non-thread-safe state shared across test threads.                         | Use `ThreadLocal` for drivers/contexts or isolate state per test instance.       |

## References

- [TestNG Documentation](https://testng.org/doc/)
