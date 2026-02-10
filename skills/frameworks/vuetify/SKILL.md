---
name: vuetify
description: Vuetify Material Design component framework for Vue. Use for Vue UI.
---

# Vuetify

Vuetify is the comprehensive UI toolkit for Vue. v3 (Titan) is built for **Vue 3** and Vite, offering massive performance improvements over v2.

## When to Use

- **Enterprise Dashboards**: The `VDataTable` is feature-rich.
- **Material Design**: Strict adherence to MD3 (Material Design 3).
- **Speed**: Rapid prototyping with pre-built components.

## Core Concepts

### Layout System

`v-app`, `v-main`, `v-container`. Essential for structure.

### Slots

Extensive use of slots for customization (`<template v-slot:append>`).

### Defaults

Global configuration of component default props.

## Best Practices (2025)

**Do**:

- **Use `Vite`**: Webpack is legacy.
- **Use Tree-shaking**: Import only what you use (automatic in v3).
- **Use SASS/SCSS Variables**: For theming.

**Don't**:

- **Don't mix with other UI libs**: Vuetify is invasive (global styles).

## References

- [Vuetify Documentation](https://vuetifyjs.com/)
