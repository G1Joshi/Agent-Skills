---
name: jupyter
description: Jupyter notebooks for interactive computing. Use for data exploration.
---

# Jupyter

Jupyter is the de facto standard for interactive data science. v7 (2025) of the Notebook is built on JupyterLab components, offering a modern, extensible experience.

## When to Use

- **Exploratory Data Analysis (EDA)**: Plotting data inline (`matplotlib`).
- **Education**: Teaching code with markdown explanations.
- **Prototyping**: Testing snippets before moving to a script.

## Core Concepts

### Kernels

The computation engine (IPython, IJulia).

### Cells

Code cells (executed) vs Markdown cells (documentation).

### Magic Commands

`%timeit`, `!pip install`.

## Best Practices (2025)

**Do**:

- **Use JupyterLab**: The richer, multi-tab interface is standard.
- **Use `nbdev`**: If you want to build libraries from notebooks.
- **Use Version Control**: Use `jupytext` to pair notebooks with `.py` files for git diffs.

**Don't**:

- **Don't store secrets**: Clear output before committing.

## References

- [Jupyter Documentation](https://jupyter.org/)
