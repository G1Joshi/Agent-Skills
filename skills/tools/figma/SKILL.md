---
name: figma
description: Figma design tool for UI/UX, components, and design systems. Use for design collaboration.
---

# Figma

Collaborative design tool for UI/UX and design systems.

## When to Use

- UI/UX design
- Design system creation
- Prototyping
- Developer handoff

## Quick Start

```
Creating a component:
1. Design your element
2. Select layers
3. Ctrl/Cmd + Alt + K to create component
4. Use component panel to manage variants
```

## Core Concepts

### Auto Layout

```
Auto Layout Properties:
- Direction: Horizontal / Vertical
- Spacing: Gap between items
- Padding: Internal spacing
- Alignment: Start / Center / End
- Fill Container / Hug Contents

Best Practices:
- Use consistent spacing tokens
- Nest auto layouts for complex UI
- Use "Fill" for responsive elements
```

### Components & Variants

```
Component Structure:
├── Button (Component Set)
│   ├── Size=Large, State=Default
│   ├── Size=Large, State=Hover
│   ├── Size=Small, State=Default
│   └── Size=Small, State=Hover

Properties:
- Variant: Switch between variations
- Boolean: Show/hide elements
- Instance Swap: Replace nested components
- Text: Override text content
```

## Common Patterns

### Design Tokens

```css
/* Color Styles */
Primary/500: #3B82F6
Primary/600: #2563EB
Gray/100: #F3F4F6
Gray/900: #111827

/* Text Styles */
Heading/H1: Inter 48px Bold
Body/Regular: Inter 16px Regular

/* Effect Styles */
Shadow/SM: 0 1px 2px rgba(0,0,0,0.05)
Shadow/MD: 0 4px 6px rgba(0,0,0,0.1)
```

### Developer Handoff

```
Dev Mode Features:
- Inspect panel for CSS values
- Asset export (SVG, PNG, PDF)
- Component documentation
- Redline measurements

Annotations:
- Use sticky notes for dev notes
- Link to documentation
- Specify interaction details
```

## Best Practices

**Do**:

- Create a design system library
- Use auto layout everywhere
- Name layers meaningfully
- Document component usage

**Don't**:

- Use absolute positioning
- Create one-off styles
- Forget responsive design
- Skip component organization

## Troubleshooting

| Issue              | Cause                 | Solution                |
| ------------------ | --------------------- | ----------------------- |
| Slow performance   | Large file            | Split into pages/files  |
| Component issues   | Detached instance     | Reset to main component |
| Styles not syncing | Library not published | Publish library updates |

## References

- [Figma Help Center](https://help.figma.com/)
- [Figma Community](https://www.figma.com/community)
