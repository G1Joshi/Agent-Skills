---
name: selenium
description: Selenium browser automation framework. Use for web testing.
---

# Selenium

Selenium is an umbrella project for a range of tools and libraries that enable and support the automation of web browsers. It is the grandfather of browser automation and defined the W3C WebDriver standard.

## When to Use

- **Legacy/Enterprise**: Vast ecosystems and existing test suites.
- **Obscure Browsers**: Need to test Internet Explorer (IE Mode) or specialized browsers.
- **Grid**: Distributing tests across a massive farm of diverse OS/Browser combinations.

## Quick Start (Java)

```java
WebDriver driver = new ChromeDriver();
driver.get("https://selenium.dev");
WebElement element = driver.findElement(By.id("search"));
element.sendKeys("webdriver");
element.submit();
driver.quit();
```

## Core Concepts

### WebDriver

The API protocol that talks to the specific browser driver (chromedriver, geckodriver) which then controls the browser.

### Selenium Grid

Allows running tests on different machines against different browsers in parallel.

### Page Object Model (POM)

A design pattern where each UI page is a class. Tests interact with the class methods rather than raw elements.

## Best Practices (2025)

**Do**:

- **Use Explicit Waits**: `WebDriverWait(driver).until(ExpectedConditions....)`.
- **Use Headless Mode**: For faster CI execution (`ChromeOptions.addArguments("--headless")`).
- **Migrate to W3C**: Ensure you are using W3C compliant capabilities.

**Don't**:

- **Don't use Thread.sleep**: It slows down tests and is flaky.
- **Don't mix Logic and Tests**: Strictly follow Page Object Model (POM) to keep tests readable.

## References

- [Selenium Documentation](https://www.selenium.dev/)
