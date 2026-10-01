---
name: cpp
description: Expert modern C++ (C++17/C++20/C++23) assistance covering RAII, smart pointers, template metaprogramming, STL containers, move semantics, and memory profiling. Use when developing high-performance native systems, low-latency algorithms, game engines, or embedded C++ codebases.
---

# C++

Modern C++ development with smart pointers, RAII, and performance optimization.

## When to Use

- **High-Performance Game Engine & Graphics Development**: Unreal Engine, Vulkan, DirectX 12, and real-time ray tracing pipelines.
- **Low-Latency Quantitative Finance**: Writing high-frequency trading (HFT) engines with microsecond and nanosecond execution SLAs.
- **Systems & Database Infrastructure**: Building foundational engines (Chromium, ClickHouse, RocksDB, MongoDB).
- **Embedded & Autonomous Robotics**: ROS 2, computer vision pipelines, and self-driving automotive control systems.

## Quick Start

```cpp
#include <memory>
#include <string>
#include <vector>

class User {
public:
    User(std::string name, std::string email)
        : name_(std::move(name)), email_(std::move(email)) {}

    const std::string& name() const { return name_; }
    const std::string& email() const { return email_; }

private:
    std::string name_;
    std::string email_;
};

auto user = std::make_unique<User>("John", "john@example.com");
```

## Core Concepts

### RAII & Modern Smart Pointers (C++20/C++23)

Resource Acquisition Is Initialization (RAII) ties resource management directly to object lifetime:

```cpp
#include <iostream>
#include <memory>
#include <string>

class DatabaseConnection {
public:
    explicit DatabaseConnection(std::string conn_str) { std::cout << "Connected
"; }
    ~DatabaseConnection() { std::cout << "Closed connection safely
"; }
    void query(std::string sql) { std::cout << "Executing: " << sql << "
"; }
};

void execute_task() {
    // std::unique_ptr automatically destructs and frees resource when exiting scope
    auto conn = std::make_unique<DatabaseConnection>("postgres://localhost");
    conn->query("SELECT 1;");
} // conn goes out of scope here; destructor executes automatically
```

### Move Semantics & `std::move`

Transfers ownership of heavy heap resources without expensive deep memory copying:

```cpp
#include <vector>

std::vector<int> generate_data() {
    std::vector<int> large_vector(1'000'000, 42);
    return large_vector; // Move semantics (or RVO) avoids copying 1M integers
}
```

### C++20 Concepts & Constexpr Metaprogramming

Constrains template arguments with readable compile-time predicates:

```cpp
#include <concepts>

template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T calculate_mean(T a, T b) {
    return (a + b) / 2;
}
```

## Common Patterns

### Structured Bindings & Optional Returns

**Problem**: Returning multiple values safely without error-prone output pointers or boilerplate structs.

**Solution**:

```cpp
// Structured bindings (C++17)
auto [name, age] = std::make_pair("John", 25);
for (const auto& [key, value] : map) { /* ... */ }

// std::optional (C++17)
std::optional<User> findUser(int id) {
    if (exists) return User{...};
    return std::nullopt;
}

// Concepts (C++20)
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<Numeric T>
T add(T a, T b) { return a + b; }

// Ranges (C++20)
auto result = numbers
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * 2; });
```

### RAII Pattern

**Problem**: Manual resource management risks leaks when exceptions interrupt execution flow.

**Solution**:

```cpp
class FileHandle {
public:
    explicit FileHandle(const char* path)
        : file_(std::fopen(path, "r")) {
        if (!file_) throw std::runtime_error("Cannot open file");
    }

    ~FileHandle() { if (file_) std::fclose(file_); }

    // Delete copy
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // Allow move
    FileHandle(FileHandle&& other) noexcept : file_(other.file_) {
        other.file_ = nullptr;
    }

private:
    FILE* file_;
};
```

## Best Practices

**Do**:

- Use Smart Pointers (`std::unique_ptr`, `std::shared_ptr`): Completely avoid raw `new` and `delete` expressions.
- Pass Heavy Read-Only Objects by `const&`: Prevent accidental copy overhead (`void process(const std::string& data)`).
- Use `std::string_view` and `std::span`: Reference continuous memory without copying or allocating heap strings.
- Enable Clang-Tidy & AddressSanitizer in CI: Enforce modern standards and catch memory leaks automatically.

**Don't**:

- Use C-style casts (`(int)x`): Use explicit C++ casts (`static_cast`, `reinterpret_cast`) to retain compiler safety checks.
- Return references to local stack variables: Returning local references causes dangling pointers and immediate undefined behavior.
- Use macros (`#define`) for constants: Use `constexpr` or `inline constexpr` variables.

## Troubleshooting

| Error              | Cause                           | Solution                       |
| ------------------ | ------------------------------- | ------------------------------ |
| Segmentation fault | Null pointer or buffer overflow | Use sanitizers, smart pointers |
| Memory leak        | Missing delete                  | Use RAII, smart pointers       |
| Undefined behavior | Dangling reference              | Ensure lifetime validity       |

## References

- [C++ Reference](https://en.cppreference.com/)
- [ISO C++ Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
