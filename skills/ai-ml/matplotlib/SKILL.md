---
name: matplotlib
description: Expert Matplotlib visualization assistance covering figure subplots, custom styling, colormaps, and publication-ready charts. Use when creating static or publication scientific figures in Python.
---

# Matplotlib

Matplotlib is the grandfather of Python plotting. It is verbose but provides **infinite control**.

## When to Use

- **Publication-Quality Scientific Plotting**: Generating exact, reproducible figures for academic papers, documentation, and reports.
- **Fine-Grained Custom Visualizations**: Complete control over every pixel, tick, axis spine, legend, and colorbar.
- **Headless Server-Side Chart Rendering**: Generating PNG, SVG, and PDF visualizations in backend microservices without GUI displays.
- **Subplot Grid Layouts**: Assembling multi-panel visual figure grids with `GridSpec`.

## Quick Start

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
ax.plot(x, y1, label="sin(x)", color="#2563eb", linewidth=2)
ax.plot(x, y2, label="cos(x)", color="#dc2626", linestyle="--")

ax.set_title("Trigonometric Functions")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

## Core Concepts

### Object-Oriented Subplots & Modern Styling

Building clean, publication-ready multi-axis figures:

```python
import matplotlib.pyplot as plt
import numpy as np

# Use non-interactive backend for server environments
import matplotlib
matplotlib.use('Agg')

# Set modern styling parameters
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

x = np.linspace(0, 10, 200)
y1 = np.sin(x) * np.exp(-0.1 * x)
y2 = np.cos(x) * np.exp(-0.1 * x)

# Panel 1: Line plot with error bands
ax1.plot(x, y1, color='#2563eb', lw=2, label='Damped Sine')
ax1.fill_between(x, y1 - 0.2, y1 + 0.2, color='#2563eb', alpha=0.15)
ax1.set_title("Signal Decay", fontsize=12, fontweight='bold')
ax1.set_xlabel("Time (seconds)")
ax1.set_ylabel("Amplitude")
ax1.legend(loc='upper right')

# Panel 2: Distribution histogram
data = np.random.normal(loc=0, scale=1, size=1000)
ax2.hist(data, bins=30, color='#10b981', edgecolor='white', alpha=0.85)
ax2.set_title("Residual Distribution", fontsize=12, fontweight='bold')
ax2.set_xlabel("Value")
ax2.set_ylabel("Frequency")

plt.tight_layout()
fig.savefig("metrics_figure.png", dpi=300, bbox_inches='tight')
plt.close(fig)
```

### Secondary Twin Axis (twinx)

Plotting two metrics with different scales on the same chart:

```python
fig, ax1 = plt.subplots(figsize=(8, 4.5))

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [120, 145, 160, 190, 210, 250]
churn_rate = [2.4, 2.1, 1.9, 1.8, 1.5, 1.2]

# Primary axis: Bar chart
bars = ax1.bar(months, revenue, color='#4f46e5', alpha=0.7, width=0.5, label='Revenue ($k)')
ax1.set_ylabel('Revenue in Thousands ($)', color='#4f46e5')
ax1.tick_params(axis='y', labelcolor='#4f46e5')

# Secondary axis: Line plot
ax2 = ax1.twinx()
line = ax2.plot(months, churn_rate, color='#ef4444', lw=3, marker='o', label='Churn Rate (%)')
ax2.set_ylabel('Churn Rate (%)', color='#ef4444')
ax2.tick_params(axis='y', labelcolor='#ef4444')
ax2.grid(False) # Prevent overlapping grid lines

plt.title("Revenue Growth vs. Churn Reduction (2026)")
plt.savefig("revenue_churn.png", bbox_inches='tight')
plt.close(fig)
```

### Heatmaps & Custom Colormaps

Visualizing correlation matrices or loss surfaces:

```python
matrix = np.corrcoef(np.random.randn(8, 100))

fig, ax = plt.subplots(figsize=(6, 5))
cax = ax.matshow(matrix, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)

ax.set_xticks(range(8))
ax.set_yticks(range(8))
ax.set_title("Correlation Heatmap", pad=20)
plt.savefig("heatmap.png", bbox_inches='tight')
plt.close(fig)
```

## Common Patterns

### Clean Multi-Panel Subplots with Shared Axes

**Problem**: Creating multiple comparative charts where axis ranges must stay aligned.

**Solution**:
Use `plt.subplots` with shared axes:

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

ax1.plot(x, y1, color="navy")
ax1.set_ylabel("Raw Signal")

ax2.plot(x, np.abs(y1), color="darkorange")
ax2.set_ylabel("Rectified")
ax2.set_xlabel("Sample")

plt.tight_layout()
```

## Best Practices

**Do**:

- Use the Object-Oriented interface (`fig, ax = plt.subplots()`) instead of stateful `plt.plot()` calls.
- Set `matplotlib.use('Agg')` when running inside serverless functions, Docker, or CI without a desktop display.
- Always call `plt.close(fig)` after saving to disk to prevent memory leaks from accumulated figures.
- Save figures with `bbox_inches='tight'` to prevent labels and titles from being clipped at margins.

**Don't**:

- Use rainbow/jet colormaps; use perceptively uniform colormaps (`viridis`, `plasma`, `coolwarm`).
- Rely on default DPI (100); export publication graphics with at least `dpi=300`.
- Leave gridlines enabled on both axes when using `twinx()`; disable one to prevent clutter.

## Troubleshooting

| Error                                                                        | Cause                                                    | Solution                                                            |
| :--------------------------------------------------------------------------- | :------------------------------------------------------- | :------------------------------------------------------------------ |
| `UserWarning: Matplotlib is currently using agg, which is a non-GUI backend` | Attempting `plt.show()` in headless server/container.    | Save figure to disk instead: `fig.savefig('output.png')`.           |
| `Labels overlapping or cut off`                                              | Figure bounding box too tight for tick labels.           | Call `plt.tight_layout()` or use `bbox_inches='tight'` when saving. |
| `Memory leak: Figures not closing`                                           | Creating figures in loops without calling `plt.close()`. | Add `plt.close(fig)` at the end of each loop iteration.             |

## References

- [Matplotlib Documentation](https://matplotlib.org/)
