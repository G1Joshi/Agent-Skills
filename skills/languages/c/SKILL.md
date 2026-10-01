---
name: c
description: Expert C programming assistance covering pointers, manual memory management, struct layout, and POSIX APIs. Use when developing systems software, embedded firmware, high-performance libraries, or OS kernels.
---

# C

The foundational language for modern computing, operating systems, and embedded systems.

## When to Use

- **Operating System Kernels & Drivers**: Developing the Linux kernel, device drivers, and low-level firmware.
- **High-Performance Embedded Systems**: Microcontroller programming (ARM Cortex, RISC-V) with strict real-time memory constraints.
- **Foundational Infrastructure & Databases**: Powering core engines like SQLite, Redis, Nginx, and Python runtimes.
- **Hardware-Accelerated Audio / Video Codecs**: Building zero-overhead media codecs and DSP signal processing routines.

## Quick Start

```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

## Core Concepts

### Explicit Memory Management & Pointer Arithmetic

Direct manipulation of memory addresses, stack allocation, and heap lifetimes:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    size_t length;
    char *data;
} StringBuffer;

StringBuffer* buffer_create(const char *initial_str) {
    StringBuffer *buf = malloc(sizeof(StringBuffer));
    if (!buf) return NULL;

    buf->length = strlen(initial_str);
    buf->data = malloc(buf->length + 1);
    if (!buf->data) {
        free(buf);
        return NULL;
    }
    memcpy(buf->data, initial_str, buf->length + 1);
    return buf;
}

void buffer_free(StringBuffer *buf) {
    if (buf) {
        free(buf->data);
        free(buf);
    }
}
```

### Modern C Standards (C23 / C17) Features

C23 introduces standardized `bool`, `nullptr`, and `auto` type inference:

```c
// Modern C23 syntax
#include <stdbool.h>

int main(void) {
    bool is_active = true;
    void *ptr = nullptr; // C23 standardized nullptr
    return is_active ? 0 : 1;
}
```

### Memory Sanitizers (ASan & UBSan)

Instruments binary builds to detect buffer overflows, use-after-free, and undefined behavior at runtime:

```bash
# Compile with AddressSanitizer and UndefinedBehaviorSanitizer
gcc -std=c17 -Wall -Wextra -Werror -fsanitize=address,undefined -g -O1 main.c -o app
```

## Common Patterns

### Safe Dynamic Allocation with Cleanup Labels

**Problem**: Multi-step initialization with multiple `malloc` calls causes memory leaks if middle steps fail.

**Solution**:
Use single exit goto cleanup pattern for resource management:

```c
#include <stdlib.h>
#include <stdio.h>

int process_data(size_t n) {
    int *buf1 = malloc(n * sizeof(int));
    if (!buf1) return -1;

    char *buf2 = malloc(n * sizeof(char));
    if (!buf2) {
        free(buf1);
        return -1;
    }

    // Work with buffers
    int status = 0;

    free(buf2);
    free(buf1);
    return status;
}
```

## Best Practices

**Do**:

- Compile with Strict Warnings: Use `-Wall -Wextra -Wpedantic -Wconversion -Werror` to catch bugs at compile time.
- Run AddressSanitizer and Valgrind: Test test binaries under ASan to eliminate memory leaks and buffer overruns before release.
- Use `snprintf` Instead of `sprintf`: Always specify buffer boundaries to prevent catastrophic stack-based buffer overflows.
- Initialize Every Variable: Avoid undefined behavior by zero-initializing structs (`StringBuffer buf = {0};`).

**Don't**:

- Use `gets()` or unbounded `strcpy()`: Legacy unbounded string functions are major attack vectors for remote code execution.
- Access memory after calling `free()`: Set pointers to `NULL` after freeing to prevent use-after-free exploits.
- Assume integer overflow wraps safely: Signed integer overflow is undefined behavior in C; check limits explicitly.

## Troubleshooting

| Error                              | Cause                                                         | Solution                                                           |
| :--------------------------------- | :------------------------------------------------------------ | :----------------------------------------------------------------- |
| `Segmentation fault`               | Null pointer dereference, buffer overflow, or use-after-free. | Compile with AddressSanitizer: `gcc -fsanitize=address -g main.c`. |
| `double free or corruption`        | Calling `free()` twice on the same memory pointer.            | Set pointer to `NULL` immediately after calling `free(ptr)`.       |
| `implicit declaration of function` | Missing header file `#include` declaring the target function. | Include the header file matching the C standard library function.  |

## References

- [C Reference](https://en.cppreference.com/w/c)
