---
name: materialui
description: Expert Material UI (MUI) assistance covering Emotion styled components, theme customization, DataGrid, and accessible icons. Use when building React enterprise dashboards with Google's Material Design.
---

# Material UI (MUI)

MUI Core (v6) is the gold standard for React UI. v6 introduces **Pigment CSS** (Zero-runtime CSS-in-JS) for compatibility with React Server Components (Next.js App Router).

## When to Use

- **Enterprise React Design Systems**: Implementing Google's Material Design guidelines with battle-tested React components.
- **Complex Administrative Portals**: Utilizing advanced Data Grid, Date Pickers, and Tree View components.
- **Custom Theming & Design Tokens**: Building accessible, branded design systems via `createTheme` and CSS variables.
- **Rapid Dashboard Prototyping**: Developing polished responsive dashboards with minimal custom CSS.

## Quick Start

```tsx
import * as React from "react";
import {
  Button,
  Container,
  Typography,
  Card,
  CardContent,
} from "@mui/material";

export default function MuiDemo() {
  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Card elevation={3}>
        <CardContent>
          <Typography variant="h5" component="div" gutterBottom>
            Material UI Card
          </Typography>
          <Typography color="text.secondary" paragraph>
            Pre-styled component adhering to Material Design 3.
          </Typography>
          <Button variant="contained" color="primary">
            Primary Action
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
}
```

## Core Concepts

### Theme Customization & CSS Theme Variables

Configuring design tokens and light/dark color schemes with MUI:

```tsx
import { createTheme, ThemeProvider, CssBaseline } from "@mui/material";

const theme = createTheme({
  cssVariables: true, // Enables native CSS variables
  colorSchemes: {
    light: {
      palette: {
        primary: { main: "#2563eb" },
        secondary: { main: "#475569" },
      },
    },
    dark: {
      palette: {
        primary: { main: "#60a5fa" },
        secondary: { main: "#94a3b8" },
      },
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", sans-serif',
  },
});

export function AppThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
```

### The SX Prop & Dynamic System Styling

Applying theme-aware styles directly to components:

```tsx
import { Box, Typography, Button, Stack } from "@mui/material";

export function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <Box
      sx={{
        p: 3,
        bgcolor: "background.paper",
        borderRadius: 2,
        boxShadow: 1,
        border: "1px solid",
        borderColor: "divider",
        transition: "transform 0.2s, box-shadow 0.2s",
        "&:hover": {
          transform: "translateY(-2px)",
          boxShadow: 3,
        },
      }}
    >
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="h4" fontWeight="bold" sx={{ mt: 1 }}>
        {value}
      </Typography>
    </Box>
  );
}
```

### Accessible Form Controls & Dialog Composition

Building composable modal workflows with focus trap:

```tsx
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
} from "@mui/material";
import { useState } from "react";

export function EditDialog({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const [name, setName] = useState("");

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Update Profile</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Full Name"
          type="text"
          fullWidth
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button variant="contained" onClick={onClose}>
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}
```

## Common Patterns

### Custom Theme Provider with Global Style Overrides

**Problem**: Overriding MUI typography and component defaults across an entire application without repetitive `sx` props.

**Solution**:
Use `createTheme` with component default props:

```typescript
import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    secondary: { main: "#dc004e" },
  },
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: { textTransform: "none", borderRadius: 8 },
      },
    },
  },
});

// Wrap app: <ThemeProvider theme={theme}><App /></ThemeProvider>
```

## Best Practices

**Do**:

- Enable `cssVariables: true` in `createTheme` to prevent SSR dark-mode flicker.
- Import icons using path imports (`import AddIcon from '@mui/icons-material/Add'`) to reduce bundle size.
- Use MUI Joy UI or MUI Base UI for unstyled / modern non-Material design requirements.
- Wrap inputs with `FormControl`, `InputLabel`, and `FormHelperText` for accessibility.

**Don't**:

- Use inline style objects (`style={{...}}`); use the theme-aware `sx` prop.
- Override MUI internal classnames (`.MuiButton-root`) directly; use theme overrides or `sx`.
- Nest multiple `ThemeProvider` instances without inheritance.

## Troubleshooting

| Error                                                                | Cause                                                            | Solution                                                                      |
| :------------------------------------------------------------------- | :--------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| `TypeError: Cannot read properties of undefined (reading 'spacing')` | Component rendered outside `<ThemeProvider>`.                    | Ensure root app is wrapped in `<ThemeProvider theme={theme}>`.                |
| `MUI: The value provided to Autocomplete is invalid`                 | Value object reference does not match any item in options array. | Implement `isOptionEqualToValue={(option, value) => option.id === value.id}`. |
| `CSS specificity clash with Tailwind / emotion`                      | Order of CSS injection causes rules to be overridden.            | Configure Emotion `StyledEngineProvider` with `injectFirst`.                  |

## References

- [Material UI Documentation](https://mui.com/)
