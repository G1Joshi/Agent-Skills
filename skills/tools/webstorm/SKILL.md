---
name: webstorm
description: Expert WebStorm assistance covering JavaScript/TypeScript tooling, React/Vue/Angular integrations, Jest/Vitest debugging, and ESLint/Prettier setup. Use when configuring WebStorm projects, setting up debugger configurations, optimizing IDE performance, or refactoring TypeScript code.
---

# WebStorm

WebStorm is the JetBrains IDE for Web. While VS Code is free, WebStorm allows better refactoring for complex **TypeScript**, **Angular**, and **React** projects.

## When to Use

- **Professional JavaScript & TypeScript Development**: Advanced refactoring, symbol renaming, and deep static code analysis.
- **Full-Stack Framework Tooling**: First-class support for Next.js, React, Vue, Angular, Svelte, and Node.js.
- **Interactive Visual Debugging**: Breakpoint debugging across browser clients, server processes, and unit test suites.
- **Integrated Git, HTTP Client & Database Tooling**: Managing Git branches, testing REST endpoints, and querying databases inside one IDE.

## Quick Start

#1. Launch Project via Terminal

```bash
# Open frontend project in WebStorm
webstorm .
```

#2. Run Debug Session

```bash
# Start Vite / Next.js with Node inspect enabled
node --inspect-brk ./node_modules/vite/bin/vite.js
```

## Core Concepts

### TypeScript Service & Auto-Imports Configuration

Configuring WebStorm to use project TypeScript engine and strict import formatting in `.idea/codeStyles/Project.xml`:

```xml
<component name="ProjectCodeStyleConfiguration">
  <code_scheme name="Project" version="173">
    <JSCodeStyleSettings version="0">
      <option name="FORCE_SEMICOLON_STYLE" value="true" />
      <option name="USE_DOUBLE_QUOTES" value="false" />
      <option name="IMPORT_SORT_MEMBERS" value="true" />
    </JSCodeStyleSettings>
    <TypeScriptCodeStyleSettings version="0">
      <option name="FORCE_SEMICOLON_STYLE" value="true" />
      <option name="USE_DOUBLE_QUOTES" value="false" />
    </TypeScriptCodeStyleSettings>
  </code_scheme>
</component>
```

Settings verification:

- Open **Settings -> Languages & Frameworks -> TypeScript**.
- Set **TypeScript** to **Use TypeScript service** and select `node_modules/typescript`.

### Integrated HTTP Client for API Testing (`api.http`)

Writing and running executable HTTP requests directly inside WebStorm:

```http
### Authenticate User
# @name login
POST https://{{host}}/api/v1/auth/login
Content-Type: application/json

{
  "email": "developer@example.com",
  "password": "{{password}}"
}

> {%
  client.global.set("auth_token", response.body.token);
%}

### Fetch Protected Profile
GET https://{{host}}/api/v1/user/profile
Authorization: Bearer {{auth_token}}
Accept: application/json
```

### Full-Stack Debugging Configuration (`.idea/runConfigurations`)

Debugging Node.js server and Chrome frontend simultaneously:

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Debug Client & Server" type="CompoundRunConfigurationType">
    <toRun name="Next.js Server" type="NodeJS" />
    <toRun name="Client Browser" type="JavascriptDebugType" />
    <method v="2" />
  </configuration>
</component>
```

## Common Patterns

#Strict TypeScript Workspace Configuration
**Problem**: Ensure WebStorm uses project-specific TypeScript version rather than IDE fallback.  
**Solution**: Configure `tsconfig.json` path mapping recognized by WebStorm.

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    },
    "strict": true,
    "moduleResolution": "bundler"
  }
}
```

#Vitest / Jest Run Configuration
**Problem**: Standardize test runner execution with breakpoint debugging across team.  
**Solution**: Create committed run configuration file.

```xml
<!-- .run/Run Tests.run.xml -->
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Run Tests" type="JavaScriptTestRunnerVitest">
    <package-json value="$PROJECT_DIR$/package.json" />
    <vitest-package value="$PROJECT_DIR$/node_modules/vitest" />
    <working-dir value="$PROJECT_DIR$" />
    <method v="2" />
  </configuration>
</component>
```

## Best Practices (2026)

- **Do** configure ESLint and Prettier under **Languages & Frameworks -> JavaScript -> Code Quality Tools** with "Run on save".
- **Do** use WebStorm's **Extract Component / Method** (`Ctrl+Alt+M` / `Cmd+Option+M`) for safe structural refactoring.
- **Do** utilize `.http` files stored in the repository for shareable, executable API integration tests.
- **Do** exclude heavy build output directories (`.next`, `dist`, `coverage`) by right clicking -> **Mark Directory as -> Excluded**.
- **Don't** commit `.idea/workspace.xml` or user-specific shelf patches into Git.
- **Don't** run duplicate linters simultaneously; coordinate Prettier and ESLint configurations cleanly.
- **Don't** ignore yellow inspection warnings in JavaScript/TypeScript code; resolve them using `Alt + Enter`.

## Troubleshooting

| Error / Symptom                                   | Cause                                                              | Solution                                                                                                                   |
| ------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| WebStorm displays errors that `tsc` does not show | IDE using different TypeScript version than project `package.json` | Configure WebStorm to use project TypeScript under `Settings > Languages & Frameworks > TypeScript`.                       |
| IDE slow or indexing continuously                 | Large cache or build directories being indexed                     | Right-click `dist`, `.next`, `coverage` folders > **Mark Directory as > Excluded**.                                        |
| ESLint rules not reporting in editor              | ESLint configuration flat config mode disabled                     | Under **Settings > Languages & Frameworks > JavaScript > Code Quality Tools > ESLint**, ensure Automatic search is active. |

## References

- [WebStorm Documentation](https://www.jetbrains.com/webstorm/documentation/)
