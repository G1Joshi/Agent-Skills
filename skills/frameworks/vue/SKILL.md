---
name: vue
description: Expert Vue 3 assistance covering Composition API (<script setup>), reactivity (ref, reactive), Pinia, and Vue Router. Use when developing modern, progressive web interfaces and single-page applications.
---

# Vue.js

Vue is a progressive framework for building user interfaces. Vue 3.5 (2025) solidifies the Composition API and introduces "Vapor Mode" for solid-js like performance.

## When to Use

- **Progressive Full-Stack Web Applications**: Vue 3.5+ with `<script setup>` and Composition API.
- **Single Page Applications (SPAs)**: Building fast, reactive frontends with Vue Router and Pinia.
- **Interactive Micro-Frontends & Widgets**: Embedding reactive components into existing server-rendered templates.
- **Design System Implementation**: Building accessible, scoped component libraries with PrimeVue or Vuetify.

## Quick Start

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

#Composition API with <script setup> & TypeScript

Reactive primitives using `ref`, `computed`, and `watch`:

```vue
<!-- components/ProductCounter.vue -->
<script setup lang="ts">
import { ref, computed, watch } from "vue";

interface Props {
  initialCount?: number;
  unitPrice: number;
}

const props = withDefaults(defineProps<Props>(), {
  initialCount: 1,
});

const emit = defineEmits<{
  (e: "totalChanged", total: number): void;
}>();

const quantity = ref(props.initialCount);
const totalPrice = computed(() => quantity.value * props.unitPrice);

watch(totalPrice, (newTotal) => {
  emit("totalChanged", newTotal);
});

function increment() {
  quantity.value += 1;
}

function decrement() {
  if (quantity.value > 1) quantity.value -= 1;
}
</script>

<template>
  <div class="counter-box">
    <button @click="decrement">-</button>
    <span>{{ quantity }}</span>
    <button @click="increment">+</button>
    <p>Total: ${{ totalPrice.toFixed(2) }}</p>
  </div>
</template>
```

#State Management with Pinia

Centralized reactive store with type inference:

```typescript
// stores/cart.ts
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export interface CartItem {
  id: number;
  name: string;
  price: number;
}

export const useCartStore = defineStore("cart", () => {
  const items = ref<CartItem[]>([]);

  const totalCost = computed(() =>
    items.value.reduce((sum, item) => sum + item.price, 0),
  );
  const itemCount = computed(() => items.value.length);

  function addItem(item: CartItem) {
    items.value.push(item);
  }

  function clearCart() {
    items.value = [];
  }

  return { items, totalCost, itemCount, addItem, clearCart };
});
```

#Asynchronous Components & Suspense

Lazy-loading components for optimal code splitting:

```vue
<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const HeavyChart = defineAsyncComponent(
  () => import("./HeavyAnalyticsChart.vue"),
);
</script>

<template>
  <Suspense>
    <template #default>
      <HeavyChart />
    </template>
    <template #fallback>
      <div class="loading-skeleton">Loading interactive chart...</div>
    </template>
  </Suspense>
</template>
```

## Common Patterns

### Composable Pattern with Auto-Cleanup

**Problem**: Encapsulating reactive stateful logic for reuse across multiple components.

**Solution**:
Build typed composables with Vue 3 lifecycle hooks:

```typescript
import { ref, onMounted, onUnmounted } from "vue";

export function useMouse() {
  const x = ref(0);
  const y = ref(0);

  function update(event: MouseEvent) {
    x.value = event.pageX;
    y.value = event.pageY;
  }

  onMounted(() => window.addEventListener("mousemove", update));
  onUnmounted(() => window.removeEventListener("mousemove", update));

  return { x, y };
}
```

## Best Practices (2026)

- **Do** use `<script setup lang="ts">` as the default syntax for all Vue 3 components.
- **Do** use Pinia for global state management; deprecate legacy Vuex.
- **Do** use `shallowRef` or `shallowReactive` for large arrays/objects that do not need deep reactivity.
- **Do** scope component CSS (`<style scoped>`) to avoid leaking styles across the application.
- **Don't** use Options API (`data()`, `methods`) in new greenfield TypeScript codebases.
- **Don't** mutate props directly inside child components; emit events for the parent to update state.
- **Don't** use `v-if` and `v-for` on the exact same HTML element.

## Troubleshooting

| Error                                                | Cause                                                     | Solution                                                                  |
| :--------------------------------------------------- | :-------------------------------------------------------- | :------------------------------------------------------------------------ |
| `TypeError: Cannot set property of undefined in ref` | Forgetting `.value` when updating `ref` in JavaScript.    | Always read and write refs using `.value` in `<script>`: `count.value++`. |
| `Reactivity lost when destructuring reactive object` | Destructuring `reactive({})` strips the underlying Proxy. | Wrap object with `toRefs(state)` before destructuring.                    |
| `Component emitted event but no listener registered` | Event name casing mismatch between component and parent.  | Use kebab-case for event listeners in templates: `@update-item="handle"`. |

## References

- [Vue.js Documentation](https://vuejs.org/)
- [Vue Vapor Mode](https://github.com/vuejs/core-vapor)
