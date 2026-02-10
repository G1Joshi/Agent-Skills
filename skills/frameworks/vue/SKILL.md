---
name: vue
description: Vue.js progressive framework with Composition API and Pinia. Use for .vue files.
---

# Vue.js

Vue is a progressive framework for building user interfaces. Vue 3.5 (2025) solidifies the Composition API and introduces "Vapor Mode" for solid-js like performance.

## When to Use

- **Progressive Adoption**: Drop it into an existing HTML page or build a full SPA.
- **Developer Experience**: Often cited as having the best balance of simplicity and power.
- **Performance**: With Vapor Mode, it rivals the fastest signals-based frameworks.

## Quick Start (Composition API)

```vue
<script setup>
import { ref, computed } from "vue";

const count = ref(0);
const double = computed(() => count.value * 2);

function increment() {
  count.value++;
}
</script>

<template>
  <button @click="increment">
    Count is: {{ count }}, Double is: {{ double }}
  </button>
</template>
```

## Core Concepts

### Composition API (`<script setup>`)

The standard way to write Vue components. It groups logic by feature, not by option type (data, methods, mounted).

### Reactivity System (Signals)

Vue's reactivity is based on proxies. `ref()` and `reactive()` allow fine-grained dependency tracking.

### Vapor Mode (Opt-in)

A compilation strategy that compiles Vue components into highly efficient JavaScript that modifies the DOM directly (no Virtual DOM).

## Best Practices (2025)

**Do**:

- **Use `<script setup>`**: It is less verbose and provides better TypeScript support.
- **Use `defineModel`**: The new standard for two-way binding props (Vue 3.4+).
- **Use Composables**: Extract logic into reusable `useFeature()` functions (Vue's version of Hooks).

**Don't**:

- **Don't mix Options and Composition API**: Stick to Composition API for new projects.
- **Don't destructure `props`**: You lose reactivity (unless using `toRefs` or Vue 3.5 reactive destructuring).

## References

- [Vue.js Documentation](https://vuejs.org/)
- [Vue Vapor Mode](https://github.com/vuejs/core-vapor)
