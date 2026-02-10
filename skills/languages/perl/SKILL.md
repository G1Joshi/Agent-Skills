---
name: perl
description: Perl text processing and scripting with regular expressions. Use for .pl files.
---

# Perl

Perl 5.40 (2024) introduced a **native `try/catch`** and the `__CLASS__` keyword. It remains unbeatable for text processing one-liners.

## When to Use

- **Text Processing**: Regex engine is the gold standard.
- **Sysadmin**: Legacy scripts on every Unix system.
- **Bioinformatics**: Massive existing codebases (Bioperl).

## Core Concepts

### Sigils

`$scalar`, `@array`, `%hash`. Visual typing.

### Context

Scalar vs List context. `my $len = @arr` (count) vs `my. ($first) = @arr` (element).

### CPAN

The "Comprehensive Perl Archive Network". The original package repository.

## Best Practices (2025)

**Do**:

- **Use `v5.40`**: Enable new features `use v5.40;`.
- **Use `strict` and `warnings`**: Mandatory for sanity.
- **Use `App::cpanminus`**: Modern installer.

**Don't**:

- **Don't write "write-only" code**: value readability over golf.

## References

- [Perl.org](https://www.perl.org/)
