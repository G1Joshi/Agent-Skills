---
name: xctest
description: XCTest framework for iOS/macOS testing with XCUITest. Use for Apple platform tests.
---

# XCTest

Apple's testing framework for Swift and Objective-C.

## When to Use

- iOS/macOS unit testing
- UI automation with XCUITest
- Performance testing
- Integration testing

## Quick Start

```swift
import XCTest
@testable import MyApp

final class CalculatorTests: XCTestCase {
    var calculator: Calculator!

    override func setUp() {
        calculator = Calculator()
    }

    func testAddition() {
        XCTAssertEqual(calculator.add(2, 3), 5)
    }
}
```

## Core Concepts

### Assertions

```swift
// Equality
XCTAssertEqual(actual, expected)
XCTAssertNotEqual(actual, unexpected)

// Boolean
XCTAssertTrue(condition)
XCTAssertFalse(condition)

// Nil checks
XCTAssertNil(value)
XCTAssertNotNil(value)

// Comparison
XCTAssertGreaterThan(a, b)
XCTAssertLessThanOrEqual(a, b)

// Throwing
XCTAssertThrowsError(try riskyOperation())
XCTAssertNoThrow(try safeOperation())
```

### Async Testing

```swift
func testAsyncFetch() async throws {
    let user = try await userService.fetchUser(id: "123")
    XCTAssertEqual(user.name, "John")
}

func testWithExpectation() {
    let expectation = expectation(description: "Data loaded")

    dataService.load { result in
        XCTAssertNotNil(result)
        expectation.fulfill()
    }

    wait(for: [expectation], timeout: 5.0)
}
```

## Common Patterns

### UI Testing

```swift
final class LoginUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUp() {
        continueAfterFailure = false
        app.launch()
    }

    func testSuccessfulLogin() {
        app.textFields["email"].tap()
        app.textFields["email"].typeText("user@example.com")

        app.secureTextFields["password"].tap()
        app.secureTextFields["password"].typeText("password123")

        app.buttons["Login"].tap()

        XCTAssertTrue(app.staticTexts["Welcome"].exists)
    }
}
```

### Mocking

```swift
protocol UserRepositoryProtocol {
    func getUser(id: String) async throws -> User
}

class MockUserRepository: UserRepositoryProtocol {
    var mockUser: User?
    var shouldThrow = false

    func getUser(id: String) async throws -> User {
        if shouldThrow { throw TestError.failed }
        return mockUser ?? User(id: id, name: "Mock")
    }
}

func testGetUser() async throws {
    let mockRepo = MockUserRepository()
    mockRepo.mockUser = User(id: "1", name: "John")
    let service = UserService(repository: mockRepo)

    let user = try await service.getUser(id: "1")
    XCTAssertEqual(user.name, "John")
}
```

## Best Practices

**Do**:

- Use async/await for async tests
- Create protocols for mocking
- Use setUp/tearDown properly
- Test accessibility identifiers

**Don't**:

- Force unwrap in tests
- Use Thread.sleep
- Skip UI test cleanup
- Hardcode test data

## Troubleshooting

| Issue                | Cause             | Solution            |
| -------------------- | ----------------- | ------------------- |
| Test timeout         | Async not awaited | Use async/await     |
| UI element not found | Wrong identifier  | Check accessibility |
| Flaky tests          | Race conditions   | Add proper waits    |

## References

- [XCTest Documentation](https://developer.apple.com/documentation/xctest)
- [Testing Tips](https://developer.apple.com/documentation/xcode/testing-your-app)
