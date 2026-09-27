---
name: cursor-ai
description: Expert Cursor AI code editor assistance covering .cursorrules, Composer, Agent mode, inline edits, and semantic codebase indexing. Use when configuring AI pair programming workflows in Cursor.
---

# Cursor AI

Cursor is a fork of VS Code with AI baked into the core. **Cursor Composer** (2025) acts as an autonomous engineer that can write/edit multiple files simultaneously.

## When to Use

- **AI-Native Software Engineering**: Supercharging development with Cursor IDE, Composer, and multi-file code generation.
- **Context-Aware Codebase Exploration**: Indexing entire repositories to ask architectural questions using `@codebase`.
- **Automated Rule Enforcement**: Defining project conventions, tech stack guidelines, and testing rules with `.cursorrules`.
- **Terminal & In-Editor Debugging**: Resolving compiler errors, stack traces, and linter warnings with inline AI prompts.

## Quick Start

Create `.cursorrules` in your project root to provide persistent agent instructions:

```markdown
# .cursorrules

- Always use TypeScript with strict null checks.
- Prefer functional components with React 19 hooks.
- Write tests in Vitest for every new helper function.
- Do not add comments explaining obvious code.
```

## Core Concepts

#Configuring .cursorrules for Automated Agent Guidelines

Guiding AI behavior with standardized project rules:

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

#Repository Rules for AI (.cursorrules)
**Problem**: AI generates code with inconsistent formatting, outdated libraries, or non-idiomatic abstractions.  
**Solution**: Define deterministic coding instructions in root `.cursorrules`.

```markdown
# .cursorrules

You are an expert TypeScript engineer working on a Next.js 15 App Router codebase.

- Always use server components unless client interactivity (onClick, useState) is required.
- Validate all incoming request payloads with Zod schemas.
- Use Tailwind CSS utility classes; avoid inline styles or CSS modules.
- Handle errors with explicit Result types rather than throwing untyped exceptions.
- Never write placeholder comments (// TODO); provide complete implementations.
```

#Multi-File Composer Context (@Folders)
**Problem**: Refactoring cross-cutting concerns (e.g. updating an auth token interface across 5 files).  
**Solution**: Scope Cursor Composer with `@src/services/auth` and `@src/types` to synchronize type definitions, API callers, and test mocks in one unified multi-file diff.

## Best Practices (2026)

- **Do** create a `.cursorrules` file in the project root to permanently align model completions with team conventions.
- **Do** use `@file`, `@docs`, and `@symbol` instead of `@codebase` for targeted tasks to reduce prompt token noise and cost.
- **Do** review AI-generated diffs carefully before accepting multi-file Composer changes.
- **Do** configure `.cursorignore` to prevent indexing of generated files, `.env` secrets, and build output directories.
- **Don't** prompt the AI with raw database passwords, production API keys, or private customer data.
- **Don't** blindly accept massive multi-file refactors without running automated test suites (`npm test`).
- **Don't** write ambiguous prompts; specify desired libraries, error handling strategies, and boundary constraints.

## Troubleshooting

| Error                                | Cause                                                       | Solution                                                    |
| :----------------------------------- | :---------------------------------------------------------- | :---------------------------------------------------------- |
| `Codebase indexing stuck or failing` | Large binary files, `.git/`, or `node_modules` not ignored. | Add build directories and binaries to `.cursorignore`.      |
| `Cursorrules ignored in Composer`    | File placed in subfolder or named incorrectly.              | Name file exactly `.cursorrules` in project root directory. |
| `Inline edit diff rejects changes`   | File modified externally during generation.                 | Re-run prompt using `Cmd+K` / `Ctrl+K` on fresh file state. |

## References

- [Cursor Website](https://cursor.com/)
