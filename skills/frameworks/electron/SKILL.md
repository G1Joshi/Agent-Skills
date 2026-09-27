---
name: electron
description: Expert Electron assistance covering Main and Renderer processes, IPC communication, preload scripts, and packaging. Use when building cross-platform desktop applications with web technologies.
---

# Electron

Electron bundles **Chromium** and **Node.js** into a desktop app. It is the industry standard (VS Code, Slack, Discord) despite the file size.

## When to Use

- **Cross-Platform Desktop Applications**: Building native macOS, Windows, and Linux apps using web technologies (HTML, CSS, JS).
- **Desktop Software Requiring Deep OS Integration**: System tray menus, native notifications, file system access, and global hotkeys.
- **High-Performance Offline Desktop Tools**: IDEs (VS Code), communication tools (Slack), and media editors.
- **Enterprise Desktop Packaging**: Code-signing, auto-updating, and multi-architecture builds (x64, arm64).

## Quick Start

```javascript
// main.js
const { app, BrowserWindow } = require("electron");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.loadFile("index.html");
}

app.whenReady().then(createWindow);
```

## Core Concepts

#Secure Main and Renderer Architecture with Context Isolation

Enforcing security boundaries via preload scripts:

```javascript
// main.js (Main Process)
const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true, // Enforce security isolation
      nodeIntegration: false, // Disable raw Node in renderer
      sandbox: true,
    },
  });

  win.loadFile("index.html");
}

ipcMain.handle("read-app-version", async () => {
  return app.getVersion();
});

app.whenReady().then(createWindow);
```

#Preload Script & ContextBridge

Exposing safe, audited IPC channels to renderer window:

```javascript
// preload.js (Preload Script)
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  getAppVersion: () => ipcRenderer.invoke("read-app-version"),
  onFileSaved: (callback) => {
    ipcRenderer.on("file-saved", (_event, value) => callback(value));
  },
});
```

#Renderer Process Invocation

Calling native desktop capabilities from client frontend:

```typescript
// renderer.ts (Frontend / React / Vue / Vanilla)
declare global {
  interface Window {
    electronAPI: {
      getAppVersion: () => Promise<string>;
      onFileSaved: (callback: (path: string) => void) => void;
    };
  }
}

async function initUI() {
  const version = await window.electronAPI.getAppVersion();
  const versionDisplay = document.getElementById("app-version");
  if (versionDisplay) {
    versionDisplay.textContent = `v${version}`;
  }
}

initUI();
```

## Common Patterns

### Secure IPC Communication with Context Bridge

**Problem**: Enabling Renderer processes to communicate with OS APIs without creating remote code execution vulnerabilities.

**Solution**:
Expose strictly typed APIs via `contextBridge` in `preload.js`:

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  openFile: () => ipcRenderer.invoke("dialog:openFile"),
});

// main.js: ipcMain.handle("dialog:openFile", async () => { ... });
```

## Best Practices (2026)

- **Do** always set `contextIsolation: true` and `nodeIntegration: false` in `webPreferences`.
- **Do** enforce Content Security Policy (CSP) headers in all loaded HTML files to prevent XSS execution.
- **Do** use `ipcMain.handle()` and `ipcRenderer.invoke()` for asynchronous request-response IPC.
- **Do** validate and sanitize all IPC arguments received from renderer processes.
- **Don't** enable `webSecurity: false` or disable certificate validation.
- **Don't** expose entire Node.js modules (e.g. `fs`, `child_process`) through `contextBridge`.
- **Don't** block the Main process event loop with heavy computation; delegate work to utility processes.

## Troubleshooting

| Error                                        | Cause                                                                           | Solution                                                                   |
| :------------------------------------------- | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------- |
| `require is not defined in renderer process` | `nodeIntegration: false` and `contextIsolation: true` enabled (secure default). | Expose necessary Node functions through `preload.js` with `contextBridge`. |
| `Error: Cannot find module 'electron'`       | Electron installed globally instead of local devDependencies.                   | Run `npm install --save-dev electron` in project directory.                |
| `White screen on app launch in production`   | Asset paths relative to file system failing when packaged.                      | Use hash routing or ensure relative paths (`./`) in build output.          |

## References

- [Electron Documentation](https://www.electronjs.org/)
