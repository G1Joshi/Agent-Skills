---
name: php
description: PHP 8+ web development with Composer, attributes, and modern frameworks. Use for .php files.
---

# PHP

A popular specific-purpose scripting language that is especially suited to web development.

## When to Use

- Server-side web development
- WordPress / CMS development
- Content-heavy sites
- Rapid prototyping

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

### Arrays

PHP arrays are versatile (serve as lists, maps, stacks, etc.).

```php
$user = [
    "id" => 1,
    "name" => "Foo"
];
```

### Superglobals

Built-in variables available in all scopes (`$_GET`, `$_POST`, `$_SESSION`).

### OOP

PHP 8+ has robust object-oriented features including properties, attributes, and match expressions.

## Best Practices

**Do**:

- Use Composer for dependency management
- Type hint function arguments and return types
- Use PDO for database access (prepared statements)
- Follow PSR standards (PSR-12)

**Don't**:

- Use `mysql_` functions (deprecated/removed)
- Trust user input (sanitize/validate)
- leave `display_errors` on in production

## References

- [PHP.net](https://www.php.net/)
- [PHP The Right Way](https://phptherightway.com/)
