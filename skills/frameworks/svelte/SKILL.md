---
name: svelte
description: Expert Svelte assistance covering Svelte 5 Runes, reactive declarations, stores, animations, and transitions. Use when building fast, reactive web UIs with minimal boilerplate.
---

# Svelte

Svelte is a component framework that compiles your code to tiny, framework-less vanilla JS. Svelte 5 (2025) introduces "Runes" for explicit reactivity.

## When to Use

- **High Performance defaults**: Svelte apps are tiny and fast by default.
- **Embedded Apps**: Great for widgets/embeds because of small bundle size.
- **Simplicity**: HTML, CSS, and JS in one file, with very little boilerplate.

## Quick Start

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

## Common Patterns

### Svelte 5 Runes for Fine-Grained Reactive State

**Problem**: Legacy Svelte 3/4 `let` bindings and `$: ` labels lack universal TypeScript ergonomics across `.svelte.ts` modules.

**Solution**:
Use modern Svelte 5 Runes (`$state`, `$derived`, `$effect`):

```svelte
<script lang="ts">
  let count = $state(0);
  let double = $derived(count * 2);

  $effect(() => {
    console.log(`Count changed to: ${count}`);
  });
</script>

<button on:click={() => count++}>
  Count: {count} (Double: {double})
</button>
```

## Best Practices (2026)

**Do**:

- **Use Runes**: Migrate from `let` + `$` syntax to `$state` and `$derived` for explicit reactivity.
- **Use `onclick`**: Svelte 5 prefers native attributes (`onclick`) over `on:click` directives.
- **Use Snippets**: Replace `slots` with Snippets for better type safety and flexibility.

**Don't**:

- **Don't rely on auto-reactivity (Legacy)**: In Svelte 5 settings, opting into Runes disables the "magic" assignment tracking of Svelte 3/4. This is good for predictability.

## Troubleshooting

| Error                                                       | Cause                                                             | Solution                                                                                 |
| :---------------------------------------------------------- | :---------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| `Array/Object mutation not triggering update in Svelte 3/4` | Mutating array in-place without reassignment (`arr.push(x)`).     | Reassign array: `arr = [...arr, x]` or upgrade to Svelte 5 `$state()`.                   |
| `Cannot bind to undefined property`                         | Missing `export let propName` in child component definition.      | Declare `export let propName;` (Svelte 3/4) or `let { propName } = $props()` (Svelte 5). |
| `Component is not defined in script`                        | Typo in import or relative path missing `.svelte` file extension. | Include explicit `.svelte` extension on component imports.                               |

## References

- [Svelte 5 Preview](https://svelte.dev/blog/runes)
- [Svelte Documentation](https://svelte.dev/)
