---
name: zig
description: Expert Zig systems programming assistance covering comptime code execution, manual memory allocators, C interop, and cross-compilation. Use when writing low-level systems software, embedded apps, or high-performance libraries.
---

# Zig

Zig is a modern systems programming language offering manual memory management, compile-time code execution (`comptime`), and a built-in cross-compiling C/C++ toolchain.

## When to Use

- **Low-Level Systems & Kernel Development**: Writing bare-metal kernels, embedded device software, hypervisors, and audio engines.
- **Drop-in C/C++ Compiler Toolchain**: Utilizing `zig cc` and `zig c++` for instant, cross-compilation without external dependencies.
- **Explicit Memory Allocation & Safety**: High-performance software demanding complete control over allocations without hidden heap usage.
- **Compile-Time Metaprogramming (Comptime)**: Writing generics, serialization, and type-level algorithms without macro systems or templates.

## Quick Start

```zig
const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello from Zig!
", .{});
}
```

## Core Concepts

### Explicit Memory Allocation with GeneralPurposeAllocator

Zero hidden allocations—every data structure requires an explicit allocator:

```zig
const std = @import("std");

pub fn main() !void {
    // Standard debug memory allocator with leak detection
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer {
        const check = gpa.deinit();
        if (check == .leak) std.debug.print("Memory leak detected!
", .{});
    }
    const allocator = gpa.allocator();

    // Dynamically allocated array list
    var list = std.ArrayList(u32).init(allocator);
    defer list.deinit();

    try list.append(10);
    try list.append(20);
    try list.append(30);

    for (list.items) |item| {
        std.debug.print("Item: {d}
", .{item});
    }
}
```

### Comptime Generics & Metaprogramming

Compile-time code execution replacing C++ templates and C macros:

```zig
const std = @import("std");

// Generic Queue data structure generated at compile-time
pub fn Queue(comptime T: type) type {
    return struct {
        const Self = @this();
        items: std.ArrayList(T),

        pub fn init(allocator: std.mem.Allocator) Self {
            return Self{
                .items = std.ArrayList(T).init(allocator),
            };
        }

        pub fn deinit(self: *Self) void {
            self.items.deinit();
        }

        pub fn push(self: *Self, value: T) !void {
            try self.items.append(value);
        }

        pub fn pop(self: *Self) ?T {
            if (self.items.items.len == 0) return null;
            return self.items.orderedRemove(0);
        }
    };
}
```

### Error Handling, Defer & Errdefer

Deterministic resource management and lightweight error unions:

```zig
const std = @import("std");

const FileError = error{
    AccessDenied,
    FileNotFound,
    DiskFull,
};

fn openAndProcessFile(allocator: std.mem.Allocator, filename: []const u8) !void {
    const buffer = try allocator.alloc(u8, 1024);
    // defer runs unconditionally when exiting scope
    defer allocator.free(buffer);

    var file = std.fs.cwd().openFile(filename, .{}) catch |err| switch (err) {
        error.FileNotFound => return FileError.FileNotFound,
        error.AccessDenied => return FileError.AccessDenied,
        else => return error.DiskFull,
    };
    defer file.close();

    // errdefer only runs if an error is returned later in the function
    errdefer std.debug.print("Error occurred while reading file: {s}
", .{filename});

    _ = try file.readAll(buffer);
}
```

## Common Patterns

### Explicit Memory Allocation with Defer Cleanup

**Problem**: Hidden allocations in language runtimes make memory leaks difficult to identify and fix.

**Solution**:
Pass explicit allocator parameter and defer cleanup immediately:

```zig
const std = @import("std");

pub fn createBuffer(allocator: std.mem.Allocator, size: usize) ![]u8 {
    const buf = try allocator.alloc(u8, size);
    errdefer allocator.free(buf);

    @memset(buf, 0);
    return buf;
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const buffer = try createBuffer(allocator, 1024);
    defer allocator.free(buffer);
}
```

## Best Practices

**Do**:

- Always pass explicit `std.mem.Allocator` to functions and structs that perform dynamic allocation.
- Use `defer` for cleanup immediately following successful resource acquisition, and `errdefer` for failure rollbacks.
- Leverage `zig test` with built-in leak tracking to test functions and algorithms thoroughly.
- Take advantage of `zig build` as a unified, portable build system replacing Make and CMake.

**Don't**:

- Use `@ptrCast` or `@alignCast` without verifying alignment and layout safety.
- Ignore error return values; handle with `try`, `catch`, or explicit pattern matching.
- Allocate inside tight inner loops; pass pre-allocated buffers or slice views.

## Troubleshooting

| Error                                     | Cause                                                | Solution                                                              |
| :---------------------------------------- | :--------------------------------------------------- | :-------------------------------------------------------------------- |
| `error: memory leak detected`             | GPA allocator detected memory not freed at shutdown. | Ensure every `allocator.alloc` has a matching `defer allocator.free`. |
| `error: use of undeclared identifier`     | Symbol misspelled or missing `@import`.              | Check spelling and verify imported namespace.                         |
| `error: expected type '...', found '...'` | Static type mismatch in expression.                  | Use explicit cast `@as(TargetType, val)` or `@intCast`.               |

## References

- [Zig Documentation](https://ziglang.org/)
