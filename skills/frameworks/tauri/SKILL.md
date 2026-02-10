---
name: tauri
description: Tauri lightweight desktop framework with Rust backend. Use for desktop apps.
---

# Tauri

Tauri allows building desktop (and now mobile in v2.0) apps using web technologies. It differs from Electron by using the **OS Native Webview** (WebView2 on Windows, WebKit on macOS/Linux).

## When to Use

- **Small Binaries**: Installers are ~3MB (vs 100MB+ for Electron).
- **Security**: Strict isolation and permission system.
- **Rust Backend**: If you need high-performance background logic.

## Core Concepts

### Frontend Agnostic

Use Svelte, React, Vue, or vanilla JS.

### Commands (IPC)

Interact with Rust backend: `invoke('my_command')`.

### Config (`tauri.conf.json`)

Defines permissions, windows, and bundling settings.

## Best Practices (2025)

**Do**:

- **Use v2.0 Mobile**: Target iOS/Android from the same codebase.
- **Use Commands**: Don't run heavy logic in JS. Offload to Rust.

**Don't**:

- **Don't assume Chrome**: You are running on Safari (macOS) or Edge (Windows). Test cross-platform.

## References

- [Tauri Documentation](https://tauri.app/)
