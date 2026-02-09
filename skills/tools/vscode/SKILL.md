---
name: vscode
description: VS Code editor configuration, extensions, debugging, and productivity tips. Use for editor customization.
---

# VS Code

Visual Studio Code editor customization and productivity.

## When to Use

- Configuring development environment
- Debugging applications
- Creating workspace settings
- Extension development

## Quick Start

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

## Core Concepts

### Workspace Configuration

```json
// .vscode/settings.json
{
  "editor.tabSize": 2,
  "editor.rulers": [80, 120],
  "files.exclude": {
    "**/node_modules": true,
    "**/.git": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

### Debug Configuration

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Server",
      "program": "${workspaceFolder}/src/server.ts",
      "preLaunchTask": "npm: build",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "env": {
        "NODE_ENV": "development"
      }
    },
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Frontend",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}"
    }
  ]
}
```

## Common Patterns

### Tasks

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "npm: dev",
      "type": "npm",
      "script": "dev",
      "isBackground": true,
      "problemMatcher": ["$tsc-watch"]
    },
    {
      "label": "Build & Test",
      "dependsOn": ["npm: build", "npm: test"],
      "dependsOrder": "sequence"
    }
  ]
}
```

### Extensions Recommendations

```json
// .vscode/extensions.json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

## Best Practices

**Do**:

- Use workspace settings per project
- Configure format on save
- Create debug configurations
- Share extension recommendations

**Don't**:

- Commit user-specific settings
- Install too many extensions
- Ignore keybinding conflicts
- Skip workspace trust settings

## Troubleshooting

| Issue                 | Cause               | Solution              |
| --------------------- | ------------------- | --------------------- |
| Extension not working | Conflict            | Check Output panel    |
| Slow startup          | Too many extensions | Disable unused        |
| Formatting wrong      | Multiple formatters | Set default formatter |

## References

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [VS Code Tips](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)
