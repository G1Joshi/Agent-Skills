---
name: phpunit
description: Expert PHPUnit testing assistance covering PHP assertions, data providers, and test doubles. Use when writing unit and functional tests for PHP, Laravel, Symfony, or WordPress.
---

# PHPUnit

PHPUnit is the standard unit testing framework for the PHP ecosystem. Examples include usage in Laravel, Symfony, and WordPress.

## When to Use

- **PHP Standard Testing Framework**: The official, universal testing framework for Laravel, Symfony, and modern PHP applications.
- **Unit and Integration Testing**: Testing PHP domain models, services, controllers, and database interactions.
- **Data Providers for Parameterized Tests**: Running tests against multi-dimensional test datasets using `@dataProvider`.
- **Mocking & Test Doubles**: Generating mock objects and verifying invocation expectations natively without external libraries.

## Quick Start

```php
<?php
use PHPUnit\Framework\TestCase;

final class StackTest extends TestCase
{
    public function testPushAndPop(): void
    {
        $stack = [];
        $this->assertEmpty($stack);

        array_push($stack, 'foo');
        $this->assertNotEmpty($stack);
        $this->assertEquals('foo', array_pop($stack));
    }
}
```

## Core Concepts

### PHPUnit Test Case Structure

Extends `TestCase` and leverages modern PHP 8 attributes:

```php
<?php
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\DataProvider;

final class CurrencyConverterTest extends TestCase
{
    #[Test]
    #[DataProvider('currencyProvider')]
    public function it_converts_usd_to_eur(float $usd, float $expectedEur): void
    {
        $converter = new CurrencyConverter(exchangeRate: 0.92);
        $this->assertEqualsWithDelta($expectedEur, $converter->toEur($usd), 0.01);
    }

    public static function currencyProvider(): array
    {
        return [
            'zero value' => [0.0, 0.0],
            'standard transaction' => [100.0, 92.0],
            'fractional amount' => [10.50, 9.66],
        ];
    }
}
```

### Native Mock Objects

Stubs methods and asserts on invocation parameters:

```php
public function testPaymentServiceSendsNotification(): void
{
    $mailerMock = $this->createMock(MailerInterface::class);
    $mailerMock->expects($this->once())
        ->method('send')
        ->with($this->equalTo('user@example.com'));

    $service = new PaymentService($mailerMock);
    $service->processPayment('user@example.com', 50);
}
```

### Declarative phpunit.xml Configuration

Configures test suites, environment variables, and coverage enforcement:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
         cacheDirectory=".phpunit.cache">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
    </testsuites>
    <source>
        <include><directory>src</directory></include>
    </source>
</phpunit>
```

## Common Patterns

### Data Providers for Clean Test Matrices

**Problem**: Writing multiple separate test methods to validate email formatting regex rules.

**Solution**:
Use PHPUnit Data Providers:

```php
use PHPUnit\Framework\TestCase;

class ValidatorTest extends TestCase
{
    /**
     * @dataProvider emailProvider
     */
    public function testEmailValidation(string $email, bool $expected): void
    {
        $validator = new EmailValidator();
        $this->assertSame($expected, $validator->isValid($email));
    }

    public static function emailProvider(): array
    {
        return [
            ['test@example.com', true],
            ['invalid-email', false],
            ['user@sub.domain.org', true],
            ['', false],
        ];
    }
}
```

## Best Practices

**Do**:

- Adopt PHP 8 Attributes: Use `#[Test]` and `#[DataProvider]` instead of legacy docblock annotations (`@test`).
- Use Static Data Providers: Ensure all data provider methods are declared as `public static`.
- Run with `--colors=always --testdox`: Produce clean, human-readable test output in local terminals and CI.
- Enforce Strict Types in Tests: Add `declare(strict_types=1);` at the top of all test files.

**Don't**:

- Use `@runInSeparateProcess` unless strictly necessary: Process isolation adds severe performance overhead.
- Use `assertEquals` on floats: Use `assertEqualsWithDelta` to avoid floating point precision failures.
- Catch exceptions manually: Use `$this->expectException(CustomException::class)` to assert on thrown errors.

## Troubleshooting

| Error                                                  | Cause                                                            | Solution                                                                 |
| :----------------------------------------------------- | :--------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `Class 'PHPUnit\Framework\TestCase' not found`         | Composer autoload missing or PHPUnit not installed via Composer. | Run `composer dump-autoload` and execute via `./vendor/bin/phpunit`.     |
| `Failed asserting that false is true`                  | Method assertion failed.                                         | Add custom failure message: `$this->assertTrue($val, 'Custom message')`. |
| `Risky Test: This test did not perform any assertions` | Test executed code without performing explicit `$this->assert*`. | Add assertion or mark with `@doesNotPerformAssertions` annotation.       |

## References

- [PHPUnit Documentation](https://phpunit.de/documentation.html)
