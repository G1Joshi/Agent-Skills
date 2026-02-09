---
name: github-copilot
description: GitHub Copilot AI pair programming with suggestions and chat. Use for AI-assisted coding.
---

# GitHub Copilot

AI pair programmer for code suggestions and chat assistance.

## When to Use

- Writing new code
- Understanding existing code
- Generating tests
- Refactoring and debugging

## Quick Start

```
# VS Code Commands
Ctrl/Cmd + I           - Open Copilot Chat
Tab                    - Accept suggestion
Esc                    - Dismiss suggestion
Alt + ]                - Next suggestion
Alt + [                - Previous suggestion
```

## Core Concepts

### Inline Suggestions

```typescript
// Write a comment describing what you want
// Function to validate email address
function validateEmail(email: string): boolean {
  // Copilot suggests:
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Type function signature, Copilot completes
async function fetchUserById(id: string): Promise<User> {
  // Copilot suggests implementation
}
```

### Chat Commands

```
# In Copilot Chat

/explain - Explain selected code
/fix - Suggest fixes for problems
/tests - Generate unit tests
/doc - Add documentation
/new - Create new code
```

## Common Patterns

### Effective Prompting

```typescript
// BE SPECIFIC
// ❌ Bad: Create a function
// ✅ Good: Create an async function that fetches user data from /api/users/:id
//          and returns a User object or null if not found

// PROVIDE CONTEXT
// Helper function for the UserService class
// Uses the existing httpClient and handles 404 gracefully
async function fetchUser(id: string): Promise<User | null> {
  // Copilot has better context now
}

// USE EXAMPLES
// Format: parseDate("2024-01-15") => Date
// Format: parseDate("invalid") => null
function parseDate(input: string): Date | null {
  // Copilot understands the pattern
}
```

### Chat Interactions

```
# Explain code
@workspace explain the authentication flow

# Generate tests
@workspace /tests for UserService

# Fix issues
/fix this function throws an error when input is null

# Create documentation
/doc add JSDoc comments to this class
```

## Best Practices

**Do**:

- Write clear comments describing intent
- Review all suggestions carefully
- Use chat for complex explanations
- Provide context in file headers

**Don't**:

- Accept without reviewing
- Trust for security-critical code
- Skip testing generated code
- Rely on it for architecture decisions

## Troubleshooting

| Issue          | Cause             | Solution             |
| -------------- | ----------------- | -------------------- |
| No suggestions | Extension issue   | Restart VS Code      |
| Wrong language | File not detected | Check file extension |
| Slow response  | Network/load      | Check connection     |

## References

- [GitHub Copilot Docs](https://docs.github.com/copilot)
- [VS Code Copilot](https://code.visualstudio.com/docs/copilot/)
