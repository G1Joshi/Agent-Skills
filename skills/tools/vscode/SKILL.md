---
name: vscode
description: Expert Visual Studio Code assistance covering settings.json, launch.json debugging, tasks.json automation, dev containers, and workspace extensions. Use when configuring VS Code environments, setting up multi-language debuggers, automating tasks, or configuring devcontainer environments.
---

# Visual Studio Code

Visual Studio Code is a versatile, lightweight code editor offering rich language ecosystems, built-in debugging, source control integration, and Dev Container support.

## When to Use

- **Polyglot Development Workspace**: Full-featured IDE for TypeScript, Python, Go, Rust, C#, and Cloud Native development.
- **Standardized Team Workspace Configuration**: Enforcing shared settings, linter rules, and extensions across engineering teams.
- **Container & Remote Development**: Developing inside Docker containers, WSL2, or remote servers via Remote - SSH / Dev Containers.
- **Interactive Multi-Target Debugging**: Setting conditional breakpoints, inspecting variables, and debugging full-stack architectures.

## Quick Start

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "files.autoSave": "onFocusChange"
}
```

## Core Concepts

### Enterprise Workspace Settings (`.vscode/settings.json`)

Standardizing format-on-save, linter integrations, and search exclusions:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.fontFamily": "'JetBrains Mono', 'Fira Code', monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/.git": true,
    "**/.svn": true,
    "**/.DS_Store": true,
    "**/node_modules": true
  },
  "search.exclude": {
    "**/dist": true,
    "**/build": true,
    "**/.next": true
  }
}
```

### Full-Stack Debugging Configuration (`.vscode/launch.json`)

Debugging Next.js server and client simultaneously:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: Node Server",
      "type": "node",
      "request": "launch",
      "command": "npm run dev",
      "serverReadyAction": {
        "pattern": "- Local:.+(https?://.+)",
        "uriFormat": "%s",
        "action": "debugWithEdge"
      }
    },
    {
      "name": "Next.js: Chrome Client",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}"
    }
  ],
  "compounds": [
    {
      "name": "Full-Stack Next.js",
      "configurations": ["Next.js: Node Server", "Next.js: Chrome Client"]
    }
  ]
}
```

### Recommended Team Extensions (`.vscode/extensions.json`)

Prompting developers to install essential project plugins:

```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-azuretools.vscode-docker",
    "github.copilot",
    "eamodio.gitlens"
  ]
}
```

## Common Patterns

### Dev Container Configuration

**Problem**: Standardize development environment across entire team inside Docker.  
**Solution**: Define `.devcontainer/devcontainer.json`.

```json
{
  "name": "Node & TypeScript Container",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "customizations": {
    "vscode": {
      "extensions": ["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  },
  "forwardPorts": [3000]
}
```

### Workspace Tasks Automation (.vscode/tasks.json)

**Problem**: Run build or test scripts via standard `Ctrl + Shift + B` build shortcut.  
**Solution**: Configure tasks.json.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "npm",
      "script": "build",
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": ["$tsc"]
    }
  ]
}
```

## Best Practices

**Do**:

- Commit `.vscode/settings.json`, `.vscode/launch.json`, and `.vscode/extensions.json` to version control for team alignment.
- Configure **Dev Containers** (`.devcontainer/devcontainer.json`) for instant, reproducible containerized onboarding.
- Use `editor.formatOnSave: true` with a defined `editor.defaultFormatter` to maintain clean git diffs.
- Define task workflows in `.vscode/tasks.json` to run tests and linters via unified keybindings (`Cmd+Shift+B`).

**Don't**:

- Install hundreds of unnecessary extensions; disable extensions globally and enable them per workspace.
- Commit `.vscode/settings.json` with machine-specific hardcoded local file paths.
- Ignore VS Code security prompts when opening untrusted repositories in Workspace Trust mode.

## Troubleshooting

| Error                                   | Cause                                                               | Solution                                                                         |
| --------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Format on save not executing            | Multiple formatters installed without default specified             | Set `"editor.defaultFormatter"` explicitly in `settings.json`.                   |
| Remote - SSH disconnects frequently     | Keepalive packets timing out over unstable connection               | Add `"ServerAliveInterval 60"` to `~/.ssh/config` for target host.               |
| High CPU usage by `Code Helper` or `rg` | Searching or watching ignored folders like `node_modules` or `.git` | Add paths to `"files.watcherExclude"` and `"search.exclude"` in `settings.json`. |

## References

- [VS Code Documentation](https://code.visualstudio.com/docs)
