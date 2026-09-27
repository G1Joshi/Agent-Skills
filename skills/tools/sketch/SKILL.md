---
name: sketch
description: Expert Sketch assistance covering vector UI/UX design, symbol libraries, design tokens, color variables, and developer handoff workflows. Use when creating design systems in Sketch, managing shared libraries, exporting asset slices, or integrating Sketch with prototyping tools.
---

# Sketch

Sketch is the native Mac design tool. While Figma dominates the web, Sketch remains beloved for its native performance and privacy. 2025 updates focus on **Command Bar** and **Stacks**.

## When to Use

- **macOS Native UI/UX Vector Design**: Crafting vector interfaces, design system component libraries, and interactive wireframes.
- **Design Token Automation**: Exporting colors, typography, and spacing tokens to code using Sketch plugins and JavaScript APIs.
- **Symbol & Shared Style Libraries**: Managing synchronized component libraries across distributed design and frontend teams.
- **Handoff Specification Generation**: Exporting pixel-perfect SVG assets, PDF specs, and developer inspect documentation.

## Quick Start

### 1. Export Assets via Sketchtool CLI

```bash
# Export all artboards to @2x PNG
sketchtool export artboards "MyDesign.sketch" --scales="1, 2" --output="assets/exports"

# Export specific slices
sketchtool export slices "MyDesign.sketch" --formats="svg,png"
```

### 2. Design Token Organization

- Define Global Color Variables in **Document Settings > Color Variables**.
- Name systematically: `color/primary/500`, `color/neutral/100`.
- Create Components as **Symbols** with standardized naming: `Button/Primary/Large/Default`.

## Core Concepts

### Sketch JavaScript API: Automated Token Exporter

Writing an automated Sketch script to export document color variables to JSON tokens:

```javascript
// export-tokens.js (Run via Sketch Developer Console)
const sketch = require("sketch");
const document = sketch.getSelectedDocument();

const colors = document.colors.map((colorAsset) => ({
  name: colorAsset.name || "Untitled",
  hex: colorAsset.color,
}));

const designTokens = {
  version: "1.0.0",
  palette: colors.reduce((acc, curr) => {
    const slug = curr.name.toLowerCase().replace(/\s+/g, "-");
    acc[slug] = curr.hex;
    return acc;
  }, {}),
};

console.log(JSON.stringify(designTokens, null, 2));
```

### Sketch Plugin Manifest (`manifest.json`)

Creating a developer handoff plugin for Sketch:

```json
{
  "name": "Design Token Exporter",
  "identifier": "com.company.sketch.token-exporter",
  "version": "1.0.0",
  "description": "Exports Sketch color variables and text styles to Tailwind CSS tokens.",
  "author": "Engineering Design Team",
  "appcast": "https://raw.githubusercontent.com/company/sketch-plugin/main/appcast.xml",
  "commands": [
    {
      "name": "Export Tokens to JSON",
      "identifier": "export-tokens",
      "script": "./plugin.js",
      "handler": "onExportTokens"
    }
  ],
  "menu": {
    "title": "Design Tokens",
    "items": ["export-tokens"]
  }
}
```

### Exporting SVG Assets with Clean Paths

- Select artboard or symbol -> Right sidebar -> **Make Exportable**.
- Format: **SVG** (enable **Compact SVG** to remove editor metadata).
- Automate CLI export using `sketchtool`:
  ```bash
  sketchtool export slices "DesignSystem.sketch" --output="./dist/assets/" --formats="svg,png"
  ```

## Common Patterns

### Reusable Symbol Design with Smart Layout

**Problem**: Buttons and card components break layout when text labels change in length.  
**Solution**: Apply Smart Layout to Symbols.

1. Select button group (Background + Text).
2. In the Inspector panel, configure **Smart Layout**: Horizontal (Center or Left-to-Right).
3. Set text layer alignment and fixed paddings.
4. When overriding label in instances, the button auto-expands while preserving margins.

### Design System Token Export to Code

**Problem**: Sync Sketch color variables and typography to CSS variables or Tailwind tokens.  
**Solution**: Export JSON tokens via Sketch Cloud API or sketchtool.

```json
{
  "colors": {
    "primary": { "value": "#4F46E5" },
    "background": { "value": "#0F172A" }
  },
  "spacing": {
    "sm": { "value": "8px" },
    "md": { "value": "16px" }
  }
}
```

## Best Practices (2026)

- **Do** organize UI components into **Smart Layout Symbols** with flexible resizing constraints (Pin to edge, Fixed width/height).
- **Do** maintain a central **Shared Library** file hosted on Sketch Cloud for typography, colors, and elevation styles.
- **Do** run automated exports via `sketchtool` CLI in continuous integration pipelines for asset synchronization.
- **Do** name layers semantically (`header/search-input`, `button/primary/hover`) to improve developer handoff clarity.
- **Don't** leave detached symbols with unlinked layer styles across production design files.
- **Don't** commit multi-gigabyte `.sketch` binary files into standard Git repos; use Git LFS or Sketch Cloud.
- **Don't** export unoptimized SVGs; process exported vectors with SVGO before committing to frontend codebases.

## Troubleshooting

| Error / Symptom                                                 | Cause                                                             | Solution                                                                                         |
| --------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `sketchtool: command not found`                                 | Sketch command line tools not linked in system path               | Run `sudo /Applications/Sketch.app/Contents/Resources/sketchtool/bin/sketchtool-install.sh`.     |
| Symbol overrides reset when library updates                     | Symbol layer structure was modified or layer names desynchronized | Keep layer names identical in both base library and modified components to preserve overrides.   |
| Exported SVG icons have nested clipped paths and extra wrappers | Sketch exports artboard backgrounds or hidden masks               | Disable artboard background in export settings and flatten combined vector shapes before export. |

## References

- [Sketch Documentation](https://www.sketch.com/docs/)
