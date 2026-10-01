---
name: seaborn
description: Expert Seaborn statistical data visualization assistance covering statistical charts, categorical plots, heatmap matrices, and themes. Use when creating insightful statistical graphics and exploratory data analysis plots.
---

# Seaborn

Seaborn is a high-level wrapper around Matplotlib. It makes **statistical plots** (violins, heatmaps, pairs) easy.

## When to Use

- **Statistical Data Visualization**: Producing clear distribution plots, regression curves, and correlation heatmaps.
- **Multi-Plot Categorical Comparisons**: Visualizing complex distributions with `boxplot`, `violinplot`, and `catplot`.
- **Modern Object Interface (sns.objects)**: Clean grammar of graphics visualization inspired by ggplot2.
- **Pairwise Feature Exploration**: Rapidly identifying variable correlations and cluster separations with `pairplot`.

## Quick Start

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Load sample dataset and plot regression with confidence interval
tips = sns.load_dataset("tips")

plt.figure(figsize=(8, 5))
sns.set_theme(style="whitegrid")
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time", size="size")
plt.title("Tip Amount vs Total Bill by Dining Time")
plt.show()
```

## Core Concepts

### Modern Seaborn Objects Interface (sns.objects)

Grammar of graphics data visualization:

```python
import seaborn.objects as so
import seaborn as sns
import matplotlib.pyplot as plt

# Load sample dataset
penguins = sns.load_dataset("penguins").dropna()

# Declarative grammar of graphics plot
plot = (
    so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm", color="species", pointsize="body_mass_g")
    .add(so.Dots(alpha=0.7))
    .add(so.Line(), so.PolyFit(order=1))
    .label(
        title="Penguin Bill Dimensions & Linear Fits",
        x="Bill Length (mm)",
        y="Bill Depth (mm)",
        color="Species"
    )
    .theme({"axes.grid": True})
)

fig = plt.figure(figsize=(9, 5))
plot.on(fig).save("seaborn_objects_plot.png")
```

### Statistical Distributions & Faceted Grids

Visualizing density and distributions across categories:

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="muted")
tips = sns.load_dataset("tips")

# Multi-panel faceted distribution
g = sns.displot(
    data=tips,
    x="total_bill",
    hue="time",
    col="day",
    kind="kde",
    fill=True,
    common_norm=False,
    palette="crest",
    height=3.5,
    aspect=0.8
)

g.set_axis_labels("Total Bill ($)", "Density")
g.savefig("tips_kde_faceted.png", bbox_inches="tight")
plt.close()
```

### Categorical Box and Violin Comparisons

Comparing distributions across discrete classes:

```python
fig, ax = plt.subplots(figsize=(8, 5))

sns.violinplot(
    data=tips,
    x="day",
    y="total_bill",
    hue="sex",
    split=True,
    inner="quart",
    palette={"Male": "#3b82f6", "Female": "#ec4899"},
    ax=ax
)

ax.set_title("Total Bill Distribution by Day & Gender")
plt.savefig("violin_comparison.png", bbox_inches="tight")
plt.close(fig)
```

## Common Patterns

### Correlation Heatmap with Masked Triangle

**Problem**: Large correlation heatmaps are visually redundant and cluttered when showing both upper and lower triangles.

**Solution**:
Mask upper triangle using NumPy:

```python
import numpy as np

corr = df.select_dtypes(include=np.number).corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

plt.figure(figsize=(10, 8))
sns.heatmap(corr, mask=mask, cmap="vlag", vmax=1.0, vmin=-1.0,
            annot=True, fmt=".2f", square=True, linewidths=.5)
plt.title("Feature Correlation Matrix")
plt.show()
```

## Best Practices

**Do**:

- Adopt the new `seaborn.objects` (`so.Plot`) API for modern, composable grammar-of-graphics visualizations.
- Apply `sns.set_theme()` at application startup to configure consistent typography and aesthetic palettes.
- Pass tidy long-form DataFrames to Seaborn functions (`data=df, x='col1', y='col2', hue='category'`).
- Always close Matplotlib figures (`plt.close(fig)`) when generating charts in backend web pipelines.

**Don't**:

- Use pie charts for categorical proportions; use horizontal bar charts (`sns.barplot`).
- Overload charts with more than 4-5 categories in `hue`; use faceted subplots (`col='category'`) instead.
- Mix stateful `plt.title()` with object-oriented `ax.set_title()`.

## Troubleshooting

| Error                                                      | Cause                                            | Solution                                                       |
| :--------------------------------------------------------- | :----------------------------------------------- | :------------------------------------------------------------- |
| `TypeError: Object of type '...' is not JSON serializable` | Passing non-numeric columns to `heatmap()`.      | Filter numeric columns: `df.select_dtypes(include=np.number)`. |
| `Seaborn plot showing tiny unreadable fonts`               | Default scaling mismatch with high-DPI displays. | Set context scaling: `sns.set_context("talk")` or `"poster"`.  |
| `AttributeError: module 'seaborn' has no attribute '...'`  | Outdated Seaborn version installed.              | Upgrade Seaborn to 0.13+: `pip install --upgrade seaborn`.     |

## References

- [Seaborn Documentation](https://seaborn.pydata.org/)
