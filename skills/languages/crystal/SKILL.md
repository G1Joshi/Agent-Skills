---
name: crystal
description: Expert Crystal programming assistance covering static typing, LLVM compilation, C bindings, and fibers. Use when writing ultra-fast compiled programs with elegant Ruby-like syntax.
---

# Crystal

Crystal compiles to native code (using LLVM) but looks exactly like Ruby. v1.12 continues improving **Windows support** and parallelism.

## When to Use

- **High-Performance Ruby-Like Applications**: Building compiled native binaries with Ruby-like elegance and C-like execution speed.
- **Fast Microservices & APIs (Kemal / Lucky)**: Serving high-throughput REST and WebSocket APIs with sub-millisecond response latencies.
- **CLI Tool Development**: Compiling single, self-contained standalone executable binaries without external runtime dependencies.
- **Concurrent Network Processing**: Handling thousands of concurrent connections using lightweight CSP fibers and channels.

## Quick Start

```crystal
# Define typed struct with automatic getters
record User, id : Int32, name : String, email : String

users = [
  User.new(1, "Alice", "alice@example.com"),
  User.new(2, "Bob", "bob@example.com")
]

users.each do |user|
  puts "#{user.name} (#{user.email})"
end
```

## Core Concepts

#Compile-Time Static Type Inference

Provides the syntax of Ruby with the type-safety of a compiled language without redundant type annotations:

```crystal
# Crystal infers types at compile time
def compute_discount(price, coupon = nil)
  if coupon == "VIP"
    price * 0.8
  else
    price
  end
end

puts compute_discount(100)       # 100
puts compute_discount(100, "VIP") # 80.0
```

#Concurrency via Fibers & Channels (CSP)

Lightweight cooperative green threads scheduled cooperatively on an event loop:

```crystal
channel = Channel(String).new

# Spawn lightweight fiber
spawn do
  sleep 0.5.seconds
  channel.send("Processing complete")
end

puts "Waiting for background fiber..."
message = channel.receive
puts "Received: #{message}"
```

#C-Binding Interoperability

Calls external C dynamic libraries natively with zero wrapper boilerplate:

```crystal
@[Link("m")]
lib LibM
  fun sqrt(x : Float64) : Float64
end

puts LibM.sqrt(144.0) # 12.0
```

## Common Patterns

### Fast C Library Interoperability

**Problem**: Calling native C libraries without writing complex wrapper boilerplate.

**Solution**:
Declare `lib` binding directly in Crystal:

```crystal
lib LibC
  fun puts(str : UInt8*) : Int32
  fun getpid : Int32
end

pid = LibC.getpid
puts "Current process ID: #{pid}"
```

## Best Practices (2026)

**Do**:

- **Build with `--release` for Production**: Always pass `--release` to enable aggressive LLVM dead-code elimination and inlining.
- **Use Non-Nilable Types**: Benefit from Crystal's compile-time null safety; handle `nil` explicitly with `.try` or `if val`.
- **Use Static Builds via Docker/Alpine**: Compile fully static Linux binaries using `docker run --rm -v $(pwd):/workspace crystallang/crystal:latest-alpine`.
- **Structure Concurrency Around Channels**: Share memory by communicating through typed channels rather than shared mutable pointers.

**Don't**:

- **Don't use `Object#as` blindly**: Unchecked type assertions cause runtime type cast exceptions; use pattern matching or `.is_a?`.
- **Don't perform blocking CPU-bound loops in fibers**: Cooperatively yield CPU control using `Fiber.yield` in tight loops.
- **Don't deploy debug builds**: Non-release Crystal binaries are significantly larger and order of magnitude slower.

## Troubleshooting

| Error                             | Cause                                                | Solution                                                            |
| :-------------------------------- | :--------------------------------------------------- | :------------------------------------------------------------------ |
| `type must be (Type), not (Type   | Nil)`                                                | Nil-checking missing before accessing methods on nullable variable. | Use `var.not_nil!` or guard with `if var`. |
| `Can't use Type as type in union` | Incompatible types combined without common ancestor. | Explicitly annotate union type or cast with `.as(TargetType)`.      |
| `undefined constant in shard`     | Missing dependency or `shards.yml` not resolved.     | Run `shards install` to install project dependencies.               |

## References

- [Crystal Lang](https://crystal-lang.org/)
