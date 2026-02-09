---
name: vue
description: Vue.js progressive framework with Composition API and Pinia. Use for .vue files.
---

# Vue.js

Progressive JavaScript framework with Composition API and reactivity.

## When to Use

- Single-page applications
- Progressive enhancement
- Component-based UIs
- Projects requiring flexibility

## Quick Start

```vue
<script setup lang="ts">
import { ref, computed } from "vue";

const count = ref(0);
const double = computed(() => count.value * 2);

function increment() {
  count.value++;
}
</script>

<template>
  <button @click="increment">Count: {{ count }} (Double: {{ double }})</button>
</template>
```

## Core Concepts

### Composition API

```vue
<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from "vue";

interface User {
  id: string;
  name: string;
}

const user = ref<User | null>(null);
const loading = ref(true);

const state = reactive({
  filters: { status: "active" },
  page: 1,
});

const displayName = computed(() => user.value?.name.toUpperCase() ?? "Guest");

watch(
  () => state.filters,
  async (newFilters) => {
    await fetchData(newFilters);
  },
  { deep: true },
);

onMounted(async () => {
  user.value = await fetchUser();
  loading.value = false;
});
</script>
```

### Composables

```typescript
// composables/useUser.ts
import { ref, onMounted } from "vue";

export function useUser(userId: string) {
  const user = ref<User | null>(null);
  const loading = ref(true);
  const error = ref<Error | null>(null);

  async function load() {
    loading.value = true;
    try {
      user.value = await fetchUser(userId);
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  onMounted(load);

  return { user, loading, error, reload: load };
}

// Usage
const { user, loading } = useUser(props.userId);
```

## Common Patterns

### Pinia Store

```typescript
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", () => {
  const user = ref<User | null>(null);
  const isLoggedIn = computed(() => !!user.value);

  async function login(email: string, password: string) {
    user.value = await authService.login(email, password);
  }

  function logout() {
    user.value = null;
  }

  return { user, isLoggedIn, login, logout };
});

// In component
const store = useUserStore();
store.login(email, password);
```

## Best Practices

**Do**:

- Use Composition API with `<script setup>`
- Use TypeScript for type safety
- Create composables for reusable logic
- Use Pinia for global state

**Don't**:

- Mix Options and Composition API
- Mutate props directly
- Use v-if and v-for on same element
- Overuse watchers

## Troubleshooting

| Issue                 | Cause                   | Solution         |
| --------------------- | ----------------------- | ---------------- |
| Reactivity lost       | Destructuring reactive  | Use toRefs()     |
| Watch not firing      | Shallow watch on object | Use deep: true   |
| Computed not updating | Non-reactive dependency | Use ref/reactive |

## References

- [Vue.js Documentation](https://vuejs.org/)
- [Vue School](https://vueschool.io/)
