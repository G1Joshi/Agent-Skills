---
name: svelte
description: Svelte compile-time framework with reactive declarations. Use for .svelte files.
---

# Svelte

Svelte is a component framework that compiles your code to tiny, framework-less vanilla JS. Svelte 5 (2025) introduces "Runes" for explicit reactivity.

## When to Use

- **High Performance defaults**: Svelte apps are tiny and fast by default.
- **Embedded Apps**: Great for widgets/embeds because of small bundle size.
- **Simplicity**: HTML, CSS, and JS in one file, with very little boilerplate.

## Quick Start (Runes)

```svelte
<script>
  let count = $state(0);
  let double = $derived(count * 2);

  function increment() {
    count += 1;
  }
</script>

<button onclick={increment}>
  Count: {count} / Double: {double}
</button>
```

## Core Concepts

### Runes

Svelte 5 reactivity markers.

- **`$state`**: Declares reactive state.
- **`$derived`**: Declares a value that updates when dependencies change.
- **`$effect`**: Runs code when dependencies change (side effects).
- **`$props`**: Declares component props.

### Snippets

Reusable chunks of markup within a component.

```svelte
{#snippet figure(src, caption)}
  <figure>
    <img {src} alt={caption} />
    <figcaption>{caption}</figcaption>
  </figure>
{/snippet}

{@render figure(imageSrc, "A nice image")}
```

## Best Practices (2025)

**Do**:

- **Use Runes**: Migrate from `let` + `$` syntax to `$state` and `$derived` for explicit reactivity.
- **Use `onclick`**: Svelte 5 prefers native attributes (`onclick`) over `on:click` directives.
- **Use Snippets**: Replace `slots` with Snippets for better type safety and flexibility.

**Don't**:

- **Don't rely on auto-reactivity (Legacy)**: In Svelte 5 settings, opting into Runes disables the "magic" assignment tracking of Svelte 3/4. This is good for predictability.

## References

- [Svelte 5 Preview](https://svelte.dev/blog/runes)
- [Svelte Documentation](https://svelte.dev/)
