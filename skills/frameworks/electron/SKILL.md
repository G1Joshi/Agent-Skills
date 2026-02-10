---
name: electron
description: Electron cross-platform desktop apps with web technologies. Use for desktop apps.
---

# Electron

Electron bundles **Chromium** and **Node.js** into a desktop app. It is the industry standard (VS Code, Slack, Discord) despite the file size.

## When to Use

- **Rich Capabilities**: If you need full Node.js access (Filesystem, Serial Port).
- **Consistent UI**: Loops exactly the same on Windows/Mac/Linux (Pixel Perfect).
- **Legacy**: Migrating an existing web app to desktop with zero changes.

## Core Concepts

### Main Process

The Node.js backend. Controls lifecycle and windows.

### Renderer Process

The Chromium frontend. Displays UI.

### Preload Scripts

The secure bridge between Main and Renderer (Context Isolation).

## Best Practices (2025)

**Do**:

- **Enable Context Isolation**: Critical security feature (`contextIsolation: true`).
- **Use IPC**: `ipcMain` and `ipcRenderer` for communication.
- **Update Chromium**: Security patches come via Electron updates.

**Don't**:

- **Don't use `remote` module**: It is deprecated and insecure.

## References

- [Electron Documentation](https://www.electronjs.org/)
