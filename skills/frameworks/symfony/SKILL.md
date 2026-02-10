---
name: symfony
description: Symfony PHP framework with reusable components. Use for PHP applications.
---

# Symfony

Symfony v7.1 (2025) is the bedrock of modern PHP (Drupal, Laravel components). It emphasizes **Attributes** (Annotations) and strict typing.

## When to Use

- **Enterprise PHP**: Complex business logic, long-term stability (LTS).
- **Components**: Using standalone libraries (Console, HttpFoundation) in other apps.
- **DDD**: Well-suited for complex domain modeling.

## Core Concepts

### Dependency Injection

The Container is central. Auto-wiring is default.

### Bundles

Plugin system.

### Attributes

`#[Route('/api', name: 'api')]` replaces YAML/Annotation configs.

## Best Practices (2025)

**Do**:

- **Use Maker Bundle**: `php bin/console make:controller`.
- **Use AssetMapper**: No Webpack/Node.js required for simple assets.
- **Use Messenger**: For async message bus (queues).

**Don't**:

- **Don't use YAML for Services**: Use PHP attributes and autowiring.

## References

- [Symfony Documentation](https://symfony.com/)
