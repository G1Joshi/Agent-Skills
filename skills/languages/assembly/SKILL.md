---
name: assembly
description: Assembly language for low-level system and embedded programming. Use for .asm files.
---

# Assembly

Low-level language with a very strong correspondence between the instruction in the language and the architecture's machine code instructions.

## When to Use

- Operating System Kernels
- Embedded Systems / Microcontrollers
- Reverse Engineering
- Extreme optimization (rarely needed today)

## Quick Start (x86_64 Linux)

```assembly
section .data
    msg db "Hello, World!", 0xa
    len equ $ - msg

section .text
    global _start

_start:
    mov rax, 1      ; write syscall
    mov rdi, 1      ; stdout
    mov rsi, msg    ; buffer
    mov rdx, len    ; length
    syscall

    mov rax, 60     ; exit syscall
    xor rdi, rdi    ; exit code 0
    syscall
```

## Core Concepts

### Registers

Small, fast storage locations directly in the CPU (e.g., RAX, RBX, RIP).

### Instructions

Commands executed by the CPU (MOV, ADD, SUB, JMP).

### Stack

Region of memory for storing local variables and return addresses (USH, POP).

## Best Practices

**Do**:

- Use comments liberally (assembly is hard to read)
- Follow calling conventions (e.g., System V AMD64 ABI)
- Use descriptive labels

**Don't**:

- Hand-optimize unless you beat the compiler (unlikely)
- Ignore alignment requirements

## References

- [x86 Assembly Guide](https://www.cs.virginia.edu/~evans/cs216/guides/x86.html)
