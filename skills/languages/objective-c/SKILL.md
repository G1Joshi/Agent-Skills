---
name: objective-c
description: Objective-C for legacy iOS/macOS development with manual memory. Use for .m files.
---

# Objective-C

Objective-C is in **maintenance mode**. New features are rare, but it powers the Apple ecosystem's foundation. It allows mixing C++ (`.mm`) loosely.

## When to Use

- **Legacy iOS/macOS**: Maintaining apps created before 2014.
- **C++ Interop**: Obj-C++ is often the bridge between C++ engines and Swift.
- **Runtime Swizzling**: Dynamic method replacement (used by Analytics SDKs).

## Core Concepts

### Message Passing

`[object method:argument]`. Dynamic binding at runtime.

### ARC

Automatic Reference Counting. (Retain/Release).

### Headers

`.h` (interface) and `.m` (implementation).

## Best Practices (2025)

**Do**:

- **Use Nullability Annotations**: `nullable`, `nonnull` to aid Swift interop.
- **Use Modern Syntax**: `@[@"a", @"b"]` for arrays.
- **Migrate to Swift**: New features should be written in Swift.

**Don't**:

- **Don't use manual retain/release**: Always ensure ARC is on.

## References

- [Apple Developer Documentation](https://developer.apple.com/)
