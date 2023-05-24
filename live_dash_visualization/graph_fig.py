import plotly.graph_objs as go
from .config import N_SENSORS

# Create initial empty data lists
x_data = []
y_data = [[] for _ in range(N_SENSORS)]

# Create plot traces for each temperature
plot_data = []
for i in range(N_SENSORS):
    trace = go.Scatter(
        x=x_data,
        y=y_data[i],
        mode="lines",
        name=f"Sensor {i+1}",
        line=dict(width=2),
    )
    plot_data.append(trace)


# Create plot layout
layout = go.Layout(
    xaxis=dict(title="Time"),
    yaxis=dict(title="Temperature"),
    showlegend=True,
    width=1120,
    height=700
)

# Create plot figure and heatmap figure
fig = go.Figure(data=plot_data, layout=layout)

