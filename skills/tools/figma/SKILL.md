---
name: figma
description: Expert Figma design tool assistance covering auto-layout, design tokens, component variants, REST API, and dev mode. Use when translating UI designs into production code and inspecting components.
---

# Figma

Figma is a collaborative cloud-based interface design tool featuring vector networks, design tokens, component variant libraries, and dedicated Dev Mode inspect tooling.

## When to Use

- **Collaborative UI/UX Design & Prototyping**: Designing interfaces, design systems, wireframes, and user flows.
- **Design Token Extraction via Figma REST API**: Exporting colors, typography, spacing, and variables to JSON/Tailwind.
- **Dev Mode & Code Inspection**: Inspecting CSS, iOS SwiftUI, and Android Compose properties directly from design frames.
- **Custom Figma Plugin Development**: Automating asset export, linting layers, and syncing with code repositories.

## Quick Start

```bash
# Query Figma REST API to extract design tokens / styles
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/{file_key}/styles" | jq '.meta.styles[] | {name, style_type}'
```

## Core Concepts

### Fetching Design Tokens via Figma REST API

Extracting variables and color styles using Node.js:

```typescript
import axios from "axios";

const FIGMA_API_TOKEN = process.env.FIGMA_ACCESS_TOKEN!;
const FILE_KEY = "vXyZ123456AbCdEf";

async function exportDesignTokens() {
  const response = await axios.get(
    `https://api.figma.com/v1/files/${FILE_KEY}/variables/local`,
    {
      headers: { "X-Figma-Token": FIGMA_API_TOKEN },
    },
  );

  const variables = response.data.meta.variables;
  const designTokens: Record<string, any> = {};

  for (const id in variables) {
    const v = variables[id];
    designTokens[v.name] = {
      type: v.resolvedType,
      value: v.valuesByMode[Object.keys(v.valuesByMode)[0]],
    };
  }

  console.log("Exported Tokens:", JSON.stringify(designTokens, null, 2));
}

exportDesignTokens();
```

### Developing a Figma Plugin (manifest.json & code.ts)

Creating an automation plugin to inspect layers:

```json
// manifest.json
{
  "name": "Design Token Linter",
  "id": "1234567890123456",
  "api": "1.0.0",
  "main": "code.js",
  "capabilities": [],
  "enableProposedApi": false,
  "editorType": ["figma"]
}
```

```typescript
// code.ts (Runs in Figma sandbox)
figma.showUI(__html__, { width: 320, height: 240 });

figma.ui.onmessage = (msg) => {
  if (msg.type === "scan-selection") {
    const selection = figma.currentPage.selection;
    let unstyledLayers = 0;

    for (const node of selection) {
      if ("fills" in node && (!node.fillStyleId || node.fillStyleId === "")) {
        unstyledLayers++;
      }
    }

    figma.ui.postMessage({
      type: "scan-result",
      unstyledCount: unstyledLayers,
    });
  }
};
```

### Dev Mode Code Generation

Mapping Figma variables directly to Tailwind CSS:

- Open **Dev Mode** in Figma (`Shift + D`).
- Inspect component tokens: `background: var(--color-primary-500)`.
- Export CSS variables directly into `theme.css` / Tailwind `@theme` directives.

## Common Patterns

### Design Token Export Pipeline (Figma Tokens to Tailwind CSS)

**Problem**: Designers update color palettes in Figma while developers manually copy hex codes.

**Solution**:
Automate token extraction using Figma REST API:

```javascript
async function exportTokens(fileKey, token) {
  const res = await fetch(
    `https://api.figma.com/v1/files/${fileKey}/variables/local`,
    {
      headers: { "X-Figma-Token": token },
    },
  );
  const data = await res.json();

  // Map Figma Variables directly into Tailwind CSS color theme tokens
  const colors = {};
  for (const [id, v] of Object.entries(data.meta.variables)) {
    if (v.resolvedType === "COLOR") {
      colors[v.name] =
        v.valuesByMode[
          data.meta.variableCollections[v.variableCollectionId].defaultModeId
        ];
    }
  }
  return colors;
}
```

## Best Practices

**Do**:

- Build components using Figma Auto Layout (`Shift + A`) to accurately reflect CSS flexbox and responsive behaviors.
- Define global color, spacing, and typography variables in Figma Variables to automate design token exports.
- Use Figma Dev Mode to inspect exact CSS, Jetpack Compose, and SwiftUI code generation snippets.
- Name frames and layers with semantic identifiers (e.g. `Button/Primary/Hover`) rather than default `Frame 42`.

**Don't**:

- Detach component instances; use component variants and properties (`boolean`, `instance swap`, `text`).
- Hardcode raw hex values in design mockups; bind colors to design tokens.
- Commit Figma personal access tokens to public GitHub repositories.

## Troubleshooting

| Error                                     | Cause                                                            | Solution                                                                   |
| :---------------------------------------- | :--------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `Figma API: 403 Invalid token`            | Personal access token expired or revoked.                        | Generate fresh Personal Access Token in Figma Account Settings > Security. |
| `Auto-layout breaks when resizing parent` | Child elements set to "Fixed width" instead of "Fill container". | Change child resizing property to "Fill container" in Figma Dev Mode.      |
| `Exported SVG missing fonts or icons`     | Text layers not converted to outlines prior to export.           | Outline text layers (`Cmd+Shift+O`) or embed font families in SVG.         |

## References

- [Figma Help](https://help.figma.com/)
