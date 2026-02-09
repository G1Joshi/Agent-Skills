---
name: selenium
description: Selenium WebDriver for cross-browser automation testing. Use for legacy E2E tests.
---

# Selenium

Browser automation framework for web testing.

## When to Use

- Cross-browser testing
- Legacy system testing
- Multi-language support
- CI/CD integration

## Quick Start

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")

element = driver.find_element(By.ID, "search")
element.send_keys("test query")
element.submit()

driver.quit()
```

## Core Concepts

### Locators

```python
from selenium.webdriver.common.by import By

# Finding elements
driver.find_element(By.ID, "element-id")
driver.find_element(By.NAME, "element-name")
driver.find_element(By.CLASS_NAME, "class-name")
driver.find_element(By.TAG_NAME, "input")
driver.find_element(By.CSS_SELECTOR, ".container > .item")
driver.find_element(By.XPATH, "//div[@class='item']")
driver.find_element(By.LINK_TEXT, "Click here")
driver.find_element(By.PARTIAL_LINK_TEXT, "Click")

# Multiple elements
driver.find_elements(By.CLASS_NAME, "item")
```

### Waits

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Explicit wait
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "loaded")))
element = wait.until(EC.element_to_be_clickable((By.ID, "button")))
wait.until(EC.visibility_of_element_located((By.ID, "result")))

# Implicit wait
driver.implicitly_wait(10)
```

## Common Patterns

### Page Object Model

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.submit_button = (By.ID, "submit")

    def enter_email(self, email):
        self.driver.find_element(*self.email_input).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def submit(self):
        self.driver.find_element(*self.submit_button).click()

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.submit()
```

### Actions

```python
from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# Mouse actions
actions.move_to_element(element).click().perform()
actions.double_click(element).perform()
actions.context_click(element).perform()  # Right-click
actions.drag_and_drop(source, target).perform()

# Keyboard
actions.send_keys(Keys.ENTER).perform()
actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
```

## Best Practices

**Do**:

- Use explicit waits
- Implement Page Object Model
- Use headless mode in CI
- Handle stale elements

**Don't**:

- Use Thread.sleep
- Chain too many actions
- Skip cleanup
- Ignore exceptions

## Troubleshooting

| Issue             | Cause           | Solution          |
| ----------------- | --------------- | ----------------- |
| Element not found | Timing issue    | Add explicit wait |
| Stale element     | DOM changed     | Re-find element   |
| Click intercepted | Overlay element | Wait or scroll    |

## References

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Selenium Python](https://selenium-python.readthedocs.io/)
