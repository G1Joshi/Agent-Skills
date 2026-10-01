---
name: selenium
description: Expert Selenium WebDriver automation covering multi-browser testing, explicit waits, and page objects. Use when automating web browsers, running legacy test automation, or interacting with web UIs.
---

# Selenium

Selenium is an umbrella project for a range of tools and libraries that enable and support the automation of web browsers. It is the grandfather of browser automation and defined the W3C WebDriver standard.

## When to Use

- **Enterprise Cross-Browser Automation**: The foundational W3C standard for browser automation across Chrome, Firefox, Safari, and Edge.
- **Distributed Grid Scaling (Selenium Grid 4)**: Running enterprise test suites across distributed Docker/Kubernetes grid clusters.
- **Polyglot Test Automation**: Maintaining shared test frameworks across Java, Python, C#, Ruby, and JavaScript teams.
- **Legacy Test Suite Maintenance**: Extending long-standing enterprise test suites built on Selenium WebDriver.

## Quick Start

```java
WebDriver driver = new ChromeDriver();
driver.get("https://selenium.dev");
WebElement element = driver.findElement(By.id("search"));
element.sendKeys("webdriver");
element.submit();
driver.quit();
```

## Core Concepts

### W3C Standardized WebDriver Architecture

Clients communicate with browser-specific drivers (ChromeDriver, GeckoDriver) using standard W3C HTTP commands:

```text
[ Test Script (Java/Python/C#) ] ──(W3C WebDriver Protocol)──→ [ Browser Driver (chromedriver) ] ──→ [ Browser ]
```

### Explicit Waits with WebDriverWait & ExpectedConditions

Polls the DOM until specific conditions (visibility, clickability) are fulfilled:

```java
// Java Selenium WebDriver 4
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

public class LoginPageTest {
    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        try {
            driver.get("https://app.example.com/login");

            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
            WebElement emailInput = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("email")));
            emailInput.sendKeys("user@example.com");

            WebElement submitBtn = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("button[type='submit']")));
            submitBtn.click();
        } finally {
            driver.quit();
        }
    }
}
```

### Page Object Model (POM) Design Pattern

Encapsulates page selectors and interactions into reusable classes:

```python
# Python Page Object
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.submit_button = (By.CSS_SELECTOR, "button.login")

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.submit_button).click()
```

## Common Patterns

### Explicit Wait Strategy to Avoid Flakiness

**Problem**: Static `time.sleep()` calls either slow down test runs or cause random flakiness under load.

**Solution**:
Use WebDriverWait with Expected Conditions:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")

element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "submit-btn"))
)
element.click()
```

## Best Practices

**Do**:

- Always Use Explicit Waits: Never use `Thread.sleep()` or global implicit waits; use `WebDriverWait` with `ExpectedConditions`.
- Implement the Page Object Model: Separate test assertions from UI selector mechanics.
- Always Call `driver.quit()` in Teardown: Prevent orphaned driver and browser processes from consuming runner memory.
- Leverage Selenium Manager: Allow Selenium 4.x to manage browser driver downloads automatically without manual binary management.

**Don't**:

- Mix implicit and explicit waits: Mixing both causes unpredictable wait durations that multiply timeouts.
- Use fragile XPath hierarchies: Avoid absolute paths like `/html/body/div[2]/div[1]/button`; use unique IDs or CSS selectors.
- Run UI tests for pure API validation: Use lightweight HTTP libraries for API testing; reserve Selenium for user journeys.

## Troubleshooting

| Error                                                                       | Cause                                                                   | Solution                                                               |
| :-------------------------------------------------------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `SessionNotCreatedException: This version of ChromeDriver only supports...` | Installed ChromeDriver version does not match installed Chrome browser. | Use `webdriver-manager` or upgrade Chrome browser to match driver.     |
| `StaleElementReferenceException`                                            | DOM node was removed or re-rendered after element was found.            | Re-locate the element immediately prior to calling actions on it.      |
| `ElementClickInterceptedException`                                          | Floating banner, modal, or overlay blocking target click.               | Dismiss overlay or scroll element into view using JavaScript executor. |

## References

- [Selenium Documentation](https://www.selenium.dev/)
