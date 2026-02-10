---
name: cursor-ai
description: Cursor AI editor with context-aware coding. Use for AI-assisted development.
---

# Cursor AI

Cursor is a fork of VS Code with AI baked into the core. **Cursor Composer** (2025) acts as an autonomous engineer that can write/edit multiple files simultaneously.

## When to Use

- **Productivity**: It is currently the fastest way to write code.
- **Refactoring**: "Refactor this file to use hooks" works instantly.
- **Debugging**: It sees your terminal errors and fixes them automatically.

## Core Concepts

### Composer (`Cmd+I`)

A multi-file editing agent. You describe a feature ("Add a login page with auth middleware") and it creates/edits all necessary files.

### Tab Completion (Copilot++)

Predicts your next _edit_, not just your next word. It predicts cursor movement.

### Context (`@`)

Tagging files, folders, or docs (`@React Docs`) to give the AI context.

## Best Practices (2025)

**Do**:

- **Use Composer**: Don't just chat. Use Composer to apply edits directly.
- **Add Documentation**: Add external docs (`@Docs -> Add URL`) so Cursor knows your specific library versions.
- **Review Diffs**: Composer is powerful but can delete code. Always review the diffs.

**Don't**:

- **Don't ignore the ` .cursorrules`**: Define project-specific rules (e.g. "Always use TypeScript").

## References

- [Cursor Website](https://cursor.com/)
