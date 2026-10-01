---
name: php
description: Expert modern PHP (PHP 8.2/8.3+) assistance covering strict typing, attributes, fibers, Composer, and OPcache. Use when building Laravel/Symfony web apps, developing REST APIs, or optimizing PHP workloads.
---

# PHP

A popular specific-purpose scripting language that is especially suited to web development.

## When to Use

- **Modern Full-Stack Web Development**: Powering high-velocity Laravel and Symfony web backends with rich ecosystem tooling.
- **Enterprise CMS Platforms**: Building and extending WordPress, Drupal, and headless CMS architectures.
- **High-Performance Asynchronous APIs (FrankenPHP / Swoole)**: Running persistent in-memory PHP workers serving thousands of requests per second.
- **Rapid CRUD & API Engineering**: Building robust APIs quickly with PHP 8.3/8.4 typed properties, attributes, and match expressions.

## Quick Start

```php
<?php
$name = "World";
echo "Hello, $name!";

$colors = ["red", "green", "blue"];
foreach ($colors as $color) {
    echo $color . "<br>";
}
?>
```

## Core Concepts

### Modern Strict Typing & Constructor Promotion (PHP 8.2+)

Enforces strict scalar types, readonly classes, and promoted constructor properties:

```php
<?php
declare(strict_types=1);

namespace App\Domain;

final readonly class Order
{
    public function __construct(
        public string $id,
        public float $amount,
        public OrderStatus $status = OrderStatus::Pending,
        public \DateTimeImmutable $createdAt = new \DateTimeImmutable()
    ) {}
}

enum OrderStatus: string
{
    case Pending = 'PENDING';
    case Paid = 'PAID';
    case Shipped = 'SHIPPED';
}
```

### Expressive `match` Expressions & First-Class Callables

Replaces verbose `switch` statements with strict type comparison and returned values:

```php
function getDiscountPercentage(OrderStatus $status): float
{
    return match ($status) {
        OrderStatus::Pending => 0.0,
        OrderStatus::Paid    => 0.05,
        OrderStatus::Shipped => 0.10,
    };
}
```

### Modern Fiber-Based Concurrency & Persistent Runtimes

Runs concurrent fibers and persistent memory workers with FrankenPHP:

```php
$fiber = new Fiber(function (): void {
    $value = Fiber::suspend('paused');
    echo "Resumed with: $value
";
});

$result = $fiber->start();
$fiber->resume('active');
```

## Common Patterns

### Constructor Promotion and Readonly Properties

**Problem**: Verbose boilerplate required to declare, type, and assign class properties.

**Solution**:
Use PHP 8 constructor property promotion with `readonly`:

```php
<?php
declare(strict_types=1);

readonly class UserProfile
{
    public function __construct(
        public int $id,
        public string $name,
        public string $email,
        public array $roles = ['user']
    ) {}
}

$user = new UserProfile(1, 'Jane', 'jane@example.com');
echo $user->name;
```

## Best Practices

**Do**:

- Always Add `declare(strict_types=1);`: Enforce strict scalar type checking at the top of every single PHP file.
- Use PHPStan or Psalm at Level 8+: Integrate static analysis in CI to eliminate type bugs and undefined method calls.
- Deploy with FrankenPHP or Octane: Maximize throughput by serving applications via persistent workers in production.
- Use `DateTimeImmutable`: Prevent accidental time-mutation bugs by replacing mutable `DateTime` with `DateTimeImmutable`.

**Don't**:

- Use raw superglobals (`$_POST`, `$_GET`): Validate incoming parameters via framework Request classes and validation schemas.
- Use weak comparison (`==`): Always use strict equality (`===`) to avoid unintended type coercion.
- Ignore Composer lock files: Always commit `composer.lock` and run `composer install --no-dev --optimize-autoloader` in production.

## Troubleshooting

| Error                                                     | Cause                                                   | Solution                                                                          |
| :-------------------------------------------------------- | :------------------------------------------------------ | :-------------------------------------------------------------------------------- |
| `TypeError: Argument 1 passed must be of the type ...`    | Strict types enabled and caller passed mismatched type. | Cast argument explicitly or verify caller inputs.                                 |
| `Fatal error: Allowed memory size of ... bytes exhausted` | Script exceeded `memory_limit` loading large dataset.   | Use generators (`yield`) or increase `memory_limit` in `php.ini`.                 |
| `Class '...' not found`                                   | Autoloader not included or Composer autoloader stale.   | Add `require __DIR__ . '/vendor/autoload.php';` and run `composer dump-autoload`. |

## References

- [PHP.net](https://www.php.net/)
- [PHP The Right Way](https://phptherightway.com/)
