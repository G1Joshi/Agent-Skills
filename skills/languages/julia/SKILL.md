---
name: julia
description: Expert Julia assistance covering numerical computing, multiple dispatch, broadcasting, and parallel computing. Use when developing scientific models, machine learning, physics simulations, or differential equations.
---

# Julia

Julia is a high-performance dynamic programming language designed for scientific computing, data analysis, and numerical algorithms with speed approaching C.

## When to Use

- **High-Performance Scientific Computing & Numerical Math**: Solving differential equations, linear algebra, and scientific simulations at C-like speeds.
- **Machine Learning & Differentiable Programming**: Training deep learning architectures using native automatic differentiation (Flux.jl / Zygote.jl).
- **Solving the "Two-Language Problem"**: Writing both high-level mathematical prototypes and high-speed production algorithms in the same language.
- **Multi-Threaded & Distributed Parallelism**: Utilizing CPU multi-threading, GPU acceleration (CUDA.jl), and distributed cluster memory.

## Quick Start

```julia
# Vectorized matrix math with broadcasting syntax (.)
function compute_loss(y_true, y_pred)
    return sum((y_true .- y_pred) .^ 2) / length(y_true)
end

y_true = [1.0, 2.0, 3.0]
y_pred = [1.1, 1.9, 3.2]
println("Mean Squared Error: ", compute_loss(y_true, y_pred))
```

## Core Concepts

### Multiple Dispatch Paradigm

Functions choose execution methods based on the runtime types of all arguments, not just the first receiver:

```julia
# Defining multi-dispatch methods
abstract type Shape end
struct Circle <: Shape radius::Float64 end
struct Rectangle <: Shape width::Float64; height::Float64 end

# Dispatches dynamically to exact matching method
area(c::Circle) = π * c.radius^2
area(r::Rectangle) = r.width * r.height

println("Circle Area: ", area(Circle(5.0)))
println("Rectangle Area: ", area(Rectangle(4.0, 6.0)))
```

### JIT Compilation (LLVM) & Type Specialization

The Julia compiler specializes machine code for the exact types encountered at runtime:

```julia
function compute_mandelbrot(max_iter::Int, c::Complex{Float64})
    z = c
    for i in 1:max_iter
        if abs2(z) > 4.0
            return i
        end
        z = z^2 + c
    end
    return max_iter
end
# Compiles to optimized SIMD machine code upon first execution!
```

### Composable Package Ecosystem (Broadcast & Metaprogramming)

The dot syntax (`.`) vectorizes any function over arrays automatically:

```julia
numbers = [1.0, 4.0, 9.0, 16.0]
# Broadcast sqrt over entire array
square_roots = sqrt.(numbers) # [1.0, 2.0, 3.0, 4.0]
```

## Common Patterns

### High-Performance Type-Stable Functions

**Problem**: Type instability causes Julia to fall back to slow dynamic dispatch inside inner loops.

**Solution**:
Ensure return types can be inferred purely from argument types:

```julia
function sum_positive(arr::Vector{Float64})::Float64
    acc = 0.0 # Float literal ensures type stability
    @inbounds for x in arr
        if x > 0.0
            acc += x
        end
    end
    return acc
end
```

## Best Practices

**Do**:

- Write Type-Stable Functions: Ensure functions return values of predictable types regardless of input branch values to maintain LLVM speed.
- Inspect Code Performance with `@benchmark` and `@code_warntype`: Use BenchmarkTools.jl and `@code_warntype` to detect type instabilities.
- Pre-Allocate Memory for Inner Loops: Avoid reallocating arrays inside tight numerical loops; mutate in place using `.!` syntax.
- Leverage Built-In Multithreading: Run with `julia --threads auto` and parallelize loops using `Threads.@threads for ...`.

**Don't**:

- Use untyped global variables in performance-critical code: Untyped globals prevent compiler optimization; declare them with `const`.
- Create abstract type fields in structs: Specify concrete type parameters (`struct Container{T} data::T end`) to avoid boxing.
- Benchmark functions with global inputs: Always benchmark inside functions or interpolate globals (`@btime my_func($global_val)`).

## Troubleshooting

| Error                                             | Cause                                                               | Solution                                                                         |
| :------------------------------------------------ | :------------------------------------------------------------------ | :------------------------------------------------------------------------------- |
| `MethodError: no method matching ...(::Type)`     | No matching method overload exists for the provided argument types. | Inspect available methods using `methods(func_name)` and check type annotations. |
| `Slow execution in inner loops`                   | Type instability or global variable access in loop body.            | Use `@code_warntype func(...)` to identify type instabilities (red flags).       |
| `BoundsError: attempt to access ... at index [0]` | Julia uses 1-based indexing by default.                             | Access first element with index `1` instead of `0`.                              |

## References

- [Julia Lang](https://julialang.org/)
