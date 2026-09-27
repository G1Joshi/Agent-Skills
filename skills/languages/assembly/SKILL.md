---
name: assembly
description: Expert x86-64 and ARM64 assembly assistance covering registers, calling conventions, stack frames, and inline asm. Use when writing low-level code, optimizing hot loops, or reverse engineering binaries.
---

# Assembly

Low-level language with a very strong correspondence between the instruction in the language and the architecture's machine code instructions.

## When to Use

- **Low-Level Hardware & OS Kernel Programming**: Writing bootloaders, CPU context switches, interrupt handlers, and page table setup.
- **Micro-Architectural SIMD Vector Optimization**: Crafting hand-tuned AVX-512, Neon, or SSE assembly kernels for game physics and matrix multiplication.
- **Reverse Engineering & Exploit Analysis**: Disassembling binary executables to audit firmware, analyze malware, or debug compiler crashes.
- **Embedded Bare-Metal Firmware**: Direct CPU register manipulation on microcontrollers without operating system abstractions.

## Quick Start

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

#CPU Registers & Memory Addressing Modes (x86-64 / ARM64)

Registers hold immediate state for execution; addressing modes compute memory operands:

```nasm
; x86-64 NASM: Moving data and base-index-scale-displacement addressing
mov rax, 42                     ; Immediate to register
mov rbx, [rsp + 16]             ; Base + displacement
mov rcx, [rdi + rsi * 8 + 32]   ; Base + index * scale + displacement
```

#The System V AMD64 Calling Convention

Governs how functions receive parameters and return values in Linux and macOS:

| Register   | Argument Role                              |
| :--------- | :----------------------------------------- |
| `rdi`      | 1st function argument                      |
| `rsi`      | 2nd function argument                      |
| `rdx`      | 3rd function argument                      |
| `rcx`      | 4th function argument                      |
| `r8`, `r9` | 5th and 6th function arguments             |
| `rax`      | Function return value (and syscall number) |

```nasm
; Direct 64-bit Linux syscall (sys_write = 1)
mov rax, 1          ; syscall: sys_write
mov rdi, 1          ; file descriptor: stdout (1)
mov rsi, msg        ; pointer to buffer
mov rdx, 14         ; count (bytes)
syscall             ; invoke kernel
```

#SIMD Vectorization (AVX-512 / AVX2)

Processes multiple data elements simultaneously across 256-bit or 512-bit vector registers:

```nasm
; Add 8 single-precision floats in parallel using AVX
vmovups ymm0, [rdi]        ; Load 8 floats into YMM0
vmovups ymm1, [rsi]        ; Load 8 floats into YMM1
vaddps  ymm2, ymm0, ymm1   ; YMM2 = YMM0 + YMM1 in single clock cycle
vmovups [rdx], ymm2        ; Store result
```

## Common Patterns

### Syscall Invocation with Proper Register Arguments (Linux x86-64)

**Problem**: Invoking kernel system calls directly without C runtime dependencies.

**Solution**:
Load syscall number into `rax` and arguments in `rdi, rsi, rdx, r10, r8, r9`:

```nasm
section .text
global _start

_start:
    ; sys_write(fd: 1, buf: msg, len: 14)
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, 14
    syscall

    ; sys_exit(code: 0)
    mov rax, 60
    xor rdi, rdi
    syscall

section .data
msg db "Hello, Assembly", 10
```

## Best Practices (2026)

**Do**:

- **Preserve Callee-Saved Registers**: Always preserve `rbx`, `rsp`, `rbp`, `r12`-`r15` across function boundaries.
- **Maintain 16-Byte Stack Alignment**: Ensure `rsp` is 16-byte aligned before issuing `call` instructions to avoid segmentation faults in libc.
- **Use Inline Assembly Sparingly in C/Rust**: Rely on compiler intrinsic headers (`<immintrin.h>`) whenever possible instead of raw inline assembly.
- **Comment Every Assembly Routine Thoroughly**: Document input register assumptions, output registers, and modified flags.

**Don't**:

- **Don't rewrite algorithms in assembly without profiling**: Modern LLVM/GCC compilers generate near-optimal machine code for standard loops.
- **Don't ignore processor architecture differences**: x86-64 CISC code is incompatible with ARM64 RISC instruction sets.
- **Don't bypass platform calling conventions**: Mixing calling conventions causes silent stack corruption and elusive crashes.

## Troubleshooting

| Error                                                 | Cause                                                                   | Solution                                                             |
| :---------------------------------------------------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------- |
| `Segmentation fault (core dumped)`                    | Dereferencing invalid pointer or misaligned stack before `call`.        | Ensure stack pointer `rsp` is 16-byte aligned before function calls. |
| `Undefined reference to '_start'`                     | Linker entrypoint missing or `global _start` not exported.              | Declare `global _start` or compile with `gcc -nostartfiles`.         |
| `relocation R_X86_64_32S against ... can not be used` | Position-independent executable (PIE) requires RIP-relative addressing. | Use `[rel symbol]` addressing in NASM.                               |

## References

- [x86 Assembly Guide](https://www.cs.virginia.edu/~evans/cs216/guides/x86.html)
