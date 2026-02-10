---
name: matplotlib
description: Matplotlib data visualization library. Use for plotting.
---

# Matplotlib

Matplotlib is the grandfather of Python plotting. It is verbose but provides **infinite control**.

## When to Use

- **Publication**: Creating figures for papers (PDF/SVG).
- **Customization**: When you need to control every pixel.
- **Backend**: It powers Seaborn and Pandas plotting.

## Core Concepts

### Figure & Axes

The container (`fig`) and the plot area (`ax`). Always use the OO interface, not `plt.plot`.

### Backends

Interactive (`Qt`, `WebAgg`) vs Static (`Agg`).

## Best Practices (2025)

**Do**:

- **Use `plt.subplots()`**: The Object-Oriented style.
- **Use `style.use('seaborn-v0_8')`**: Make it look decent by default.

**Don't**:

- **Don't use `pylab`**: It is deprecated and pollutes namespaces.

## References

- [Matplotlib Documentation](https://matplotlib.org/)
