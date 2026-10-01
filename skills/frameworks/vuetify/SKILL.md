---
name: vuetify
description: Expert Vuetify assistance covering Material Design components, data tables, responsive layouts, and themes for Vue 3. Use when rapidly building enterprise dashboards and back-office tools in Vue.
---

# Vuetify

Vuetify is the comprehensive UI toolkit for Vue. v3 (Titan) is built for **Vue 3** and Vite, offering massive performance improvements over v2.

## When to Use

- **Material Design 3 Applications in Vue 3**: Enterprise business applications implementing Google Material Design.
- **Complex Enterprise Data Tables**: Server-side pagination, sorting, filtering, and row expansion with `v-data-table-server`.
- **Administrative Portals & Dashboards**: Pre-built form inputs, navigation drawers, app bars, and dialogs.
- **Accessible Multi-Theme Applications**: Switching seamlessly between light and dark themes with custom primary colors.

## Quick Start

```vue
<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card class="pa-4" elevation="2">
          <v-card-title>Vuetify Card</v-card-title>
          <v-card-text
            >Ready-to-use Material Design components for Vue 3.</v-card-text
          >
          <v-btn color="primary" @click="showAlert">Action</v-btn>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
function showAlert() {
  alert("Vuetify action triggered");
}
</script>
```

## Core Concepts

### Theme Configuration & Component Blueprint Setup

Setting up Vuetify 3 with Material Design 3 tokens:

```typescript
// plugins/vuetify.ts
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

export const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "light",
    themes: {
      light: {
        colors: {
          primary: "#1867C0",
          secondary: "#5CBBF6",
          surface: "#FFFFFF",
        },
      },
      dark: {
        colors: {
          primary: "#2196F3",
          secondary: "#424242",
          surface: "#121212",
        },
      },
    },
  },
});
```

### Server-Side Data Table with v-data-table-server

Displaying remote paginated data with sorting:

```vue
<script setup lang="ts">
import { ref } from "vue";

const itemsPerPage = ref(10);
const headers = [
  { title: "User ID", key: "id" },
  { title: "Full Name", key: "name" },
  { title: "Email Address", key: "email" },
  { title: "Role", key: "role" },
];

const serverItems = ref([]);
const totalItems = ref(0);
const loading = ref(false);

async function loadItems({ page, itemsPerPage, sortBy }: any) {
  loading.value = true;
  // Fetch from backend API
  const res = await fetch(`/api/users?page=${page}&limit=${itemsPerPage}`);
  const data = await res.json();
  serverItems.value = data.items;
  totalItems.value = data.total;
  loading.value = false;
}
</script>

<template>
  <v-card title="Registered Users" flat>
    <v-data-table-server
      v-model:items-per-page="itemsPerPage"
      :headers="headers"
      :items="serverItems"
      :items-length="totalItems"
      :loading="loading"
      item-value="id"
      @update:options="loadItems"
    />
  </v-card>
</template>
```

### Modern App Layout with v-app & Navigation Drawer

Building responsive responsive shell layout:

```vue
<script setup lang="ts">
import { ref } from "vue";

const drawer = ref(true);
</script>

<template>
  <v-app>
    <v-navigation-drawer v-model="drawer">
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Dashboard"
          value="dashboard"
        />
        <v-list-item
          prepend-icon="mdi-account-group"
          title="Customers"
          value="customers"
        />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar title="Enterprise Suite">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>
```

## Common Patterns

### Server-Side Paginated Data Table

**Problem**: Loading thousands of table rows at once overwhelms client browser memory.

**Solution**:
Use `v-data-table-server` with server pagination:

```vue
<template>
  <v-data-table-server
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="serverItems"
    :items-length="totalItems"
    :loading="loading"
    @update:options="loadItems"
  />
</template>

<script setup>
import { ref } from "vue";

const itemsPerPage = ref(10);
const headers = [
  { title: "Name", key: "name" },
  { title: "Email", key: "email" },
];
const serverItems = ref([]);
const totalItems = ref(0);
const loading = ref(false);

async function loadItems({ page, itemsPerPage, sortBy }) {
  loading.value = true;
  const res = await api.getUsers({ page, limit: itemsPerPage });
  serverItems.value = res.data;
  totalItems.value = res.total;
  loading.value = false;
}
</script>
```

## Best Practices

**Do**:

- Target Vuetify 3 with Vite plugin (`vite-plugin-vuetify`) for automatic treeshaking and minimal bundle size.
- Use `v-data-table-server` for datasets larger than 100 rows to avoid browser memory overhead.
- Use Vuetify validation rules functions (`:rules="[v => !!v || 'Required']"`) on `v-form`.
- Wrap applications in `<v-app>` and `<v-main>` to guarantee proper layout positioning.

**Don't**:

- Import all of `vuetify/components` in production builds; rely on automatic component treeshaking.
- Override component styles with high-specificity global CSS; use Vuetify props (`density`, `variant`, `color`).
- Forget to include `@mdi/font` or modern icon sets for Vuetify iconography.

## Troubleshooting

| Error                                         | Cause                                                | Solution                                                                |
| :-------------------------------------------- | :--------------------------------------------------- | :---------------------------------------------------------------------- |
| `Vuetify components not rendering / unstyled` | Component used outside `<v-app>` root wrapper.       | Ensure application template is enclosed in `<v-app>`.                   |
| `Missing styles for Vuetify components`       | Styles not imported in main entrypoint.              | Import `import 'vuetify/styles'` in your main application file.         |
| `Icon font not displaying (blank squares)`    | Icon set (mdi/fa) not configured in Vuetify options. | Install `@mdi/font` and import `@mdi/font/css/materialdesignicons.css`. |

## References

- [Vuetify Documentation](https://vuetifyjs.com/)
