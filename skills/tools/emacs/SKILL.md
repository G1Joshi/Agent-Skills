---
name: emacs
description: Expert GNU Emacs assistance covering init.el, Elisp, Org-mode, Magit, LSP Mode, and packages. Use when customizing Emacs, writing Elisp, and operating extensible keyboard-centric developer environments.
---

# GNU Emacs

GNU Emacs is an extensible, customizable text editor and computing environment featuring built-in LSP integration (Eglot), Tree-sitter syntax parsing, and native compilation.

## When to Use

- **Extensible & Fully Customizable Text Editing**: Tailoring an entire computing and editing environment in Emacs Lisp (Elisp).
- **Org Mode Productivity & Note-Taking**: Authoring structured notes, agendas, literate programming, and task management.
- **Modal Editing with Evil Mode (Doom Emacs)**: Combining Vim modal muscle memory with Emacs extensibility.
- **Language Server Protocol (LSP) with Eglot**: High-speed, built-in code navigation, completion, and diagnostic checking.

## Quick Start

```elisp
;; ~/.emacs.d/init.el - Essential modern starter configuration
(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))

(setq inhibit-startup-message t)
(global-display-line-numbers-mode t)
```

## Core Concepts

### Modern Emacs Configuration with use-package & Eglot

Configuring modern package management and built-in LSP:

```elisp
;; ~/.emacs.d/init.el
(require 'package)
(setq package-archives '(("melpa" . "https://melpa.org/packages/")
                         ("gnu" . "https://elpa.gnu.org/packages/")))
(package-initialize)

;; Install and configure use-package
(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))
(require 'use-package)
(setq use-package-always-ensure t)

;; Built-in Eglot LSP configuration
(use-package eglot
  :ensure nil ; Built into Emacs 29+
  :hook ((rust-ts-mode . eglot-ensure)
         (python-ts-mode . eglot-ensure)
         (typescript-ts-mode . eglot-ensure))
  :config
  (setq eglot-autoshutdown t))

;; Fast completion with Corfu and Vertico
(use-package vertico
  :init
  (vertico-mode 1))

(use-package corfu
  :init
  (global-corfu-mode 1))
```

### Org Mode Literate Programming

Executing embedded code blocks within documents:

```org
* Technical Report
#+BEGIN_SRC python :results output
data = [12, 45, 67, 89, 34]
print(f"Average: {sum(data)/len(data):.2f}")
#+END_SRC

#+RESULTS:
: Average: 49.40
```

### Magit: Git Porcelain for Emacs

Keyboard-driven Git operations (`M-x magit-status`):

- `s`: Stage file or hunk
- `c c`: Commit staged changes
- `P u`: Push to upstream remote
- `b b`: Switch branch interactively

## Common Patterns

### LSP Mode with Eglot (Built-in) for Fast Code Intelligence

**Problem**: Slow auto-completion and language server lag in heavy community frameworks.

**Solution**:
Use built-in lightweight `eglot`:

```elisp
;; Enable Eglot for Rust, Python, and TypeScript modes
(use-package eglot
  :ensure t
  :hook ((rust-mode . eglot-ensure)
         (python-mode . eglot-ensure)
         (typescript-ts-mode . eglot-ensure)))
```

## Best Practices

**Do**:

- Target Emacs 29/30+ with native compilation (`--with-native-compilation`) and built-in Tree-sitter modes.
- Use `use-package` with `:defer t` to keep Emacs startup time under 0.5 seconds.
- Prefer built-in `eglot` over heavy external LSP packages for low memory overhead.
- Use Magit for Git management; it is widely considered the best Git interface in the industry.

**Don't**:

- Add package installation logic without `:ensure t` or guard checks in `use-package`.
- Leave garbage collection thresholds set too low; bump `gc-cons-threshold` during startup.
- Block the Emacs main thread with synchronous network requests; use async processes.

## Troubleshooting

| Error                                                   | Cause                                                                   | Solution                                                                |
| :------------------------------------------------------ | :---------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `Failed to download package: HTTPS connection error`    | Outdated TLS/GnuTLS libraries on system or expired certificate.         | Set `(setq gnutls-algorithm-priority "NORMAL:-VERS-TLS1.3")` if needed. |
| `Spawning language server failed: executable not found` | Target LSP server (e.g. `pyright`, `rust-analyzer`) not in system PATH. | Install language server and verify `exec-path-from-shell` package.      |
| `Emacs startup taking > 5 seconds`                      | Synchronous package downloads and uncompiled Elisp during init.         | Profile startup with `emacs --profile` and use `use-package :defer t`.  |

## References

- [GNU Emacs Manual](https://www.gnu.org/software/emacs/manual/)
