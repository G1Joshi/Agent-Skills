---
name: jupyter
description: Expert Jupyter Notebook assistance covering interactive Python, kernels, ipywidgets, magic commands, and reproducible data science. Use when prototyping data analysis, ML experiments, and interactive visualizations.
---

# Jupyter

Jupyter is the de facto standard for interactive data science. v7 (2025) of the Notebook is built on JupyterLab components, offering a modern, extensible experience.

## When to Use

- **Exploratory Data Analysis (EDA)**: Interactive data investigation, statistical analysis, and visual storytelling.
- **Machine Learning Experimentation**: Rapidly prototyping model architectures, training loops, and loss visualizations.
- **Interactive Technical Reports & Teaching**: Combining executable Python/R/Julia code, rich Markdown, LaTeX, and charts.
- **Automated Batch Notebook Execution**: Executing parameterized notebooks in production pipelines with Papermill.

## Quick Start

```bash
# Install and launch JupyterLab
pip install jupyterlab
jupyter lab --port 8888
```

```python
# Useful built-in cell magics
%%time
import numpy as np
arr = np.random.randn(1000, 1000)
eig = np.linalg.eigvals(arr)
```

## Core Concepts

#Essential IPython Magic Commands

Optimizing execution, timing, and module reloading:

```python
# Automatically reload imported modules when modified on disk
%load_ext autoreload
%autoreload 2

# Measure execution time of a single statement
%timeit [i**2 for i in range(1000)]

# Profile execution time of an entire cell
%%time
import numpy as np
arr = np.random.rand(5000, 5000)
eigvals = np.linalg.eigvals(arr)

# Render Matplotlib plots inline with high DPI
%matplotlib inline
%config InlineBackend.figure_format = 'retina'
```

#Interactive UI Widgets with ipywidgets

Building interactive parameter tuning controls inside the notebook:

```python
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np

def plot_sine_wave(frequency=1.0, amplitude=1.0):
    x = np.linspace(0, 10, 500)
    y = amplitude * np.sin(frequency * x)

    plt.figure(figsize=(8, 3))
    plt.plot(x, y, color='#2563eb', lw=2)
    plt.ylim(-3, 3)
    plt.grid(True, alpha=0.3)
    plt.title(f"Sine Wave: freq={frequency}, amp={amplitude}")
    plt.show()

# Connect function to interactive slider widgets
widgets.interact(
    plot_sine_wave,
    frequency=widgets.FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1),
    amplitude=widgets.FloatSlider(value=1.0, min=0.1, max=3.0, step=0.1)
);
```

#Parameterized Execution with Papermill

Running notebooks programmatically in production data workflows:

```bash
# Execute notebook from command line with custom parameters
papermill monthly_report.ipynb output_report.ipynb \
  -p customer_region "EMEA" \
  -p fiscal_year 2026 \
  -p threshold_amount 50000.0
```

## Common Patterns

### Interactive Parameter Tuning with ipywidgets

**Problem**: Manually re-running notebook cells with different hyperparameter values is slow and tedious.

**Solution**:
Use `ipywidgets.interact` for live sliders:

```python
from ipywidgets import interact
import matplotlib.pyplot as plt
import numpy as np

@interact(frequency=(1.0, 10.0, 0.5), amplitude=(0.5, 3.0, 0.2))
def plot_wave(frequency=2.0, amplitude=1.0):
    t = np.linspace(0, 1, 500)
    y = amplitude * np.sin(2 * np.pi * frequency * t)
    plt.figure(figsize=(8, 3))
    plt.plot(t, y)
    plt.ylim(-3.5, 3.5)
    plt.show()
```

## Best Practices (2026)

- **Do** restart kernel and run all cells (`Kernel -> Restart and Run All`) before committing to verify reproducibility.
- **Do** use `nbstripout` or `jupytext` in Git hooks to avoid committing huge binary outputs and image outputs.
- **Do** move complex, reusable functions from notebook cells into tested `.py` modules and import them.
- **Do** configure `%config InlineBackend.figure_format = 'retina'` for crisp charts on high-DPI displays.
- **Don't** leave notebooks with out-of-order execution states (e.g. In [45] before In [2]).
- **Don't** commit sensitive database passwords, cloud tokens, or API keys inside notebook output cells.
- **Don't** use Jupyter notebooks for complex long-running production services; export production logic to scripts/packages.

## Troubleshooting

| Error                                    | Cause                                                                      | Solution                                                                             |
| :--------------------------------------- | :------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `No module named '...' in notebook cell` | Notebook running in different Python kernel/environment than active shell. | Install ipykernel in target venv: `python -m ipykernel install --user --name myenv`. |
| `Kernel died, restarting`                | Process ran out of RAM or triggered C/C++ segmentation fault.              | Monitor system RAM usage and downsample large datasets before plotting.              |
| `IFrame / Widget Javascript error`       | JupyterLab extension not enabled or version mismatch.                      | Run `jupyter lab build` or install compatible widget extensions.                     |

## References

- [Jupyter Documentation](https://jupyter.org/)
