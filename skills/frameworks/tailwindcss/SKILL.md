---
name: tailwindcss
description: Tailwind CSS utility-first framework for custom designs. Use for rapid UI development.
---

# Tailwind CSS

Utility-first CSS framework for rapid custom UI development.

## When to Use

- Custom design systems
- Rapid UI prototyping
- Component-based styling
- Responsive layouts

## Quick Start

```html
<button
  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
>
  Click me
</button>

<div
  class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl"
>
  <div class="md:flex">
    <div class="p-8">
      <h2 class="text-xl font-semibold text-gray-800">Card Title</h2>
      <p class="mt-2 text-gray-600">Card content goes here.</p>
    </div>
  </div>
</div>
```

## Core Concepts

### Responsive Design

```html
<!-- Mobile-first responsive -->
<div class="w-full md:w-1/2 lg:w-1/3 xl:w-1/4">Responsive width</div>

<!-- Responsive typography -->
<h1 class="text-2xl md:text-4xl lg:text-6xl font-bold">Responsive Title</h1>

<!-- Responsive flex -->
<div class="flex flex-col md:flex-row gap-4">
  <div class="flex-1">Item 1</div>
  <div class="flex-1">Item 2</div>
</div>
```

### Custom Configuration

```javascript
// tailwind.config.js
export default {
  content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef2ff",
          500: "#6366f1",
          600: "#4f46e5",
        },
      },
      spacing: {
        128: "32rem",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
```

## Common Patterns

### Component Classes

```css
/* Using @apply for component styles */
@layer components {
  .btn {
    @apply px-4 py-2 rounded font-semibold transition-colors;
  }

  .btn-primary {
    @apply btn bg-blue-500 text-white hover:bg-blue-600;
  }

  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md 
           focus:outline-none focus:ring-2 focus:ring-blue-500;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}
```

### Dark Mode

```html
<!-- Enable dark mode in config: darkMode: 'class' -->
<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  <h1 class="text-2xl font-bold">Dark Mode Support</h1>
  <p class="text-gray-600 dark:text-gray-300">Adaptive content</p>
</div>
```

## Best Practices

**Do**:

- Use consistent spacing scale
- Extract components with @apply
- Configure custom design tokens
- Use arbitrary values sparingly `[...]`

**Don't**:

- Create overly long class strings
- Override utility classes with CSS
- Skip the content configuration
- Ignore purge in production

## Troubleshooting

| Issue               | Cause                | Solution               |
| ------------------- | -------------------- | ---------------------- |
| Styles not applying | Missing content path | Update content array   |
| Large CSS bundle    | No purging           | Check content config   |
| Specificity issues  | Conflicting styles   | Use important modifier |

## References

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind UI](https://tailwindui.com/)
