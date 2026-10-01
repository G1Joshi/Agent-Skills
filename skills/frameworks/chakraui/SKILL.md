---
name: chakraui
description: Expert Chakra UI assistance covering accessible React components, theme tokens, style props, and dark mode. Use when building modular, accessible React component libraries and dashboards.
---

# Chakra UI

Chakra UI is an accessible component library for React, utilizing style props and modular design tokens to rapidly compose responsive, themeable user interfaces.

## When to Use

- **Accessible React Component Systems**: Building accessible web apps adhering strictly to WAI-ARIA standards.
- **Component-Driven Styling with Style Props**: Styling UI components directly via JSX props with design tokens.
- **Dark Mode & Theming**: Implementing color mode switching and responsive themes with minimal setup.
- **Modern Next.js & Vite SPAs**: Creating accessible design systems with Chakra UI v3 / Ark UI foundations.

## Quick Start

```tsx
import { ChakraProvider, Box, Heading, Button, VStack } from "@chakra-ui/react";

export function App() {
  return (
    <ChakraProvider>
      <VStack spacing={4} p={8} align="stretch">
        <Box p={5} shadow="md" borderWidth="1px" borderRadius="lg">
          <Heading fontSize="xl">Welcome to Chakra UI</Heading>
          <Button colorScheme="teal" mt={4}>
            Get Started
          </Button>
        </Box>
      </VStack>
    </ChakraProvider>
  );
}
```

## Core Concepts

### Style Props & Responsive Layout Tokens

Building layouts using tokenized props:

```tsx
import { Box, Flex, Heading, Text, Button, Stack } from "@chakra-ui/react";

export function HeroBanner() {
  return (
    <Box
      bg={{ base: "gray.50", md: "gray.100", _dark: "gray.900" }}
      py={{ base: 8, md: 16 }}
      px={{ base: 4, md: 8 }}
      borderRadius="xl"
    >
      <Stack spacing={4} maxW="container.md" mx="auto" textAlign="center">
        <Heading size={{ base: "xl", md: "2xl" }} color="teal.500">
          Scalable Design System
        </Heading>
        <Text
          fontSize={{ base: "md", md: "lg" }}
          color="gray.600"
          _dark={{ color: "gray.300" }}
        >
          Build responsive, fully accessible web applications with Chakra UI
          style props.
        </Text>
        <Flex justify="center" gap={4} pt={2}>
          <Button colorPalette="teal" size="lg">
            Get Started
          </Button>
          <Button variant="outline" size="lg">
            Documentation
          </Button>
        </Flex>
      </Stack>
    </Box>
  );
}
```

### Custom Theme Extension & Semantic Tokens

Extending themes with brand colors and dark mode variants:

```typescript
import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

const customConfig = defineConfig({
  theme: {
    tokens: {
      colors: {
        brand: {
          50: { value: "#eef2ff" },
          500: { value: "#6366f1" },
          900: { value: "#312e81" },
        },
      },
    },
    semanticTokens: {
      colors: {
        primaryBg: {
          value: { base: "{colors.brand.50}", _dark: "{colors.brand.900}" },
        },
      },
    },
  },
});

export const system = createSystem(defaultConfig, customConfig);
```

### Accessible Form Controls & Modal Dialogs

Composing dialogs with focus traps and keyboard navigation:

```tsx
import { Dialog, Button, Input, Stack, Field } from "@chakra-ui/react";
import { useState } from "react";

export function EditProfileModal() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog.Root open={open} onOpenChange={(e) => setOpen(e.open)}>
      <Dialog.Trigger asChild>
        <Button variant="outline">Edit Profile</Button>
      </Dialog.Trigger>
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content>
          <Dialog.Header>
            <Dialog.Title>Update Profile Details</Dialog.Title>
          </Dialog.Header>
          <Dialog.Body>
            <Stack spacing={4}>
              <Field.Root>
                <Field.Label>Display Name</Field.Label>
                <Input placeholder="Enter full name" />
              </Field.Root>
            </Stack>
          </Dialog.Body>
          <Dialog.Footer>
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button colorPalette="blue" onClick={() => setOpen(false)}>
              Save
            </Button>
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog.Positioner>
    </Dialog.Root>
  );
}
```

## Common Patterns

### Custom Theme Extension with Color Palettes

**Problem**: Overriding design tokens globally without inline style prop repetition.

**Solution**:
Extend default theme using `extendTheme`:

```typescript
import { extendTheme } from "@chakra-ui/react";

export const theme = extendTheme({
  colors: {
    brand: {
      50: "#e4f8f0",
      500: "#10b981",
      900: "#064e3b",
    },
  },
  components: {
    Button: {
      defaultProps: {
        colorScheme: "brand",
      },
    },
  },
});
```

## Best Practices

**Do**:

- Target Chakra UI v3 / Snippets architecture for reduced bundle sizes and better server component compatibility.
- Use semantic tokens for colors and spacing to support dark mode without manual condition checks.
- Favor composition via `asChild` prop over polymorphic `as` props for type safety.
- Wrap the application root in `<ChakraProvider value={system}>`.

**Don't**:

- Hardcode raw hex values in style props; reference theme tokens (`blue.500`, `gray.100`).
- Create deep nested `Box` hierarchies when standard semantic elements (`Flex`, `Stack`, `Grid`) suffice.
- Disable focus rings (`outline="none"`) without providing an accessible alternative.

## Troubleshooting

| Error                                                    | Cause                                                  | Solution                                                                                |
| :------------------------------------------------------- | :----------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| `Cannot read properties of undefined (reading 'colors')` | Component rendered outside `<ChakraProvider>`.         | Wrap root application tree inside `<ChakraProvider>`.                                   |
| `Hydration failed because initial UI does not match`     | Dark mode color mode script missing from HTML head.    | Add `<ColorModeScript initialColorMode={theme.config.initialColorMode} />` to document. |
| `Invalid prop passed to DOM element`                     | Custom prop leaked through to underlying HTML element. | Use `shouldForwardProp` in custom styled components.                                    |

## References

- [Chakra UI Documentation](https://chakra-ui.com/)
