---
name: tauri
description: Expert Tauri assistance covering Rust core backend, web frontend, secure IPC commands, and multi-platform packaging. Use when building lightweight, secure, native desktop/mobile apps.
---

# Tauri

Tauri allows building desktop (and now mobile in v2.0) apps using web technologies. It differs from Electron by using the **OS Native Webview** (WebView2 on Windows, WebKit on macOS/Linux).

## When to Use

- **Lightweight Cross-Platform Desktop Apps**: Building native macOS, Windows, and Linux apps using web frontends and Rust backends.
- **Tauri v2 Mobile & Desktop Support**: Compiling unified codebases to iOS, Android, and desktop.
- **Memory-Efficient Desktop Software**: Tiny binary size (< 10MB) and low memory usage utilizing the system webview.
- **High-Security Desktop Environments**: Strict IPC permissions, cryptographic signature verification, and zero Node runtime.

## Quick Start

```rust
// src-tauri/src/main.rs
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```javascript
// frontend app.js
import { invoke } from "@tauri-apps/api/core";
const greeting = await invoke("greet", { name: "World" });
```

## Core Concepts

#Rust Command Handlers with #[tauri::command]

Exposing high-performance native Rust functions to the webview:

```rust
// src-tauri/src/lib.rs
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct SystemStats {
    cpu_cores: usize,
    os_name: String,
}

#[tauri::command]
fn get_system_stats() -> Result<SystemStats, String> {
    Ok(SystemStats {
        cpu_cores: num_cpus::get(),
        os_name: std::env::consts::OS.to_string(),
    })
}

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_system_stats])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

#Invoking Rust Commands from Frontend

Type-safe frontend IPC invocation:

```typescript
// src/services/system.ts
import { invoke } from "@tauri-apps/api/core";

interface SystemStats {
  cpu_cores: number;
  os_name: string;
}

export async function fetchSystemMetrics(): Promise<SystemStats> {
  try {
    const stats = await invoke<SystemStats>("get_system_stats");
    console.log(`Running on ${stats.os_name} with ${stats.cpu_cores} cores`);
    return stats;
  } catch (error) {
    console.error("Failed to invoke Tauri command:", error);
    throw error;
  }
}
```

#Tauri v2 Permissions & Capabilities System

Configuring granular security rules for plugins and commands:

```json
// src-tauri/capabilities/main.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    "dialog:allow-open",
    "notification:allow-notify"
  ]
}
```

## Common Patterns

### Typed IPC Invocation with Serde Structs

**Problem**: Passing structured parameters and receiving typed errors across the Rust-to-JS bridge.

**Solution**:
Serialize payloads with serde:

```rust
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct LoginRequest {
    username: String,
    auth_token: String,
}

#[derive(Serialize)]
struct UserSession {
    user_id: u64,
    display_name: String,
}

#[tauri::command]
async fn authenticate(req: LoginRequest) -> Result<UserSession, String> {
    if req.auth_token == "valid" {
        Ok(UserSession { user_id: 1, display_name: req.username })
    } else {
        Err("Authentication failed".into())
    }
}
```

## Best Practices (2026)

- **Do** target Tauri v2 with explicit capability and permission manifests for least privilege access.
- **Do** handle heavy computation and filesystem operations in Rust, keeping the webview UI smooth and responsive.
- **Do** configure code signing and automated updates using Tauri's built-in updater plugin.
- **Do** use `@tauri-apps/api/core` for modern Tauri v2 frontend bindings.
- **Don't** pass large binary files across the IPC bridge as base64 strings; use custom protocol streaming.
- **Don't** grant wildcard permissions (`fs:allow-all`) in capability files.
- **Don't** block the main Tauri thread; use async Rust commands for I/O operations.

## Troubleshooting

| Error                                              | Cause                                                          | Solution                                                               |
| :------------------------------------------------- | :------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `Command ... not found in invoke handler`          | Command function omitted from `tauri::generate_handler![...]`. | Register the command name in `generate_handler![my_cmd]`.              |
| `Tauri build fails: WebView2 / WebKit2GTK missing` | Missing system webview libraries on Linux or Windows.          | Install `libwebkit2gtk-4.1-dev` (Linux) or WebView2 runtime (Windows). |
| `Permission denied calling plugin API in Tauri v2` | Capabilities permission file not granting access to plugin.    | Add plugin permissions in `src-tauri/capabilities/default.json`.       |

## References

- [Tauri Documentation](https://tauri.app/)
