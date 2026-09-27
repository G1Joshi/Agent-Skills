---
name: plotly
description: Expert Plotly visualization assistance covering interactive D3/WebGL charts, Dash dashboards, Plotly Express, and animations. Use when building interactive web charts and analytical data applications.
---

# Plotly

Plotly creates **interactive** (zoomable, hoverable) charts in the browser. v6.0 (2025) drops big dependencies (Pandas is optional) and improves performance.

## When to Use

- **Interactive Web Dashboards & Visualizations**: Building zoomable, pan-able, and hover-interactive charts in Python/JS.
- **Financial & Candlestick Charts**: Displaying high-frequency stock, crypto, and commodity data with interactive range sliders.
- **3D Surface & Geospatial Mapping**: Rendering 3D point clouds, geospatial choropleth maps, and WebGL scatter plots.
- **Jupyter & Streamlit Integration**: Embedding interactive visualizations into Streamlit, Dash, or JupyterLab.

## Quick Start

```python
import plotly.express as px

# Create interactive scatter plot with hover tooltips and trendline
df = px.data.iris()
fig = px.scatter(
    df, x="sepal_width", y="sepal_length",
    color="species", size="petal_length",
    hover_data=["petal_width"],
    title="Iris Dataset - Interactive Feature Exploration"
)

# Open in browser or render in Jupyter
fig.show()
```

## Core Concepts

#High-Level Charting with Plotly Express

Generating rich multi-variable interactive charts in one line:

```python
import plotly.express as px
import pandas as pd

# Load sample dataset
df = px.data.gapminder().query("year == 2007")

fig = px.scatter(
    df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
    title="Global Health vs. Wealth (2007)",
    labels={"gdpPercap": "GDP per Capita (USD)", "lifeExp": "Life Expectancy (Years)"},
    template="plotly_white"
)

# Customize hover tooltip formatting
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>GDP/Capita: $%{x:,.2f}<br>Life Expectancy: %{y:.1f} yrs<extra></extra>"
)

# Export interactive HTML widget
fig.write_html("interactive_scatter.html", include_plotlyjs="cdn")
```

#Financial Candlestick Chart with Range Slider (graph_objects)

Detailed technical analysis with interactive time navigation:

```python
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['AAPL.Open'],
    high=df['AAPL.High'],
    low=df['AAPL.Low'],
    close=df['AAPL.Close'],
    name='AAPL'
)])

fig.update_layout(
    title='Apple Inc. (AAPL) Stock Price',
    yaxis_title='Stock Price (USD)',
    xaxis_rangeslider_visible=True,
    template='plotly_dark'
)

fig.write_html("candlestick_chart.html")
```

#Interactive Subplot Grid with Secondary Y-Axis

Combining bar charts and line charts across synchronized subplots:

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(specs=[[{"secondary_y": True}]])

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
fig.add_trace(go.Bar(x=months, y=[120, 150, 180, 220, 260, 310], name="Revenue ($k)"), secondary_y=False)
fig.add_trace(go.Scatter(x=months, y=[85, 88, 89, 92, 94, 95], name="Retention (%)", mode="lines+markers"), secondary_y=True)

fig.update_layout(title="H1 Revenue & Retention Trends", template="plotly_white")
fig.update_yaxes(title_text="Revenue in Thousands ($)", secondary_y=False)
fig.update_yaxes(title_text="Customer Retention Rate (%)", secondary_y=True)
```

## Common Patterns

### Customizing Layout and Dark Theme Styling

**Problem**: Default white themes mismatch dark mode application dashboards.

**Solution**:
Apply custom templates and update figure layout:

```python
fig.update_layout(
    template="plotly_dark",
    title_font_size=20,
    xaxis_title="Measurement",
    yaxis_title="Count",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=60, b=40)
)

# Export interactive standalone HTML
fig.write_html("dashboard_chart.html")
```

## Best Practices (2026)

- **Do** start with `plotly.express` for rapid prototyping; drop down to `plotly.graph_objects` only for complex multi-axis layouts.
- **Do** use `include_plotlyjs="cdn"` when exporting HTML files to reduce file size from 3MB down to a few kilobytes.
- **Do** use WebGL-accelerated traces (`go.Scattergl`) when rendering more than 50,000 points to keep the browser responsive.
- **Do** customize `hovertemplate` to display meaningful business units and currency signs cleanly.
- **Don't** plot millions of raw points without downsampling; dense overlapping points degrade browser DOM rendering.
- **Don't** embed full static PNG images when users need zoom, pan, and hover interactivity.
- **Don't** forget to set responsive container sizing (`fig.update_layout(autosize=True)`).

## Troubleshooting

| Error                                                      | Cause                                                        | Solution                                                                      |
| :--------------------------------------------------------- | :----------------------------------------------------------- | :---------------------------------------------------------------------------- |
| `fig.show() does nothing in terminal script`               | Terminal execution lacks browser renderer or Jupyter widget. | Export to HTML with `fig.write_html("chart.html")` or run in Jupyter.         |
| `ValueError: Plotly Express cannot process wide-form data` | DataFrame columns not in tidy (long) format.                 | Use `df.melt()` to convert wide DataFrame into long-form format.              |
| `Slow rendering with 100k+ data points`                    | SVG rendering bottleneck in browser DOM.                     | Use WebGL-accelerated chart variants: `go.Scattergl` instead of `go.Scatter`. |

## References

- [Plotly Python](https://plotly.com/python/)
