---
name: cursor
description: Expert Cursor IDE assistance covering AI pair programming, codebase indexing, custom rules (.cursorrules), Composer, and debugging. Use when maximizing AI-native software development velocity.
---

# Cursor

Cursor is a fork of VS Code customized for AI. It pioneered **Tab-to-Complete** (Copilot++) and **Composer** (Multi-file edits). In 2025, it is the leading "AI Native" editor.

## When to Use

- **AI-First Software Development**: Accelerating feature engineering with Cursor IDE, Composer, and multi-file edits.
- **Repository-Level Contextual Reasoning**: Using `@codebase` to search across semantic embeddings of entire projects.
- **Custom Project Guidelines with .cursorrules**: Instructing the AI model on architecture, frameworks, and testing standards.
- **Interactive Inline Code Editing**: Generating, refactoring, and fixing code directly in the editor buffer via `Cmd+K`.

## Quick Start

Configure repository rules in `.cursorrules`:

```markdown
# .cursorrules

- Prefer functional components and hooks in React 19.
- Always use TypeScript with strict null checks.
- Keep helper functions small and pure.
- Include unit tests in Vitest for new features.
```

## Core Concepts

#Configuring .cursorrules for Automated Agent Guidelines

Defining persistent project rules for code generation:

```markdown
# .cursorrules

You are an expert Full-Stack TypeScript and Rust developer.
Always adhere strictly to these conventions:

- Framework: Next.js 15 (App Router), React 19, Tailwind CSS v4.
- Language: Strict TypeScript, no `any`, use `unknown` with type guards.
- Code Style: Functional, immutable, early returns, descriptive error messages.
- State: Favor Server Components and Server Actions over client state.
- Testing: Always write unit tests with Vitest and integration tests with Playwright.
- Do NOT hallucinate dependencies not present in package.json.
- When generating code, omit explanatory conversational filler; output code and brief rationale.
```

#Targeted Context Tagging with @ Directives

Injecting precise context into AI prompt buffers:

```text
Prompt:
@codebase How is authentication token verification handled across our microservice routes?
Inspect @middleware.ts and @src/auth/session.ts to implement a new rate-limited admin route guard.
Ensure compliance with @docs/security-guidelines.md.
```

#Multi-File Composer Refactoring Workflows

Prompting across architectural boundaries:

```text
Prompt in Composer:
Refactor our legacy User REST endpoints to modern Server Actions:
1. Create app/actions/user.ts with Zod input validation schemas.
2. Update app/profile/page.tsx to call the server action with useActionState.
3. Remove old API route handler in app/api/user/route.ts.
4. Add unit test in tests/actions/user.test.ts verifying rejection of invalid email.
```

## Common Patterns

#Global and Project .cursorrules Configuration
**Problem**: Cursor generates responses with generic boilerplate that violates repository architectural rules.  
**Solution**: Define comprehensive repository rules in root `.cursorrules`.

```markdown
# .cursorrules

- Prefer TypeScript strict mode with no explicit 'any'.
- Use named exports rather than default exports for React components.
- Colocate unit tests next to source files using the *.test.ts pattern.
- Wrap all external network calls with timeout boundaries.
```

## Best Practices (2026)

- **Do** create a `.cursorrules` file in the project root to permanently align model completions with team conventions.
- **Do** use `@file`, `@docs`, and `@symbol` instead of `@codebase` for targeted tasks to reduce prompt token noise and cost.
- **Do** review AI-generated diffs carefully before accepting multi-file Composer changes.
- **Do** configure `.cursorignore` to prevent indexing of generated files, `.env` secrets, and build output directories.
- **Don't** prompt the AI with raw database passwords, production API keys, or private customer data.
- **Don't** blindly accept massive multi-file refactors without running automated test suites (`npm test`).
- **Don't** write ambiguous prompts; specify desired libraries, error handling strategies, and boundary constraints.

## Troubleshooting

| Error                              | Cause                                                        | Solution                                              |
| :--------------------------------- | :----------------------------------------------------------- | :---------------------------------------------------- |
| `Codebase indexing failed`         | Massive files (`node_modules`, large binaries) not excluded. | Add paths to `.cursorignore`.                         |
| `Composer diff cannot be applied`  | File edited externally while Cursor was generating code.     | Re-run prompt using fresh file state.                 |
| `Cursor tab autocomplete sluggish` | Large language server indexing lag in background.            | Restart Cursor or disable unused language extensions. |

## References

- [Cursor Documentation](https://docs.cursor.com/)
