---
name: chakraui
description: Chakra UI accessible React components. Use for React UI.
---

# Chakra UI

Chakra UI v3 (2025) moves to a **Zero-runtime** engine (Panda CSS under the hood) to solve performance issues, while keeping the developer experience of style props.

## When to Use

- **Speed**: Developing UI with style props (`<Box mt={4} />`) is incredibly fast.
- **Accessibility**: WAI-ARIA compliant out of the box.
- **Customizability**: Easier to customize than MUI.

## Core Concepts

### Style Props

Passing CSS as props. `bg="red.500"`.

### Polymorphism

`as` prop. `<Button as="a" href="...">`.

### Hooks

`useColorMode`, `useDisclosure` (for modals).

## Best Practices (2025)

**Do**:

- **Use v3**: Significant performance boost over v2 (Emotion-based).
- **Use `HStack` / `VStack`**: Great abstractions for Flexbox layout.
- **Extend Theme**: Define your colors/fonts in a theme file.

**Don't**:

- **Don't hardcode hex colors**: Use theme tokens (`blue.500`).

## References

- [Chakra UI Documentation](https://chakra-ui.com/)
