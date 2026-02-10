---
name: phpunit
description: PHPUnit PHP testing framework. Use for PHP testing.
---

# PHPUnit

PHPUnit is the standard unit testing framework for the PHP ecosystem. Examples include usage in Laravel, Symfony, and WordPress.

## When to Use

- **PHP Application**: The industry standard.
- **TDD**: Built-in support for mocking and code coverage.

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

### Assertions

Methods like `$this->assertTrue()`, `$this->assertSame()`, `$this->expectException()`.

### Mock Objects

PHPUnit gives you control over the behavior of dependencies.

```php
$stub = $this->createMock(SomeClass::class);
$stub->method('doSomething')->willReturn('foo');
$this->assertEquals('foo', $stub->doSomething());
```

### Data Providers

Pass data to a test method (similar to parameterized tests).

```php
#[DataProvider('additionProvider')]
public function testAdd(int $a, int $b, int $expected): void { ... }
```

## Best Practices (2025)

**Do**:

- **Use Strict Assertions**: `$this->assertSame()` checks types (===), whereas `assertEquals` is loose (==). Strict is safer.
- **Use Namespaces**: Organize tests `Tests\Unit\UserTest` matching `App\Models\User`.
- **PHPUnit 11 features**: Use the new attributes `#[Test]` instead of `/** @test */` annotations if on PHP 8.2+.

**Don't**:

- **Don't test private methods**: Test the public API. If a private method is complex, extract it to a new class.

## References

- [PHPUnit Documentation](https://phpunit.de/documentation.html)
