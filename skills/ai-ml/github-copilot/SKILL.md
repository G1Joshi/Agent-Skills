---
name: github-copilot
description: Expert GitHub Copilot assistance covering inline completions, Copilot Chat, workspace indexing, and custom instructions. Use when maximizing AI pair programming velocity and code quality.
---

# GitHub Copilot

GitHub Copilot is the enterprise standard. 2025 features **Copilot Workspace** (Idea-to-PR workflow) and **Copilot Edits** (multi-file awareness).

## When to Use

- **In-Editor AI Pair Programming**: Generating functions, documentation, and boilerplate across VS Code, JetBrains, and Neovim.
- **Repository-Level Architectural Context**: Using Copilot Chat with workspace awareness (`@workspace`).
- **Standardizing Team Prompting**: Authoring `.github/copilot-instructions.md` to enforce organizational coding standards.
- **Automated Pull Request Summarization**: Generating detailed PR summaries and test plans within GitHub Enterprise.

## Quick Start

Configure custom repository instructions in `.github/copilot-instructions.md`:

```markdown
# GitHub Copilot Instructions

- Use modern ES2022+ syntax and TypeScript 5.
- Always validate incoming API payloads using Zod schemas.
- Do not add comments describing self-explanatory lines.
- Write unit tests using Vitest with AAA (Arrange-Act-Assert) pattern.
```

## Core Concepts

#Project-Wide Custom Instructions (.github/copilot-instructions.md)

Configuring persistent AI developer guidelines:

```markdown
# .github/copilot-instructions.md

Repository Standards

- Language: TypeScript 5.5+ with strict mode enabled.
- Framework: Next.js 15 (App Router), Tailwind CSS v4.
- Database: Drizzle ORM with PostgreSQL.
- Testing: Vitest for unit tests, Playwright for e2e.

Coding Conventions

1. Always declare explicit return types on public functions.
2. Prefer async/await over raw Promises.
3. Use early returns and guard clauses to minimize nested blocks.
4. Never suggest 'any'; use typed generics or unknown.
5. All new business functions must include an accompanying unit test file.
```

#Slash Commands & Context Modifiers in Copilot Chat

Directing the AI assistant with precision:

```text
# Prompt in Copilot Chat
@workspace /explain How is user authentication state persisted across server and client components?

# Generating Unit Tests
/tests Generate comprehensive unit tests covering edge cases for validateOrderPayload()

# Fixing Errors
@terminal /fix Resolve this TypeScript compilation error with discriminated unions
```

#Inline Prompt Engineering for Precise Code Generation

Guiding inline suggestions with intentional comment prompts:

```typescript
// Function: parseJWTHeader
// Inputs: raw auth header string (e.g., 'Bearer <token>')
// Output: decoded payload object or throws UnauthorizedException
// Handles expired tokens, malformed base64, and missing prefix
export function parseJWTHeader(authHeader?: string): TokenPayload {
  // Copilot autocompletes implementation here
}
```

## Common Patterns

#Custom Copilot Instructions (.github/copilot-instructions.md)
**Problem**: Generic completions ignore repository style guides, testing patterns, and library versions.  
**Solution**: Create project-level guidelines recognized by Copilot in VS Code and JetBrains.

```markdown
<!-- .github/copilot-instructions.md -->

# Project Guidelines

- Architecture: Feature-sliced design (`src/features/<feature-name>/{api,components,hooks}`).
- State Management: TanStack Query for server state; Zustand for global client state.
- Testing: Write Vitest unit tests colocated as `<name>.test.ts` for all pure helper functions.
- Concurrency: Prefer `Promise.allSettled()` over `Promise.all()` for batch operations.
```

#Prompt-Driven Unit Test Generation (/tests)
**Problem**: Writing repetitive unit test boilerplate for edge cases and validation schemas.  
**Solution**: Highlight target function in editor and invoke `/tests` with constraints.

```typescript
// Prompt: /tests generate vitest test cases covering boundary values, empty arrays, and null inputs
export function calculateDiscount(price: number, coupon?: string): number {
  if (price < 0) throw new Error("Price cannot be negative");
  if (coupon === "VIP50") return price * 0.5;
  if (coupon === "SAVE10") return Math.max(0, price - 10);
  return price;
}
```

## Best Practices (2026)

- **Do** maintain a `.github/copilot-instructions.md` in repository root to align Copilot with team conventions.
- **Do** use `@workspace` to scope prompts to whole repository architecture and dependency patterns.
- **Do** provide clear docstrings, parameter types, and test names to guide high-quality completions.
- **Do** verify and write unit tests for all Copilot-generated logic before committing.
- **Don't** accept multi-line completions without verifying security implications (e.g. SQL injection, sanitization).
- **Don't** prompt Copilot with confidential tokens, production certificates, or customer PII.
- **Don't** rely on Copilot for sensitive cryptographic algorithm implementation without formal review.

## Troubleshooting

| Error                                       | Cause                                                                | Solution                                                                 |
| :------------------------------------------ | :------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `Copilot completions not appearing`         | Editor extension logged out or GitHub Copilot subscription inactive. | Re-authenticate GitHub account in IDE settings.                          |
| `Copilot generating obsolete API syntax`    | Context window lacks reference to modern framework version.          | Open modern reference file in adjacent tab or specify version in prompt. |
| `Copilot completions disabled for language` | File type disabled in Copilot extension language settings.           | Check `github.copilot.enable` settings in VS Code `settings.json`.       |

## References

- [GitHub Copilot](https://github.com/features/copilot)
