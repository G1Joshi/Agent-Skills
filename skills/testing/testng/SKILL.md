---
name: testng
description: TestNG Java testing framework. Use for Java testing.
---

# TestNG

TestNG is a testing framework setup inspired by JUnit and NUnit but introducing some new functionalities that make it more powerful and easier to use, such as parallel testing and data-driven testing.

## When to Use

- **Complex Suites**: You need granular control over which groups of tests run via XML configuration (`testing.xml`).
- **Parallel Execution**: Historically better support for multi-threaded test execution than JUnit.
- **Dependencies**: Tests that depend on other tests (`@Test(dependsOnMethods = { "serverStarted" })`).

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

### Groups

Tagging tests (`@Test(groups = "smoke")`). Allows running specific subsets (Include/Exclude in XML).

### Data Providers

Native support for passing complex objects to tests.

```java
@DataProvider(name = "test1")
public Object[][] createData1() {
 return new Object[][] {
   { "Cedric", new Integer(36) },
   { "Anne", new Integer(37) },
 };
}

@Test(dataProvider = "test1")
public void verifyData1(String n1, Integer n2) { ... }
```

## Best Practices (2025)

**Do**:

- **Use Soft Assertions**: `SoftAssert` allows the test to continue even if one check fails, reporting all errors at the end.
- **Parallelize**: Leverage `thread-count` in CI to speed up execution.

**Don't**:

- **Don't use `dependsOnMethods` for Unit Tests**: Unit tests should be independent. Use dependencies only for Integration flows.

## References

- [TestNG Documentation](https://testng.org/doc/)
